from typing import Dict, Any, Optional
from uuid import UUID
import json

from ..repositories.conversation_repository import ConversationRepository


class VendasAgentService:
    """Service for Sales Agent with context management"""
    
    SYSTEM_PROMPT = """Você é um vendedor especialista em energia solar da SunOps.

REGRAS:
1. NUNCA invente preços ou especificações técnicas
2. Mantenha contexto de toda conversa
3. Colete: consumo mensal (kWh), tipo de telhado, localização
4. Seja persuasivo mas honesto
5. Linguagem natural e humanizada
6. Não saia do escopo de energia solar

DADOS PARA COLETAR:
- Nome do cliente
- Consumo mensal em kWh (ou valor da conta)
- Tipo de telhado (cerâmica, metálico, laje)
- Localização (cidade/estado)
- Telefone para contato

Quando tiver todos os dados, informe que vai gerar o orçamento."""
    
    def __init__(self, conversation_repo: ConversationRepository, gemini_service=None):
        self.conversation_repo = conversation_repo
        self.gemini_service = gemini_service
    
    async def process_message(self, phone: str, message: str) -> Dict[str, Any]:
        """Process incoming message and generate response"""
        # Get or create conversation
        conversation = await self.conversation_repo.get_or_create_conversation(phone, "vendas")
        
        # Save user message
        await self.conversation_repo.add_message(conversation.id, "user", message)
        
        # Get conversation history
        messages = await self.conversation_repo.get_messages(conversation.id, limit=10)
        
        # Build context
        context = self._build_context(messages, conversation.context_json)
        
        # Generate response
        response = await self._generate_response(message, context)
        
        # Save assistant message
        await self.conversation_repo.add_message(conversation.id, "assistant", response["text"])
        
        # Update context if needed
        if response.get("context_update"):
            new_context = {**conversation.context_json, **response["context_update"]}
            await self.conversation_repo.update_context(conversation.id, new_context)
        
        return response
    
    def _build_context(self, messages: list, context_json: dict) -> str:
        """Build context string from messages and stored context"""
        context_parts = [self.SYSTEM_PROMPT]
        
        if context_json:
            context_parts.append(f"\nDados coletados: {json.dumps(context_json, ensure_ascii=False)}")
        
        context_parts.append("\nHistórico da conversa:")
        for msg in messages[-6:]:  # Last 6 messages
            role = "Cliente" if msg.role == "user" else "Você"
            context_parts.append(f"{role}: {msg.content}")
        
        return "\n".join(context_parts)
    
    async def _generate_response(self, message: str, context: str) -> Dict[str, Any]:
        """Generate response using Gemini or fallback logic"""
        if self.gemini_service:
            # TODO: Integrate with Gemini
            pass
        
        # Fallback logic
        message_lower = message.lower()
        
        # Check for transfer to human
        if any(word in message_lower for word in ["humano", "atendente", "pessoa", "gerente"]):
            return {
                "text": "Entendi! Vou transferir você para um atendente humano. Um momento, por favor.",
                "transfer_to_human": True
            }
        
        # Extract data from message
        context_update = {}
        
        if "kwh" in message_lower or "conta" in message_lower:
            # Try to extract consumption
            import re
            numbers = re.findall(r'\d+', message)
            if numbers:
                context_update["consumo_kwh"] = int(numbers[0])
        
        if any(word in message_lower for word in ["ceramica", "metalico", "laje", "fibrocimento"]):
            for tipo in ["cerâmica", "metálico", "laje", "fibrocimento"]:
                if tipo in message_lower:
                    context_update["tipo_telhado"] = tipo
                    break
        
        # Generate appropriate response
        if not context_update:
            response_text = "Olá! Para fazer um orçamento personalizado, preciso de algumas informações. Qual é o seu consumo mensal de energia em kWh? (Você pode ver na sua conta de luz)"
        else:
            response_text = "Ótimo! Estou anotando essas informações. "
            if "consumo_kwh" not in context_update and "tipo_telhado" in context_update:
                response_text += "Qual é o seu consumo mensal em kWh?"
            elif "tipo_telhado" not in context_update:
                response_text += "Qual é o tipo do seu telhado? (cerâmica, metálico, laje ou fibrocimento)"
            else:
                response_text += "Perfeito! Vou preparar um orçamento personalizado para você."
        
        return {
            "text": response_text,
            "context_update": context_update if context_update else None
        }
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get agent metrics"""
        # TODO: Implement real metrics from database
        return {
            "total_conversations": 0,
            "active_conversations": 0,
            "orcamentos_gerados": 0,
            "taxa_conversao": 0.0,
            "tempo_medio_resposta": 0
        }
