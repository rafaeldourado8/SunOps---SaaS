"""SSE (Server-Sent Events) para notificações em tempo real."""
import asyncio
import json
from typing import AsyncGenerator, Dict
from datetime import datetime


class SSENotificador:
    """Gerencia notificações SSE para admin."""
    
    def __init__(self):
        self.subscribers = set()
    
    async def subscribe(self) -> AsyncGenerator[str, None]:
        """Inscreve cliente para receber eventos."""
        queue = asyncio.Queue()
        self.subscribers.add(queue)
        
        try:
            while True:
                evento = await queue.get()
                yield f"data: {json.dumps(evento)}\n\n"
        finally:
            self.subscribers.remove(queue)
    
    async def notificar(self, tipo: str, dados: Dict):
        """Envia notificação para todos os inscritos."""
        evento = {
            "tipo": tipo,
            "timestamp": datetime.now().isoformat(),
            "dados": dados
        }
        
        for queue in self.subscribers:
            await queue.put(evento)
    
    async def notificar_preco_vencendo(self, produto_id: str, dias: int):
        """Notifica que preço está vencendo."""
        await self.notificar("PRECO_VENCENDO", {
            "produto_id": produto_id,
            "dias_restantes": dias,
            "urgencia": "ALTA" if dias == 0 else "MEDIA"
        })
    
    async def notificar_preco_expirado(self, produto_id: str):
        """Notifica que preço expirou."""
        await self.notificar("PRECO_EXPIRADO", {
            "produto_id": produto_id,
            "urgencia": "CRITICA"
        })
    
    async def notificar_solicitacao_campo(self, vendedor_id: str, dados: Dict):
        """Notifica solicitação do campo."""
        await self.notificar("SOLICITACAO_CAMPO", {
            "vendedor_id": vendedor_id,
            "dados": dados,
            "urgencia": "MEDIA"
        })


sse_notificador = SSENotificador()
