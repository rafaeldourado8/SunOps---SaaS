"""Teste do chat WebSocket."""
import asyncio
import websockets
import json


async def test_vendedor():
    """Simula vendedor."""
    uri = "ws://localhost:8001/ws/chat/vendedor-1"
    
    async with websockets.connect(uri) as websocket:
        print("✅ Vendedor conectado")
        
        # Criar conversa
        await websocket.send(json.dumps({
            "action": "create_conversa",
            "assunto": "Preciso de orçamento"
        }))
        
        response = await websocket.recv()
        data = json.loads(response)
        print(f"📝 Conversa criada: {data}")
        
        conversa_id = data.get("conversa_id")
        
        # Entrar na sala
        await websocket.send(json.dumps({
            "action": "join_room",
            "conversa_id": conversa_id
        }))
        
        response = await websocket.recv()
        print(f"🚪 Entrou na sala: {json.loads(response)}")
        
        # Enviar mensagem
        await websocket.send(json.dumps({
            "action": "send_message",
            "conversa_id": conversa_id,
            "conteudo": "Olá! Preciso de um orçamento para 500 kWh/mês",
            "tipo_remetente": "VENDEDOR"
        }))
        
        response = await websocket.recv()
        print(f"💬 Mensagem enviada: {json.loads(response)}")
        
        # Aguardar resposta
        print("⏳ Aguardando resposta do admin...")
        for _ in range(3):
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                print(f"📨 Recebido: {json.loads(response)}")
            except asyncio.TimeoutError:
                print("⏰ Timeout aguardando mensagem")
                break


async def test_admin():
    """Simula admin."""
    await asyncio.sleep(1)  # Aguarda vendedor criar conversa
    
    uri = "ws://localhost:8001/ws/chat/admin-1"
    
    async with websockets.connect(uri) as websocket:
        print("\n✅ Admin conectado")
        
        # Usar conversa criada pelo vendedor
        conversa_id = "conv-test-123"  # Será substituído pelo real
        
        # Entrar na sala
        await websocket.send(json.dumps({
            "action": "join_room",
            "conversa_id": conversa_id
        }))
        
        response = await websocket.recv()
        print(f"🚪 Admin entrou na sala: {json.loads(response)}")
        
        # Enviar resposta
        await websocket.send(json.dumps({
            "action": "send_message",
            "conversa_id": conversa_id,
            "conteudo": "Olá! Vou preparar o orçamento para você",
            "tipo_remetente": "ADMIN"
        }))
        
        response = await websocket.recv()
        print(f"💬 Admin enviou: {json.loads(response)}")


async def main():
    """Executa teste."""
    print("🧪 Testando Chat WebSocket\n")
    
    try:
        await test_vendedor()
    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    asyncio.run(main())
