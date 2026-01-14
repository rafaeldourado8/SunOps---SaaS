"""
Router Dashboard com SSE
"""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json
from datetime import datetime

router = APIRouter()


async def dashboard_event_generator():
    """Gerador de eventos SSE para dashboard"""
    while True:
        # Simula métricas (em produção, buscar do banco)
        data = {
            "timestamp": datetime.now().isoformat(),
            "total_orcamentos": 10,
            "valor_total": 150000.00,
            "taxa_conversao": 35.5,
            "orcamentos_mes": 8
        }
        
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(5)  # Atualiza a cada 5 segundos


@router.get("/stream")
async def dashboard_stream():
    """Endpoint SSE para dashboard em tempo real"""
    return StreamingResponse(
        dashboard_event_generator(),
        media_type="text/event-stream"
    )


@router.get("/metrics")
async def dashboard_metrics():
    """Endpoint REST para métricas"""
    return {
        "total_orcamentos": 10,
        "valor_total": 150000.00,
        "taxa_conversao": 35.5,
        "orcamentos_mes": 8
    }
