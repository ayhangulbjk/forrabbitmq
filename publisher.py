#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
pika.ConnectionParameters(host='10.220.13.31'))
channel = connection.channel()
channel.queue_declare(queue='firstqueue')
channel.basic_publish(exchange='', routing_key='firstqueue', body='Hello, this is second message!')
print(" [x] Sent 'Hello, this is second message!''")
connection.close()
