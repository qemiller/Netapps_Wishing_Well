######### this is the repo file
import pika
import pymongo
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
inputChannel = connection.channel()

inputChannel.exchange_declare(exchange='Squires',exchange_type='direct')
inputChannel.exchange_declare(exchange='Library',exchange_type='direct')
inputChannel.exchange_declare(exchange='Goodwin',exchange_type='direct')
inputChannel.queue_declare(exchange='Squires', queue='Food')
inputChannel.queue_declare(exchange='Squires', queue='Meetings')
inputChannel.queue_declare(exchange='Squires', queue='Rooms')

result = inputChannel.queue_declare(exclusive=True)
queueName = result.method.queue
exchangeName = result.method.exchange

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

inputChannel.queue_bind(exchange=exchangeName,queue=queue_name,routing_key=queueName)

print(' [*] Waiting for logs. To exit press CTRL+C')

inputChannel.basic_consume(callback, queue=queue_name, no_ack=True)
inputChannel.start_consuming()
