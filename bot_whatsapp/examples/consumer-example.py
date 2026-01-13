"""
Exemplo de consumidor Python para integração com FastAPI AI Agents
Este script demonstra como consumir mensagens do WhatsApp e enviar respostas
"""

import pika
import json
import time

# Configuração RabbitMQ
RABBITMQ_URL = 'amqp://guest:guest@localhost:5672'
INPUT_QUEUE = 'whatsapp_messages'
OUTPUT_QUEUE = 'whatsapp_responses'


def process_message(message_data):
    """
    Simula processamento com AI Agent
    Na implementação real, aqui você chamaria:
    - Gemini Flash para preprocessamento
    - Redis para cache
    - Gemini Pro para resposta final
    """
    contact_name = message_data['contact']['name']
    body = message_data['body']
    
    print(f"\n📩 Processando mensagem de {contact_name}: {body}")
    
    # Simular processamento (substituir por lógica real)
    time.sleep(1)
    
    # Gerar resposta
    response = {
        'to': message_data['from'],
        'text': f"Olá {contact_name}! Recebi sua mensagem: '{body}'\n\nEsta é uma resposta automática de teste.",
        'typing': 3000  # 3 segundos de "digitando..."
    }
    
    return response


def callback(ch, method, properties, body):
    """Callback executado quando uma mensagem é recebida"""
    try:
        # Parse da mensagem
        message_data = json.loads(body)
        
        # Processar com AI Agent
        response = process_message(message_data)
        
        # Publicar resposta
        ch.basic_publish(
            exchange='',
            routing_key=OUTPUT_QUEUE,
            body=json.dumps(response),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Mensagem persistente
            )
        )
        
        print(f"✅ Resposta enviada para {message_data['contact']['name']}")
        
        # Confirmar processamento
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")
        # Rejeitar mensagem (volta para a fila)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def main():
    """Inicializa o consumidor"""
    print("🚀 Iniciando consumidor Python...\n")
    
    try:
        # Conectar ao RabbitMQ
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()
        
        # Declarar filas
        channel.queue_declare(queue=INPUT_QUEUE, durable=True)
        channel.queue_declare(queue=OUTPUT_QUEUE, durable=True)
        
        # Configurar QoS (processar 1 mensagem por vez)
        channel.basic_qos(prefetch_count=1)
        
        # Consumir mensagens
        channel.basic_consume(
            queue=INPUT_QUEUE,
            on_message_callback=callback
        )
        
        print(f"✅ Consumidor conectado à fila '{INPUT_QUEUE}'")
        print("⏳ Aguardando mensagens... (Ctrl+C para sair)\n")
        
        channel.start_consuming()
        
    except KeyboardInterrupt:
        print("\n🛑 Encerrando consumidor...")
        connection.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("\n💡 Certifique-se de que o RabbitMQ está rodando:")
        print("   docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management")


if __name__ == '__main__':
    main()
