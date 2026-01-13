from typing import Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy import select
import uuid

class SuporteAgentService:
    def __init__(self, db_session, gemini_service):
        self.db = db_session
        self.gemini = gemini_service
        self.system_prompt = """Você é um agente de suporte técnico especializado em sistemas de energia solar.
        
Suas responsabilidades:
1. Criar tickets para problemas reportados
2. Verificar status de garantia
3. Diagnosticar problemas com inversores
4. Orientar sobre manutenção preventiva
5. Escalar casos complexos para técnicos

Sempre seja educado, técnico e objetivo."""

    async def process_message(self, phone: str, message: str) -> Dict:
        from ..database.models import ConversationModel, MessageModel, TicketModel
        
        # Buscar ou criar conversa
        result = await self.db.execute(
            select(ConversationModel).where(
                ConversationModel.phone == phone,
                ConversationModel.agent_type == "suporte"
            )
        )
        conv = result.scalar_one_or_none()
        
        if not conv:
            conv = ConversationModel(
                phone=phone,
                agent_type="suporte",
                context_json={"stage": "initial"}
            )
            self.db.add(conv)
            await self.db.commit()
            await self.db.refresh(conv)
        
        # Salvar mensagem do usuário
        user_msg = MessageModel(
            conversation_id=conv.id,
            role="user",
            content=message
        )
        self.db.add(user_msg)
        await self.db.commit()
        
        # Buscar histórico
        result = await self.db.execute(
            select(MessageModel).where(
                MessageModel.conversation_id == conv.id
            ).order_by(MessageModel.created_at.desc()).limit(10)
        )
        history = result.scalars().all()
        
        # Gerar resposta
        context = self._build_context(conv, history)
        response = await self.gemini.generate(
            prompt=message,
            system_prompt=self.system_prompt,
            context=context
        )
        
        # Verificar se deve criar ticket
        if self._should_create_ticket(message, response):
            ticket = await self._create_ticket(phone, message, conv)
            response += f"\n\n✅ Ticket #{ticket.ticket_number} criado com sucesso!"
        
        # Salvar resposta
        bot_msg = MessageModel(
            conversation_id=conv.id,
            role="assistant",
            content=response
        )
        self.db.add(bot_msg)
        await self.db.commit()
        
        return {"text": response, "conversation_id": str(conv.id)}
    
    def _build_context(self, conv, history) -> str:
        ctx = f"Histórico da conversa:\n"
        for msg in reversed(history):
            ctx += f"{msg.role}: {msg.content}\n"
        return ctx
    
    def _should_create_ticket(self, message: str, response: str) -> bool:
        keywords = ["problema", "defeito", "não funciona", "parou", "erro", "falha"]
        return any(k in message.lower() for k in keywords)
    
    async def _create_ticket(self, phone: str, description: str, conv) -> "TicketModel":
        from ..database.models import TicketModel
        
        ticket_number = f"SUP-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        
        ticket = TicketModel(
            ticket_number=ticket_number,
            phone=phone,
            status="open",
            priority="normal",
            subject="Suporte técnico",
            description=description,
            data={"conversation_id": str(conv.id)}
        )
        self.db.add(ticket)
        await self.db.commit()
        await self.db.refresh(ticket)
        
        return ticket
    
    async def get_metrics(self) -> Dict:
        from ..database.models import TicketModel, ConversationModel
        from sqlalchemy import select, func
        
        result = await self.db.execute(select(func.count()).select_from(TicketModel))
        total_tickets = result.scalar() or 0
        
        result = await self.db.execute(
            select(func.count()).select_from(TicketModel).where(TicketModel.status == "open")
        )
        open_tickets = result.scalar() or 0
        
        result = await self.db.execute(
            select(func.count()).select_from(TicketModel).where(TicketModel.status == "resolved")
        )
        resolved_tickets = result.scalar() or 0
        
        # Calcular SLA médio
        result = await self.db.execute(
            select(TicketModel).where(TicketModel.resolved_at.isnot(None))
        )
        resolved = result.scalars().all()
        
        avg_sla_hours = 0
        if resolved:
            total_hours = sum([
                (t.resolved_at - t.created_at).total_seconds() / 3600
                for t in resolved
            ])
            avg_sla_hours = total_hours / len(resolved)
        
        result = await self.db.execute(
            select(func.count()).select_from(ConversationModel).where(
                ConversationModel.agent_type == "suporte"
            )
        )
        active_conversations = result.scalar() or 0
        
        return {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "resolved_tickets": resolved_tickets,
            "avg_sla_hours": round(avg_sla_hours, 2),
            "active_conversations": active_conversations
        }
