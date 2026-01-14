import pika
from decouple import config
from typing import Callable
import json


class EventBus:
    """Event Bus simples com RabbitMQ"""
    
    def __init__(self):
        self.connection = None
        self.channel = None
    
    def connect(self):
        credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq_dev_password')
        parameters = pika.ConnectionParameters(
            host=config('RABBITMQ_HOST', default='rabbitmq'),
            port=config('RABBITMQ_PORT', default=5672, cast=int),
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
    
    def publish(self, event_name: str, event_data: dict):
        if not self.channel:
            self.connect()
        
        self.channel.queue_declare(queue=event_name, durable=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=event_name,
            body=json.dumps(event_data),
            properties=pika.BasicProperties(delivery_mode=2)
        )
    
    def subscribe(self, event_name: str, callback: Callable):
        if not self.channel:
            self.connect()
        
        self.channel.queue_declare(queue=event_name, durable=True)
        
        def wrapper(ch, method, properties, body):
            data = json.loads(body)
            callback(data)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        self.channel.basic_consume(queue=event_name, on_message_callback=wrapper)
        self.channel.start_consuming()
    
    def close(self):
        if self.connection:
            self.connection.close()
