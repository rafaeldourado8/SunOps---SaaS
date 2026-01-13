import os
import asyncio
from dotenv import load_dotenv
from .consumers.whatsapp import WhatsAppConsumer

load_dotenv()


async def main():
    """Entry point para o consumidor de WhatsApp"""
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672')
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    consumer = WhatsAppConsumer(rabbitmq_url, redis_url)
    
    print('🚀 Iniciando WhatsApp AI Agent Consumer...')
    await consumer.start()


if __name__ == '__main__':
    asyncio.run(main())
