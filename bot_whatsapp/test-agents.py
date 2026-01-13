"""
Script de teste para validar integração dos agentes IA
"""
import pika
import json
import time


def test_vendas_agent():
    """Testa bot de vendas"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Mensagem de teste
    message = {
        'id': 'test_001',
        'from': '5511999999999@c.us',
        'to': '5511888888888@c.us',
        'body': 'Olá, gostaria de um orçamento para energia solar',
        'timestamp': int(time.time()),
        'hasMedia': False,
        'type': 'chat',
        'contact': {
            'name': 'João Teste',
            'number': '5511999999999'
        }
    }
    
    # Publicar mensagem
    channel.basic_publish(
        exchange='',
        routing_key='whatsapp_messages',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    
    print('✅ Mensagem de VENDAS publicada')
    print(f'   Cliente: {message["contact"]["name"]}')
    print(f'   Mensagem: {message["body"]}')
    
    connection.close()


def test_suporte_agent():
    """Testa bot de suporte"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Mensagem de teste
    message = {
        'id': 'test_002',
        'from': '5511888888888@c.us',
        'to': '5511999999999@c.us',
        'body': 'Meu inversor está offline há 3 dias, pode me ajudar?',
        'timestamp': int(time.time()),
        'hasMedia': False,
        'type': 'chat',
        'contact': {
            'name': 'Maria Teste',
            'number': '5511888888888'
        }
    }
    
    # Publicar mensagem
    channel.basic_publish(
        exchange='',
        routing_key='whatsapp_messages',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    
    print('✅ Mensagem de SUPORTE publicada')
    print(f'   Cliente: {message["contact"]["name"]}')
    print(f'   Mensagem: {message["body"]}')
    
    connection.close()


def monitor_responses():
    """Monitora respostas dos agentes"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='whatsapp_responses', durable=True)
    
    print('\n👂 Aguardando respostas dos agentes...\n')
    
    def callback(ch, method, properties, body):
        response = json.loads(body)
        print(f'📤 Resposta recebida:')
        print(f'   Para: {response["to"]}')
        print(f'   Texto: {response["text"][:100]}...')
        print(f'   Typing: {response.get("typing", 0)}ms\n')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_consume(
        queue='whatsapp_responses',
        on_message_callback=callback
    )
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('\n🛑 Monitoramento encerrado')
        connection.close()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print('Uso:')
        print('  python test-agents.py vendas    # Testa bot de vendas')
        print('  python test-agents.py suporte   # Testa bot de suporte')
        print('  python test-agents.py monitor   # Monitora respostas')
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'vendas':
        test_vendas_agent()
    elif command == 'suporte':
        test_suporte_agent()
    elif command == 'monitor':
        monitor_responses()
    else:
        print(f'❌ Comando inválido: {command}')
