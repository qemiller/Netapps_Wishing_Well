import pika
#import RPi.GPIO as GPIO
import time
from tweepy import Stream #pip install tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

Access_token="1110278796710694912-E3GEGKkHNM6IwVpgwsJ1kx4h2ChdmU"
Access_token_secret="kv813RHVcuf4RXSkL9VcClyDMmPk68ZxkJU4tuRIqFXWf"
API_key="2xbt50RBjGIK1NJJp059cPbFy"
API_secret_key="WTFNfQllRT4hO8SoMXwQb6asiF0SJORIzn2uFXl9CcMLnP5lHA"

class listener(StreamListener):
	def on_data(self, data):
		readIN=json.loads(data)
		tweet=readIN["text"]
		user=readIN["user"]["screen_name"]
		print(user,"___",tweet)
		return(true)
	def on_error(self, status):
		print(status)

auth = OAuthHandler(API_key,API_secret_key)
auth.set_access_token(Access_token, Access_token_secret)

tweets=Stream(auth, listener() )
tweets.filter(track=["#ECE4564T11"], async=true)
tweets.disconnect()
print("at the end")
"""
 
#def waitingForTweet():
    #make the light white

#def receivedPublish():
    #make the light red

#def receivedConsume():
    #make the light green

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='Squires', exchange_type='direct')
channel.exchange_declare(exchange='Goodwin', exchange_type='direct')
channel.exchange_declare(exchange='Library', exchange_type='direct')

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




