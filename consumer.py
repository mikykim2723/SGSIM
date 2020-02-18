import pika
import sys

credentials = pika.PlainCredentials('SGSim', '1234')
connection = pika.BlockingConnection(pika.ConnectionParameters('210.102.181.143', 2001, 'test', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='test', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
print(queue_name)
#라우팅 키 캆 상단에 표시 하기 위해서 프린트로 
channel.queue_bind(
    exchange='test', queue=queue_name, routing_key='KEY')

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.basic_publish(exchange='test', routing_key='KEY', body=queue_name)




channel.start_consuming()
