import pika
import RPi.GPIO as GPIO
import time
from tweepy import Stream #pip3 install tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import pymongo

def token(input):
	input=input.strip("#ECE4564T11 ")
	part=""
	subject=''
	message=''
	for i in input:
		if i==':':
			type=part
			part=''
		elif i=='+':
			place=part[1:]
			part=''
		elif i==' ' and subject=='':
			subject=part[1:]
			part=''
		part=part+i
	if type=='p':
		message=part
	else:
		subject=part[1:]
	data={'type':type,'place':place,'subject':subject,'message':message}
	return data
# LED functions
def waitingForTweetLED():
	GPIO.output(redLED, True)
	GPIO.output(blueLED, True)
	GPIO.output(greenLED, True)
	time.sleep(2)
	GPIO.output(redLED, False)
	GPIO.output(blueLED, False)
	GPIO.output(greenLED, False)

def receivedPublishLED():
	GPIO.output(redLED, True)
	time.sleep(2)
	GPIO.output(redLED, False)

def receivedConsumeLED():
	GPIO.output(greenLED, True)
	time.sleep(2)
	GPIO.output(greenLED, False)


def publish_to_queue(place, subject, message):
    #print(place, subject, message)
    #serialize message with json
    msg={'message':str(message)}
    payload=json.dumps(msg)
    #this basic publish uses parameters from the 'p' type tweet
    channel.basic_publish(exchange=place, routing_key=subject, body=payload)

def write_to_db(tweet_dict):
    client = pymongo.MongoClient()
    db = client[str(tweet_dict['place'])]
    col = db[str(tweet_dict['subject'])]
    messageid = str(time.time())
    action = tweet_dict['type']
    place = tweet_dict['place']
    subject = tweet_dict['subject']
    message = tweet_dict['message']
    dict_to_insert = {"Action": action, "Place": place, "MsgID": messageid, "Subject": subject, "Message": message}
    col.insert_one(dict_to_insert)
    return dict_to_insert

Access_token="1110278796710694912-E3GEGKkHNM6IwVpgwsJ1kx4h2ChdmU"
Access_token_secret="kv813RHVcuf4RXSkL9VcClyDMmPk68ZxkJU4tuRIqFXWf"
API_key="2xbt50RBjGIK1NJJp059cPbFy"
API_secret_key="WTFNfQllRT4hO8SoMXwQb6asiF0SJORIzn2uFXl9CcMLnP5lHA"

# This declares up the exchanges we will need for pika and RabbitMQ
credentials = pika.PlainCredentials('mqadmin', 'mqadminpassword')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.30.67.18', 5672, '/', credentials))
channel = connection.channel()
# declare the exchanges we need, with their queues
# no need to declare queues, as we've created them through the HTML interface
channel.exchange_declare(exchange='Goodwin',
						 exchange_type='direct', durable=True)

channel.exchange_declare(exchange='Squires',
						 exchange_type='direct', durable=True)

channel.exchange_declare(exchange='Library',
						 exchange_type='direct', durable=True)
channel.exchange_declare(exchange='Checkpoint',
						 exchange_type='direct', durable=True)

# End pike/rabbitmq setup
# set up GPIO stuff for LEDS
redLED = 15
greenLED = 13
blueLED = 11
def LED_setup():
	channelList = [redLED, greenLED, blueLED]
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(channelList, GPIO.OUT)


class listener(StreamListener):
	def on_data(self, data):
		readIN=json.loads(data)
		tweet=readIN["text"]
		#print('have read in tweet')
		#send to cmd queue with check point1 
		checkpoint1= "[Checkpoint 01  " + str(time.time()) + "] Tweet captured: " + tweet
		#print('created checkpoint1')
		token_tweet=token(tweet) #this returns a dictionary
		#print('created token_tweet: ', token_tweet)
		checkpoint1_json=json.dumps({"flag":'i',"checkpoint": checkpoint1}) #serialize results to send over pika->rabbitmq->socket
		channel.basic_publish(exchange="Checkpoint", routing_key="cmd",body=checkpoint1_json)
		#print('published checkpoint1 to cmd queue')
		dict=write_to_db(token_tweet) #send to local MongoDB instance
		#print('sent doc to mongodb: ', str(dict))
		checkpoint2= "[Checkpoint 02  " + str(time.time()) + "] Store command in MongoDB instance: " + str(dict)
		#print('created checkpoint2')
		checkpoint2_json=json.dumps({"flag":'i', "checkpoint":checkpoint2})
		channel.basic_publish(exchange="Checkpoint", routing_key="cmd", body=checkpoint2_json)	#send to mag DB with check point2
		#print('published checkpoint2 to cmd queue')
		#LED with check point3##########################
		checkpoint3= "[Checkpoint 03  " + str(time.time()) + "] GPIO LED: " +  "turning on LED"
		#print('created checkpoint3')
		flag='i'
		if token_tweet['type'] == 'c':
			flag='c'
		checkpoint3_json=json.dumps({"flag":flag,"checkpoint":checkpoint3, "subject": token_tweet["subject"]})
		channel.basic_publish(exchange="Checkpoint",routing_key="cmd", body= checkpoint3_json)
		#print('published checkpoint3 to cmd exchange')
		if token_tweet["type"] == 'p':
			receivedPublishLED()
			publish_to_queue(token_tweet['place'], token_tweet['subject'], token_tweet['message'])
		else:
			receivedConsumeLED()
			a,b,sendbackbody=channel.basic_get(queue='send_back')
			#print('This is what we got back from send_back queue: ',  sendbackbody)
			consumed_tweet=json.loads(sendbackbody.decode('utf-8'))
			print("tweet consumed by repo pi, and send to me (capture pi): ", consumed_tweet['message'])
		#check point 4 
		checkpoint4="[Checkpoing 04 " + str(time.time()) + "] Print out RabbitMQ command sent to Repository RPi: " + str(token_tweet)
		checkpoint4_json=json.dumps({'flag':'i',"checkpoint":checkpoint4,"subject":token_tweet["subject"]}) #include subject
		channel.basic_publish(exchange="Checkpoint",routing_key="cmd", body= checkpoint4_json)
		waitingForTweetLED()
		return True
	def on_error(self, status):
		print(status)
LED_setup()
waitingForTweetLED()
auth = OAuthHandler(API_key,API_secret_key)
auth.set_access_token(Access_token, Access_token_secret)
tweets=Stream(auth, listener())

#reading tweets start with #ECE4564T11
#notest there is a space after  #ECE4564T11
tweets.filter(track=["#ECE4564T11"])
GPIO.cleanup() #honestly don't know if this will get called when you ctl+c

#soure for ribbitMQ 
#https://www.vultr.com/docs/how-to-install-rabbitmq-on-ubuntu-16-04-47
