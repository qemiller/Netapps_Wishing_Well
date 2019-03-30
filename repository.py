######### this is the repo file
import pika
import pymongo

# setup to get rabbitmq stuff ready_______________
credentials = pika.PlainCredentials('mqadmin', 'mqadminpassword')
parameters = pika.ConnectionParameters('172.30.67.18', 5672, '/',credentials)
connection = pika.BlockingConnection(parameters)
inputChannel = connection.channel()

inputChannel.exchange_declare(exchange='Squires',exchange_type='direct', durable=True)
inputChannel.exchange_declare(exchange='Library',exchange_type='direct', durable=True)
inputChannel.exchange_declare(exchange='Goodwin',exchange_type='direct', durable=True)
inputChannel.exchange_declare(exchange='Checkpoint', exchange_type='direct', durable=True)
# declare queues. Will create if none there ( i think)
inputChannel.queue_declare(queue='Food', durable=True)
inputChannel.queue_declare(queue='Meetings', durable=True)
inputChannel.queue_declare(queue='Rooms', durable=True)
inputChannel.queue_declare(queue='Classrooms', durable=True)
inputChannel.queue_declare(queue='Auditorium', durable=True)
inputChannel.queue_declare(queue='Seating', durable=True)
inputChannel.queue_declare(queue='Noise', durable=True)
inputChannel.queue_declare(queue='Wishes', durable=True)
inputChannel.queue_declare(queue='cmd', durable=True)
inputChannel.queue_declare(queue='send_back', durable=True)
# bind queues to exchanges. WILL create bindings if they don't exist already
# but causes no errors if the bindings already exist (routing_key is SAME as queue name)
inputChannel.queue_bind(exchange='Squires', queue='Food')
inputChannel.queue_bind(exchange='Squires', queue='Meetings')
inputChannel.queue_bind(exchange='Squires', queue='Rooms')
inputChannel.queue_bind(exchange='Goodwin', queue='Classrooms')
inputChannel.queue_bind(exchange='Goodwin', queue='Auditorium')
inputChannel.queue_bind(exchange='Library', queue='Seating')
inputChannel.queue_bind(exchange='Library', queue='Noise')
inputChannel.queue_bind(exchange='Library', queue='Wishes')
inputChannel.queue_bind(exchange='Checkpiont', queue='cmd')
inputChannel.queue_bind(exchange='Checkpoint', queue='send_back')
# end rabbitmq setup___________________________________


#this callback function is where we will:
# 1. wait for commands from the cmd queue
# 2. make decisions based on things we get from cmd queue
# 3. respond to 'c' commands by COMSUMING from the appropriate queue
#    and publishing the consumptions to the 'send_back' queue where the capture pi will display on monitor
# 4. every Checkpoint string we get from cmd queue we will print out to the console of repo pi
def callback(ch, method, properties, body):
    #print(" [x] %r:%r" % (method.routing_key, body))
    if body[0] == 'c':
        #need to consume from one of the place+subject queues
        #and publish the twitter message to the 'send_back' queue

    print(body[1]) # theoretically should print out the checkpoint



print(' [*] Waiting for logs. To exit press CTRL+C')

inputChannel.basic_consume(callback, queue='cmd', no_ack=True)
inputChannel.start_consuming()