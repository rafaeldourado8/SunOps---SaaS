import asyncio
import json
import pika
from typing import Dict, Any
from ..agents.vendas import VendasAgent
from ..agents.suporte import SuporteAgent
from ..services.gemini import GeminiService
from ..services.cache import CacheService


class WhatsAppConsumer:
    """Consumidor de mensagens do WhatsApp via RabbitMQ"""
    
    def __init__(self, rabbitmq_url: str, redis_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.gemini = GeminiService()
        self.cache = CacheService(redis_url)
        
        # Agentes
        self.vendas_agent = VendasAgent(self.gemini, self.cache)
        self.suporte_agent = SuporteAgent(self.gemini, self.cache)
        
        # Sessões ativas (cliente_id -> agent)
        self.sessions: Dict[str, Any] = {}
    
    async def start(self):
        """Inicia consumidor"""
        connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
        channel = connection.channel()
        
        channel.queue_declare(queue='whatsapp_messages', durable=True)
        channel.queue_declare(queue='whatsapp_responses', durable=True)
        
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue='whatsapp_messages',
            on_message_callback=self._callback
        )
        
        print('✅ WhatsApp Consumer iniciado')
        channel.start_consuming()
    
    def _callback(self, ch, method, properties, body):
        """Callback para processar mensagem"""
        try:
            message = json.loads(body)
            response = asyncio.run(self._process_message(message))
            
            # Publicar resposta
            ch.basic_publish(
                exchange='',
                routing_key='whatsapp_responses',
                body=json.dumps(response),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"✅ Mensagem processada: {message['contact']['name']}")
            
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    async def _process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagem e roteia para agente correto"""
        client_id = message['from']
        
        # Recuperar ou criar sessão
        if client_id not in self.sessions:
            agent = await self._classify_intent(message)
            self.sessions[client_id] = agent
        
        agent = self.sessions[client_id]
        
        # Processar com agente
        response = await agent.process_message(message)
        
        # Verificar transferência para humano
        if response.get('transfer_to_human'):
            del self.sessions[client_id]
        
        return response
    
    async def _classify_intent(self, message: Dict[str, Any]) -> Any:
        """Classifica intent inicial e retorna agente apropriado"""
        body_lower = message['body'].lower()
        
        # Keywords para suporte
        suporte_keywords = ['problema', 'defeito', 'garantia', 'inversor', 'offline', 'não funciona']
        if any(keyword in body_lower for keyword in suporte_keywords):
            return self.suporte_agent
        
        # Default: vendas
        return self.vendas_agent
