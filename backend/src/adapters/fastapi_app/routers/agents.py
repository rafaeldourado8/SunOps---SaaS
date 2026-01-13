from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Dict, Any

from ...infrastructure.database.config import AsyncSessionLocal
from ...infrastructure.repositories.conversation_repository import ConversationRepository
from ...infrastructure.services.vendas_agent_service import VendasAgentService
from ...infrastructure.services.suporte_agent_service import SuporteAgentService

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])


class MessageRequest(BaseModel):
    phone: str
    message: str


class ConfigRequest(BaseModel):
    config: Dict[str, Any]


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/vendas/message")
async def process_vendas_message(
    request: MessageRequest,
    db: AsyncSession = Depends(get_db)
):
    """Process message for sales agent"""
    conversation_repo = ConversationRepository(db)
    vendas_service = VendasAgentService(conversation_repo)
    
    response = await vendas_service.process_message(request.phone, request.message)
    return response


@router.post("/vendas/config")
async def configure_vendas_agent(config: ConfigRequest):
    """Configure sales agent"""
    return {
        "message": "Configuração salva com sucesso",
        "config": config.config
    }


@router.get("/vendas/metrics")
async def get_vendas_metrics(db: AsyncSession = Depends(get_db)):
    """Get sales agent metrics"""
    conversation_repo = ConversationRepository(db)
    vendas_service = VendasAgentService(conversation_repo)
    
    metrics = await vendas_service.get_metrics()
    return metrics


@router.post("/suporte/message")
async def process_suporte_message(
    request: MessageRequest,
    db: AsyncSession = Depends(get_db)
):
    """Process message for support agent"""
    from ...whatsapp_agent.services.gemini import GeminiService
    
    gemini = GeminiService()
    suporte_service = SuporteAgentService(db, gemini)
    
    response = await suporte_service.process_message(request.phone, request.message)
    return response


@router.post("/suporte/config")
async def configure_suporte_agent(config: ConfigRequest):
    """Configure support agent"""
    return {
        "message": "Configuração salva com sucesso",
        "config": config.config
    }


@router.get("/suporte/metrics")
async def get_suporte_metrics(db: AsyncSession = Depends(get_db)):
    """Get support agent metrics"""
    from ...whatsapp_agent.services.gemini import GeminiService
    
    gemini = GeminiService()
    suporte_service = SuporteAgentService(db, gemini)
    
    metrics = await suporte_service.get_metrics()
    return metrics


@router.get("/tickets")
async def list_tickets(db: AsyncSession = Depends(get_db)):
    """List all tickets"""
    from ...infrastructure.database.models import TicketModel
    from sqlalchemy import select
    
    result = await db.execute(
        select(TicketModel).order_by(TicketModel.created_at.desc()).limit(50)
    )
    tickets = result.scalars().all()
    
    return {
        "tickets": [
            {
                "id": str(t.id),
                "ticket_number": t.ticket_number,
                "phone": t.phone,
                "status": t.status,
                "priority": t.priority,
                "subject": t.subject,
                "created_at": t.created_at.isoformat(),
                "resolved_at": t.resolved_at.isoformat() if t.resolved_at else None
            }
            for t in tickets
        ]
    }
