"""
Test script for Vendas Agent
"""
import asyncio
import httpx

BASE_URL = "http://localhost:8001"


async def test_vendas_agent():
    """Test sales agent conversation flow"""
    async with httpx.AsyncClient() as client:
        phone = "+5511999999999"
        
        # Test 1: Initial message
        print("📞 Test 1: Initial contact")
        response = await client.post(
            f"{BASE_URL}/api/v1/agents/vendas/message",
            json={"phone": phone, "message": "Olá, quero um orçamento"}
        )
        print(f"Response: {response.json()}\n")
        
        # Test 2: Provide consumption
        print("📞 Test 2: Provide consumption")
        response = await client.post(
            f"{BASE_URL}/api/v1/agents/vendas/message",
            json={"phone": phone, "message": "Minha conta vem 450 kWh por mês"}
        )
        print(f"Response: {response.json()}\n")
        
        # Test 3: Provide roof type
        print("📞 Test 3: Provide roof type")
        response = await client.post(
            f"{BASE_URL}/api/v1/agents/vendas/message",
            json={"phone": phone, "message": "Meu telhado é de cerâmica"}
        )
        print(f"Response: {response.json()}\n")
        
        # Test 4: Request human transfer
        print("📞 Test 4: Request human transfer")
        response = await client.post(
            f"{BASE_URL}/api/v1/agents/vendas/message",
            json={"phone": phone, "message": "Quero falar com um atendente"}
        )
        print(f"Response: {response.json()}\n")
        
        # Test 5: Get metrics
        print("📊 Test 5: Get metrics")
        response = await client.get(f"{BASE_URL}/api/v1/agents/vendas/metrics")
        print(f"Metrics: {response.json()}\n")


async def test_vendas_config():
    """Test sales agent configuration"""
    async with httpx.AsyncClient() as client:
        print("⚙️ Test: Configure agent")
        response = await client.post(
            f"{BASE_URL}/api/v1/agents/vendas/config",
            json={
                "config": {
                    "model": "gemini-1.5-flash",
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            }
        )
        print(f"Response: {response.json()}\n")


if __name__ == "__main__":
    print("🚀 Testing Vendas Agent\n")
    asyncio.run(test_vendas_agent())
    asyncio.run(test_vendas_config())
    print("✅ Tests completed!")
