import pika
import json
import os
import logging
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class MessageBroker:
    def __init__(self):
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None
        try:
            self._connect()
        except Exception as e:
            logger.warning(f"Failed to connect to RabbitMQ: {e}. Running without message broker.")
    
    def _connect(self):
        rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
        parameters = pika.URLParameters(rabbitmq_url)
        parameters.connection_attempts = 3
        parameters.retry_delay = 2
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        logger.info("Connected to RabbitMQ successfully")
    
    def publish(self, queue: str, message: dict):
        if not self.channel:
            logger.warning(f"Cannot publish to {queue}: No connection to RabbitMQ")
            return
        
        try:
            self.channel.queue_declare(queue=queue, durable=True)
            self.channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)
            )
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
    
    def consume(self, queue: str, callback: Callable):
        if not self.channel:
            logger.error("Cannot consume: No connection to RabbitMQ")
            return
        
        self.channel.queue_declare(queue=queue, durable=True)
        
        def wrapper(ch, method, properties, body):
            message = json.loads(body)
            callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        self.channel.basic_consume(queue=queue, on_message_callback=wrapper)
        self.channel.start_consuming()
    
    def close(self):
        if self.connection:
            self.connection.close()


broker = MessageBroker()
