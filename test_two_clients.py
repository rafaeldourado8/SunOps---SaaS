"""Teste com 2 clientes simultâneos."""
import asyncio
import json
import websockets


async def test_two_clients():
    print("🧪 Teste: 2 Clientes Simultâneos\n")
    
    conversa_id = None
    
    async def vendedor():
        nonlocal conversa_id
        async with websockets.connect("ws://localhost:8001/ws/chat/vendedor-1") as ws:
            print("✅ VENDEDOR conectado")
            
            # Criar conversa
            await ws.send(json.dumps({"action": "create_conversa"}))
            resp = json.loads(await ws.recv())
            conversa_id = resp["conversa_id"]
            print(f"📝 Conversa criada: {conversa_id}")
            
            # Entrar
            await ws.send(json.dumps({"action": "join_room", "conversa_id": conversa_id}))
            await ws.recv()
            
            # Enviar mensagem
            await ws.send(json.dumps({
                "action": "send_message",
                "conversa_id": conversa_id,
                "conteudo": "Preciso de orçamento para 500 kWh",
                "tipo_remetente": "VENDEDOR"
            }))
            msg = json.loads(await ws.recv())
            print(f"💬 VENDEDOR enviou: {msg['conteudo']}")
            
            # Aguardar resposta
            print("⏳ Aguardando admin...")
            msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=5))
            print(f"📨 VENDEDOR recebeu: {msg['conteudo']}")
    
    async def admin():
        await asyncio.sleep(1)  # Aguarda conversa ser criada
        async with websockets.connect("ws://localhost:8001/ws/chat/admin-1") as ws:
            print("✅ ADMIN conectado")
            
            # Entrar
            await ws.send(json.dumps({"action": "join_room", "conversa_id": conversa_id}))
            await ws.recv()
            
            # Receber mensagem do vendedor
            msg = json.loads(await ws.recv())
            print(f"📨 ADMIN recebeu: {msg['conteudo']}")
            
            # Responder
            await ws.send(json.dumps({
                "action": "send_message",
                "conversa_id": conversa_id,
                "conteudo": "Vou preparar um kit de 5kWp para você!",
                "tipo_remetente": "ADMIN"
            }))
            msg = json.loads(await ws.recv())
            print(f"💬 ADMIN enviou: {msg['conteudo']}")
    
    try:
        await asyncio.gather(vendedor(), admin())
        print("\n✅ Teste concluído com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")


asyncio.run(test_two_clients())
