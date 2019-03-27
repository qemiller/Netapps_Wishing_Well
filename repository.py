###
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
inputChannel = connection.channel()

inputChannel.exchange_declare(exchange='Squires',type='direct')
inputChannel.exchange_declare(exchange='Library',type='direct')
inputChannel.exchange_declare(exchange='Goodwin',type='direct')

result = inputChannel.queue_declare(exclusive=True)
queueName = result.method.queue
exchangeName = result.method.exchange

def callback(ch, method, properties, body): 
    print(" [x] %r:%r" % (method.routing_key, body))

inputChannel.queue_bind(exchange=exchangeName,queue=queue_name,routing_key=queueName)

print(' [*] Waiting for logs. To exit press CTRL+C')

inputChannel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()