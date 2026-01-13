import pika
import redis
import json
import os
import time

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

def publish_to_redis(event_type: str, data: dict):
    """Publica evento no Redis pub/sub"""
    r = redis.from_url(REDIS_URL, decode_responses=True)
    event = {"type": event_type, "data": data, "timestamp": time.time()}
    r.publish("sunops:events", json.dumps(event))
    r.close()

def callback(ch, method, properties, body):
    """Callback RabbitMQ -> Redis"""
    try:
        message = json.loads(body)
        publish_to_redis("whatsapp_message", message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def start_consumer():
    """Inicia consumer RabbitMQ"""
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue='whatsapp_messages', durable=True)
    channel.basic_consume(queue='whatsapp_messages', on_message_callback=callback)
    print("Event consumer started...")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
