"""Teste simples do chat."""
import asyncio
import json
import websockets


async def test_simple():
    print("🧪 Teste Chat WebSocket\n")
    
    # Teste 1: Vendedor cria conversa
    print("1️⃣ Vendedor conectando...")
    async with websockets.connect("ws://localhost:8001/ws/chat/vendedor-1") as ws:
        print("✅ Conectado")
        
        # Criar conversa
        await ws.send(json.dumps({"action": "create_conversa", "assunto": "Teste"}))
        resp = json.loads(await ws.recv())
        conversa_id = resp.get("conversa_id")
        print(f"📝 Conversa: {conversa_id}")
        
        # Entrar na sala
        await ws.send(json.dumps({"action": "join_room", "conversa_id": conversa_id}))
        await ws.recv()
        print("🚪 Entrou na sala")
        
        # Enviar mensagem
        await ws.send(json.dumps({
            "action": "send_message",
            "conversa_id": conversa_id,
            "conteudo": "Olá, preciso de ajuda!",
            "tipo_remetente": "VENDEDOR"
        }))
        resp = json.loads(await ws.recv())
        print(f"💬 Enviou: {resp.get('conteudo')}")
    
    print("\n✅ Teste concluído!")
    print(f"\n📊 Ver mensagens: curl 'http://localhost:8001/api/chat/conversas/{conversa_id}/mensagens'")


asyncio.run(test_simple())
