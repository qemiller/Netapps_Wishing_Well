import pika

credentials = pika.PlainCredentials('mqadmin', 'mqadminpassword')
parameters = pika.ConnectionParameters('172.30.67.18', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='Goodwin',
                                 exchange_type='direct',durable=True)

result = channel.queue_declare(queue='Classrooms',durable=True)
queue_name = result.method.queue
print(queue_name)
channel.queue_bind(exchange='Goodwin',
                           queue='Classrooms')

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
        print(" [x] %r" % body)

#channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
#nonblockconnection=pika.Connection(parameters)
#nonblock_channel=nonblockconnection.channel()
#nonblock_channel.basic_get(queue=queue_name, no_ack=True)
channel.basic_get( queue='send_back', no_ack=False)
#channel.start_consuming()
