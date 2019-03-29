import pika
#import RPi.GPIO as GPIO
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

Access_token="1110278796710694912-E3GEGKkHNM6IwVpgwsJ1kx4h2ChdmU"
Access_token_secret="kv813RHVcuf4RXSkL9VcClyDMmPk68ZxkJU4tuRIqFXWf"
API_key="2xbt50RBjGIK1NJJp059cPbFy"
API_secret_key="WTFNfQllRT4hO8SoMXwQb6asiF0SJORIzn2uFXl9CcMLnP5lHA"

class listener(StreamListener):
	def on_data(self, data):
		readIN=json.loads(data)
		tweet=readIN["text"]
		user=readIN["user"]["screen_name"]
		token_tweet=token(tweet)
		print(user,"___",token_tweet)
		if(token_tweet[0] == 'p'):
			publish_to_queue(token_tweet[1], token_tweet[2], token_tweet[3])
		else:
		    notify_consumer(token_tweet[2])
		return True
	def on_error(self, status):
		print(status)

auth = OAuthHandler(API_key,API_secret_key)
auth.set_access_token(Access_token, Access_token_secret)
tweets=Stream(auth, listener())

#reading tweets start with #ECE4564T11
#notest there is space #ECE4564T11 
tweets.filter(track=["#ECE4564T11"]

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



#def waitingForTweet():
    #make the light white

#def receivedPublish():
    #make the light red

#def receivedConsume():
    #make the light green

def notify_consumer(which_queue):
	print('here we will notify the repository pi and tell it what queue to consume from: ', which_queue)

def publish_to_queue(place, subject, message):
	#this basic publish uses parameters from the 'p' type tweet
	channel.basic_publish(exchange=place, routing_key=subject, body=message)
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