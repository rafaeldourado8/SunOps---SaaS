"""Teste automatizado do chat WebSocket."""
import asyncio
import json
from datetime import datetime


async def simulate_chat():
    """Simula troca de mensagens entre vendedor e admin."""
    try:
        import websockets
    except ImportError:
        print("❌ websockets não instalado. Instale com: pip install websockets")
        return
    
    print("🧪 Teste Automatizado - Chat WebSocket")
    print("=" * 50)
    print()
    
    conversa_id = f"conv-test-{datetime.now().strftime('%H%M%S')}"
    
    # Simula vendedor
    async def vendedor_client():
        uri = "ws://localhost:8001/ws/chat/vendedor-1"
        
        try:
            async with websockets.connect(uri) as ws:
                print("✅ VENDEDOR conectado")
                
                # Criar conversa
                await ws.send(json.dumps({
                    "action": "create_conversa",
                    "assunto": "Orçamento urgente"
                }))
                msg = json.loads(await ws.recv())
                print(f"📝 Conversa criada: {msg.get('conversa_id')}")
                
                # Usar conversa_id global
                nonlocal conversa_id
                conversa_id = msg.get('conversa_id', conversa_id)
                
                # Entrar na sala
                await ws.send(json.dumps({
                    "action": "join_room",
                    "conversa_id": conversa_id
                }))
                await ws.recv()
                print(f"🚪 VENDEDOR entrou na sala: {conversa_id}")
                
                # Enviar mensagem
                await ws.send(json.dumps({
                    "action": "send_message",
                    "conversa_id": conversa_id,
                    "conteudo": "Olá! Preciso de um orçamento para 500 kWh/mês em São Paulo",
                    "tipo_remetente": "VENDEDOR"
                }))
                msg = json.loads(await ws.recv())
                print(f"💬 VENDEDOR: {msg.get('conteudo')}")
                
                # Aguardar resposta do admin
                print("⏳ Aguardando resposta do admin...")
                for i in range(5):
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                        data = json.loads(msg)
                        if data.get('type') == 'message' and data.get('tipo_remetente') == 'ADMIN':
                            print(f"📨 ADMIN respondeu: {data.get('conteudo')}")
                            break
                    except asyncio.TimeoutError:
                        if i == 4:
                            print("⏰ Timeout - Admin não respondeu")
        
        except Exception as e:
            print(f"❌ Erro no vendedor: {e}")
    
    # Simula admin
    async def admin_client():
        await asyncio.sleep(1)  # Aguarda vendedor criar conversa
        
        uri = "ws://localhost:8001/ws/chat/admin-1"
        
        try:
            async with websockets.connect(uri) as ws:
                print("✅ ADMIN conectado")
                
                # Entrar na sala
                await ws.send(json.dumps({
                    "action": "join_room",
                    "conversa_id": conversa_id
                }))
                await ws.recv()
                print(f"🚪 ADMIN entrou na sala: {conversa_id}")
                
                # Aguardar mensagem do vendedor
                msg = json.loads(await ws.recv())
                if msg.get('type') == 'message':
                    print(f"📨 ADMIN recebeu: {msg.get('conteudo')}")
                
                # Responder
                await asyncio.sleep(0.5)
                await ws.send(json.dumps({
                    "action": "send_message",
                    "conversa_id": conversa_id,
                    "conteudo": "Perfeito! Vou preparar um orçamento de 5kWp para você",
                    "tipo_remetente": "ADMIN"
                }))
                msg = json.loads(await ws.recv())
                print(f"💬 ADMIN: {msg.get('conteudo')}")
        
        except Exception as e:
            print(f"❌ Erro no admin: {e}")
    
    # Executar ambos simultaneamente
    await asyncio.gather(
        vendedor_client(),
        admin_client()
    )
    
    print()
    print("=" * 50)
    print("✅ Teste concluído!")
    print()
    print("📊 Verificar conversas:")
    print(f"   curl 'http://localhost:8001/api/chat/conversas?user_id=vendedor-1&tipo=vendedor'")
    print()
    print("📨 Verificar mensagens:")
    print(f"   curl 'http://localhost:8001/api/chat/conversas/{conversa_id}/mensagens'")


if __name__ == "__main__":
    asyncio.run(simulate_chat())
