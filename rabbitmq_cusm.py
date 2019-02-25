#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/22 15:57
# @Author  : Py.qi
# @File    : rabbitMQ_rescv_1.py
# @Software: PyCharm

import pika
username = 'admin'
pwd = '5nkxg50axrjlrjvt'
user_pwd = pika.PlainCredentials(username, pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.97.52',credentials=user_pwd))

channel = connection.channel()
channel.queue_declare(queue='hehe',durable=True)


def callback(ch,method,properties,body):
    print('recived:',body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1) #确认发送消息个数
channel.basic_consume(callback,queue='hehe',no_ack=True)
print('waiting for message,to exit press ctrl+c')
channel.start_consuming()