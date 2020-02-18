import sys
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import pika
import urllib.request
import codecs

from Tools.scripts.dutree import display
from numpy import save

credentials = pika.PlainCredentials('SGSim', '1234')
connection = pika.BlockingConnection(pika.ConnectionParameters('210.102.181.143', 2001, 'test', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='test', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
print(queue_name)

channel.queue_bind(
    exchange='test', queue=queue_name, routing_key='KEY')

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r:%r:%r" % (method.routing_key, body, ch, properties))
    df = pd.DataFrame(data=np.array([[0, 0, 0, body],
                                     [0, 0, 0, body],
                                     [1, 1, 1, body],
                                     [2, 2, 2, body],
                                     [3, 3, 3, body],
                                     [4, 4, 4, body]]),
                      columns=['ID', 'NODE', 'Power Gen', 'routing_key'])

    print(df.index[1])
    print(df.drop(df.index[1]))
    print(df.drop(0))



print('*****************************************************************************')


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
