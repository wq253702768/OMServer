#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/22 15:51
# @Author  : Py.qi
# @File    : rabbitMQ_send_1.py
# @Software: PyCharm

import pika,sys
print('send....start....')
while True:
    inputso=input('soinsideto:')
    if inputso == 'quit':
        break
    username = 'admin'
    pwd = '5nkxg50axrjlrjvt'
    user_pwd = pika.PlainCredentials(username, pwd)
#与RabbitMQ服务器建立链接
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.97.52',credentials=user_pwd))
#建立隧道
    channel = connection.channel()
#创建队列名称zhang
    channel.queue_declare(queue='zhang')
#发送信息：exchange指定交换，routing_key指定队列名，body指定消息内容
    channel.basic_publish(exchange='',routing_key='zhang',body=inputso)
#关闭链接
    connection.close()
