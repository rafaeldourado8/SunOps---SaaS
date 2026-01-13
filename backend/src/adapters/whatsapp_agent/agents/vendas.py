from typing import Dict, Any
from .base import BaseAgent
from ..services.gemini import GeminiService
from ..services.cache import CacheService


class VendasAgent(BaseAgent):
    """Agente de Vendas IA"""
    
    RULES = """
1. NUNCA invente informações sobre produtos ou preços
2. Mantenha o contexto de toda a conversa
3. Faça perguntas para coletar: consumo mensal (kWh), tipo de telhado, localização
4. Seja persuasivo mas honesto
5. Se não souber algo, diga que vai verificar
6. Linguagem natural e humanizada
7. Não saia do escopo de vendas de energia solar
"""
    
    def __init__(self, gemini: GeminiService, cache: CacheService):
        super().__init__("vendas")
        self.gemini = gemini
        self.cache = cache
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagem do cliente"""
        body = message['body']
        contact = message['contact']
        
        # 1. Preprocessamento com Flash
        cache_key = self.cache.generate_key("preprocess", body)
        intent_data = await self.cache.get_or_compute(
            cache_key,
            lambda: self.gemini.preprocess_with_flash(body, self.context),
            ttl=3600
        )
        
        # 2. Verificar transferência para humano
        if intent_data.get('intent') == 'transferir_humano':
            return {
                'to': message['from'],
                'text': f"Entendi, {contact['name']}. Vou transferir você para um atendente humano. Um momento, por favor.",
                'typing': 2000,
                'transfer_to_human': True
            }
        
        # 3. Atualizar contexto
        self.update_context('last_intent', intent_data.get('intent'))
        self.update_context('urgency', intent_data.get('urgency'))
        
        # 4. Gerar resposta com Pro
        cache_key = self.cache.generate_key("response", body, str(self.context))
        response_text = await self.cache.get_or_compute(
            cache_key,
            lambda: self.gemini.generate_response_with_pro(
                body, self.context, self.RULES, "vendas"
            ),
            ttl=1800
        )
        
        return {
            'to': message['from'],
            'text': response_text,
            'typing': min(len(response_text) * 30, 5000)  # Simular digitação
        }
    
    async def should_transfer_to_human(self, message: Dict[str, Any]) -> bool:
        """Verifica se deve transferir para humano"""
        keywords = ['falar com humano', 'atendente', 'pessoa real', 'gerente']
        body_lower = message['body'].lower()
        return any(keyword in body_lower for keyword in keywords)
    
    async def generate_orcamento(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Gera orçamento baseado nos dados coletados"""
        # TODO: Integrar com use case CriarOrcamento
        return {
            'orcamento_id': 'ORC-2024-0001',
            'valor_total': 25000.00,
            'kit_recomendado': 'Kit 5.4kWp',
            'pdf_url': '/orcamentos/ORC-2024-0001.pdf'
        }
