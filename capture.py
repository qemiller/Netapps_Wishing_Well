import pika
import RPi.GPIO as GPIO
import time
from tweepy import Stream #pip3 install tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

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
	data=(type,place,subject,message)
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


def notify_consumer(which_queue):
    print('here we will notify the repository pi and tell it what queue to consume from: ', which_queue)

def publish_to_queue(place, subject, message):
    print(place, subject, message)
    #this basic publish uses parameters from the 'p' type tweet
    channel.basic_publish(exchange=place, routing_key=subject, body=message)

def write_to_db(tweet_tuple):
    client = pymongo.MongoClient()
    db = client[str(tweet_tuple[1])]
    col = db[str(tweet_tuple[2])]
    messageid = str(time.time())
    action = tweet_tuple[0]
    place = tweet_tuple[1]
    subject = tweet_tuple[2]
    message = tweet_tuple[3]
    dict_to_insert = {"Action": action, "Place": place, "MsgID": messageid, "Subject": subject, "Message": message}
    col.insert_one(dict_to_insert)

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
# EDIT: WE MAY CHANGE SO THAT IT CREATES NO MATTER WHAT TO AVOID ISSUES DURING DEMO
#channel.exchange_declare(exchange='Goodwin',
#						 exchange_type='direct', durable=True)

#channel.exchange_declare(exchange='Squires',
#						 exchange_type='direct', durable=True)

#channel.exchange_declare(exchange='Library',
#						 exchange_type='direct', durable=True)
# End pike/rabbitmq setup

# set up GPIO stuff for LEDS
redLED = 15
greenLED = 13
blueLED = 11

channelList = [redLED, greenLED, blueLED]
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channelList, GPIO.OUT)


class listener(StreamListener):
	def on_data(self, data):
		readIN=json.loads(data)
		tweet=readIN["text"]
		user=readIN["user"]["screen_name"]
		token_tweet=token(tweet)
		write_to_db(token_tweet) #send to local MongoDB instance
		print(user,"___",token_tweet)
		if token_tweet[0] == 'p':
			receivedPublishLED()
			publish_to_queue(token_tweet[1], token_tweet[2], token_tweet[3])
		else:
			receivedConsumeLED()
			notify_consumer(token_tweet[2])
		waitingForTweetLED()
		return True
	def on_error(self, status):
		print(status)

auth = OAuthHandler(API_key,API_secret_key)
auth.set_access_token(Access_token, Access_token_secret)
tweets=Stream(auth, listener())

#reading tweets start with #ECE4564T11
#notest there is space #ECE4564T11 
tweets.filter(track=["#ECE4564T11"])


"""
while(1):
#    waitingForTweet()
    tweet = []
    tweet[0] = input('produce or consume?\n')
    tweet[1] = input('Place\n')
    tweet[2] = input('Subject\n')
    tweet[3] = input('message')
    if tweet[0] == 'p':
        receivedPublish()
        channel.basic_publish(exchange=tweet[1], routing_key=tweet[2], body=tweet[3])
        print('sent ', tweet[3])
    
    if tweet[0] == 'c':
        receivedConsume()
        channel.queue_bind(exchange=tweet[1], queue=queue_name, routing_key=tweet[2])
        channel.basic_consume(callback, queue=queue_name, no_ack=True)
        channel.start_consuming()

"""
#soure for ribbitMQ 
#https://www.vultr.com/docs/how-to-install-rabbitmq-on-ubuntu-16-04-47
