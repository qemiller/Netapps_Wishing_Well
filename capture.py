import pika



def getTweet():
    #add code to get tweets from stream in here
    #return an array of thecommand type, place, subject, and message.
    #array should have command type in the zero index, place in the first index,
    #subject in the second, and message in the third.
    
def waitingForTweet():
    #make the light white

def receivedPublish():
    #make the light red

def receivedConsume():
    #make the light green

connection = pika.BlockingConnection(pike.ConnectionParameters('localhost'))
channel = connection.channel()

while(1):
    waitingForTweet()
    tweet[] = getTweet()
    if tweet[0] == 'p':
        receivedPublish()
        channel.exchange_declare(exchange=tweet[1], exchange_type='direct')
        channel.basic_publish(exchange=tweet[1], routing_key=tweet[2], body=tweet[3])
    
    
    if tweet[0] == 'c':
        receivedConsume()
        channel.queue_bind(exchange=tweet[1], queue=queue_name, routing_key=tweet[2])
        channel.basic_consume(callback, queue=queue_name, no_ack=True)
        channel.start_consuming()







