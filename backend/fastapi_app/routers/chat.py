"""Router WebSocket para chat."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from asgiref.sync import sync_to_async
from shared.infrastructure.websocket.connection_manager import manager
from shared.infrastructure.websocket.chat_service import chat_service

router = APIRouter()


@router.websocket("/ws/chat/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    """WebSocket endpoint para chat."""
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            action = data.get("action")
            
            if action == "join_room":
                conversa_id = data.get("conversa_id")
                manager.join_room(user_id, conversa_id)
                await manager.send_personal_message({
                    "type": "system",
                    "message": f"Conectado à conversa {conversa_id}"
                }, user_id)
            
            elif action == "send_message":
                conversa_id = data.get("conversa_id")
                conteudo = data.get("conteudo")
                tipo_remetente = data.get("tipo_remetente", "VENDEDOR")
                
                mensagem = await sync_to_async(chat_service.enviar_mensagem)(
                    conversa_id=conversa_id,
                    remetente_id=user_id,
                    tipo_remetente=tipo_remetente,
                    conteudo=conteudo
                )
                
                await manager.broadcast_to_room({
                    "type": "message",
                    "mensagem_id": mensagem["id"],
                    "conversa_id": conversa_id,
                    "remetente_id": user_id,
                    "tipo_remetente": tipo_remetente,
                    "conteudo": conteudo,
                    "timestamp": mensagem["timestamp"]
                }, conversa_id)
            
            elif action == "mark_read":
                conversa_id = data.get("conversa_id")
                mensagem_id = data.get("mensagem_id")
                await sync_to_async(chat_service.marcar_como_lida)(conversa_id, mensagem_id)
            
            elif action == "create_conversa":
                assunto = data.get("assunto")
                conversa = await sync_to_async(chat_service.criar_conversa)(user_id, assunto)
                
                await manager.send_personal_message({
                    "type": "conversa_created",
                    "conversa_id": conversa["id"],
                    "assunto": conversa["assunto"]
                }, user_id)
    
    except WebSocketDisconnect:
        manager.disconnect(user_id)


@router.get("/api/chat/conversas")
async def listar_conversas(user_id: str, tipo: str = "vendedor"):
    """Lista conversas do usuário."""
    if tipo == "vendedor":
        conversas = await sync_to_async(chat_service.listar_conversas_vendedor)(user_id)
    else:
        conversas = await sync_to_async(chat_service.listar_conversas_abertas)()
    
    return {"conversas": conversas}


@router.get("/api/chat/conversas/{conversa_id}/mensagens")
async def listar_mensagens(conversa_id: str):
    """Lista mensagens de uma conversa."""
    mensagens = await sync_to_async(chat_service.obter_mensagens)(conversa_id)
    
    if not mensagens:
        return {"error": "Conversa não encontrada"}
    
    return {
        "conversa_id": conversa_id,
        "mensagens": mensagens
    }


@router.post("/api/chat/conversas/{conversa_id}/atribuir")
async def atribuir_admin(conversa_id: str, admin_id: str):
    """Atribui admin a uma conversa."""
    from shared.infrastructure.chat.models import Conversa
    
    @sync_to_async
    def atribuir():
        try:
            conversa = Conversa.objects.get(id=conversa_id)
            conversa.admin_id = admin_id
            conversa.status = 'EM_ATENDIMENTO'
            conversa.save()
            return True
        except Conversa.DoesNotExist:
            return False
    
    success = await atribuir()
    
    if success:
        await manager.broadcast_to_room({
            "type": "admin_assigned",
            "conversa_id": conversa_id,
            "admin_id": admin_id
        }, conversa_id)
        return {"success": True}
    else:
        return {"error": "Conversa não encontrada"}
