"""Serviço de chat com persistência."""
from datetime import datetime
from typing import List
from uuid import uuid4, UUID
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shared.infrastructure.chat.models import Conversa as ConversaModel, Mensagem as MensagemModel
from shared.domain.entities.chat import TipoRemetente, StatusMensagem


class ChatService:
    """Gerencia conversas e mensagens com persistência."""
    
    def criar_conversa(self, vendedor_id: str, assunto: str = None) -> dict:
        conversa = ConversaModel.objects.create(
            id=uuid4(),
            vendedor_id=vendedor_id,
            assunto=assunto or "Solicitação de orçamento"
        )
        return {
            "id": str(conversa.id),
            "vendedor_id": conversa.vendedor_id,
            "assunto": conversa.assunto,
            "status": conversa.status
        }
    
    def enviar_mensagem(
        self,
        conversa_id: str,
        remetente_id: str,
        tipo_remetente: str,
        conteudo: str,
        metadata: dict = None
    ) -> dict:
        try:
            conversa = ConversaModel.objects.get(id=conversa_id)
        except ConversaModel.DoesNotExist:
            raise ValueError("Conversa não encontrada")
        
        mensagem = MensagemModel.objects.create(
            id=uuid4(),
            conversa=conversa,
            remetente_id=remetente_id,
            tipo_remetente=tipo_remetente,
            conteudo=conteudo,
            metadata=metadata
        )
        
        return {
            "id": str(mensagem.id),
            "conversa_id": str(conversa.id),
            "remetente_id": mensagem.remetente_id,
            "tipo_remetente": mensagem.tipo_remetente,
            "conteudo": mensagem.conteudo,
            "timestamp": mensagem.timestamp.isoformat()
        }
    
    def marcar_como_lida(self, conversa_id: str, mensagem_id: str):
        try:
            mensagem = MensagemModel.objects.get(id=mensagem_id, conversa_id=conversa_id)
            mensagem.status = 'LIDA'
            mensagem.save()
        except MensagemModel.DoesNotExist:
            pass
    
    def listar_conversas_vendedor(self, vendedor_id: str) -> List[dict]:
        conversas = ConversaModel.objects.filter(vendedor_id=vendedor_id)
        return [
            {
                "id": str(c.id),
                "vendedor_id": c.vendedor_id,
                "admin_id": c.admin_id,
                "assunto": c.assunto,
                "status": c.status,
                "criada_em": c.criada_em.isoformat(),
                "atualizada_em": c.atualizada_em.isoformat()
            }
            for c in conversas
        ]
    
    def listar_conversas_abertas(self) -> List[dict]:
        conversas = ConversaModel.objects.filter(status='ABERTA')
        return [
            {
                "id": str(c.id),
                "vendedor_id": c.vendedor_id,
                "admin_id": c.admin_id,
                "assunto": c.assunto,
                "status": c.status,
                "criada_em": c.criada_em.isoformat(),
                "atualizada_em": c.atualizada_em.isoformat()
            }
            for c in conversas
        ]
    
    def obter_mensagens(self, conversa_id: str) -> List[dict]:
        try:
            conversa = ConversaModel.objects.get(id=conversa_id)
            mensagens = conversa.mensagens.all()
            return [
                {
                    "id": str(m.id),
                    "remetente_id": m.remetente_id,
                    "tipo_remetente": m.tipo_remetente,
                    "conteudo": m.conteudo,
                    "timestamp": m.timestamp.isoformat(),
                    "status": m.status
                }
                for m in mensagens
            ]
        except ConversaModel.DoesNotExist:
            return []


chat_service = ChatService()
