from typing import Dict, Any
from datetime import datetime, timedelta
from .base import BaseAgent
from ..services.gemini import GeminiService
from ..services.cache import CacheService


class SuporteAgent(BaseAgent):
    """Agente de Suporte Técnico IA"""
    
    RULES = """
1. NUNCA invente diagnósticos ou soluções
2. Seja empático e paciente, especialmente com idosos
3. Use linguagem simples e analogias para explicar termos técnicos
4. Gere ticket único para cada atendimento
5. Aguarde 2 dias antes de notificar cliente sobre falhas
6. Em erros internos, não declare culpa diretamente
7. Se não conseguir resolver remotamente, escale para administrador
8. Ensine o uso dos apps de monitoramento com paciência
"""
    
    def __init__(self, gemini: GeminiService, cache: CacheService):
        super().__init__("suporte")
        self.gemini = gemini
        self.cache = cache
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagem do cliente"""
        body = message['body']
        contact = message['contact']
        
        # 1. Preprocessamento
        intent_data = await self.gemini.preprocess_with_flash(body, self.context)
        
        # 2. Verificar se é sobre falha de inversor
        if 'inversor' in body.lower() or 'offline' in body.lower():
            return await self._handle_inverter_issue(message, intent_data)
        
        # 3. Verificar se é sobre garantia
        if 'garantia' in body.lower():
            return await self._handle_warranty(message)
        
        # 4. Resposta geral de suporte
        response_text = await self.gemini.generate_response_with_pro(
            body, self.context, self.RULES, "suporte técnico"
        )
        
        return {
            'to': message['from'],
            'text': response_text,
            'typing': min(len(response_text) * 30, 5000)
        }
    
    async def should_transfer_to_human(self, message: Dict[str, Any]) -> bool:
        """Verifica se deve transferir para humano"""
        keywords = ['não consigo', 'não funciona', 'urgente', 'técnico presencial']
        body_lower = message['body'].lower()
        return any(keyword in body_lower for keyword in keywords)
    
    async def _handle_inverter_issue(self, message: Dict[str, Any], intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trata problemas com inversores"""
        # Verificar se já passou 2 dias
        last_check = self.get_context('inverter_offline_since')
        if last_check:
            days_offline = (datetime.now() - datetime.fromisoformat(last_check)).days
            if days_offline < 2:
                return {
                    'to': message['from'],
                    'text': 'Estou monitorando seu sistema. Vou aguardar mais um pouco antes de tomar ações, pois pode ser uma oscilação temporária.',
                    'typing': 3000
                }
        else:
            self.update_context('inverter_offline_since', datetime.now().isoformat())
        
        # Pesquisar sobre a falha
        error_code = intent_data.get('entities', {}).get('error_code')
        diagnosis = await self._diagnose_inverter_error(error_code)
        
        return {
            'to': message['from'],
            'text': f"Identifiquei o problema: {diagnosis['cause']}\n\nSolução sugerida: {diagnosis['solution']}\n\nPosso te ajudar a resolver isso remotamente?",
            'typing': 4000,
            'requires_admin_approval': True
        }
    
    async def _diagnose_inverter_error(self, error_code: str) -> Dict[str, Any]:
        """Diagnostica erro do inversor"""
        # TODO: Integrar com APIs de monitoramento (SolisCloud, Growatt, Solarman)
        return {
            'cause': 'Possível problema de comunicação com a rede',
            'solution': 'Reiniciar o inversor e verificar conexão Wi-Fi'
        }
    
    async def _handle_warranty(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Trata solicitações de garantia"""
        ticket_id = await self._create_ticket(message)
        link = f"https://sunops.com.br/garantia/{ticket_id}"
        
        return {
            'to': message['from'],
            'text': f"Abri o ticket {ticket_id} para sua solicitação de garantia.\n\nAcompanhe pelo link: {link}\n\nVou manter você informado sobre o andamento.",
            'typing': 3000
        }
    
    async def _create_ticket(self, message: Dict[str, Any]) -> str:
        """Cria ticket de suporte"""
        # TODO: Persistir no banco
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"TKT-{timestamp}"
    
    async def monitor_inverters(self):
        """Monitora inversores em tempo real (background task)"""
        # TODO: Implementar streaming de eventos das APIs
        pass
