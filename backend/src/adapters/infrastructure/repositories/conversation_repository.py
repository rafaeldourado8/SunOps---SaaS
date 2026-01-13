from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime

from ..database.models.conversation import Conversation, Message


class ConversationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_or_create_conversation(self, phone: str, agent_type: str) -> Conversation:
        """Get existing conversation or create new one"""
        result = await self.session.execute(
            select(Conversation)
            .where(Conversation.phone == phone, Conversation.agent_type == agent_type)
            .order_by(desc(Conversation.updated_at))
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            conversation = Conversation(phone=phone, agent_type=agent_type, context_json={})
            self.session.add(conversation)
            await self.session.commit()
            await self.session.refresh(conversation)
        
        return conversation
    
    async def add_message(self, conversation_id: UUID, role: str, content: str) -> Message:
        """Add message to conversation"""
        message = Message(conversation_id=conversation_id, role=role, content=content)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message
    
    async def get_messages(self, conversation_id: UUID, limit: int = 10) -> List[Message]:
        """Get recent messages from conversation"""
        result = await self.session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
        )
        return list(reversed(result.scalars().all()))
    
    async def update_context(self, conversation_id: UUID, context: dict) -> None:
        """Update conversation context"""
        result = await self.session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one()
        conversation.context_json = context
        conversation.updated_at = datetime.utcnow()
        await self.session.commit()
