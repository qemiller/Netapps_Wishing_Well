import pika
#import RPi.GPIO as GPIO
import time



#def getTweet():
    #add code to get tweets from stream in here
    #return an array of thecommand type, place, subject, and message.
    #array should have command type in the zero index, place in the first index,
    #subject in the second, and message in the third.
    
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







