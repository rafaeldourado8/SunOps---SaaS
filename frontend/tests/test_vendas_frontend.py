#!/usr/bin/env python3
"""Teste E2E - Agente de Vendas Frontend"""

import requests
import sys
import time

API_BASE = "http://api:8000/api/v1"

def wait_for_api():
    """Aguarda API estar disponível"""
    print("⏳ Aguardando API...")
    for i in range(60):
        try:
            r = requests.get(f"http://api:8000/health", timeout=5)
            if r.status_code == 200:
                print("✅ API disponível")
                return
        except Exception as e:
            if i % 10 == 0:
                print(f"   Tentativa {i}/60: {e}")
            time.sleep(2)
    raise Exception("API não respondeu")

def test_vendas_metrics():
    """Teste 1: Buscar métricas do agente"""
    print("\n📊 Teste 1: Buscar métricas")
    r = requests.get(f"{API_BASE}/agents/vendas/metrics")
    assert r.status_code == 200
    data = r.json()
    assert "total_conversations" in data
    assert "orcamentos_gerados" in data
    print(f"✅ Métricas: {data['total_conversations']} conversas, {data['orcamentos_gerados']} orçamentos")

def test_vendas_config():
    """Teste 2: Salvar configuração"""
    print("\n⚙️  Teste 2: Salvar configuração")
    config = {
        "model": "gemini-1.5-flash",
        "systemPrompt": "Você é vendedor solar",
        "rules": ["Não inventar", "Manter contexto"]
    }
    r = requests.post(f"{API_BASE}/agents/vendas/config", json={"config": config})
    assert r.status_code in [200, 201]
    print("✅ Configuração salva")

def test_vendas_message():
    """Teste 3: Enviar mensagem"""
    print("\n💬 Teste 3: Enviar mensagem")
    r = requests.post(f"{API_BASE}/agents/vendas/message", json={
        "phone": "+5511999999999",
        "message": "Quero orçamento"
    })
    assert r.status_code == 200
    data = r.json()
    assert "text" in data
    print(f"✅ Resposta: {data['text'][:50]}...")

def test_metrics_updated():
    """Teste 4: Verificar métricas atualizadas"""
    print("\n📈 Teste 4: Métricas atualizadas")
    r = requests.get(f"{API_BASE}/agents/vendas/metrics")
    assert r.status_code == 200
    data = r.json()
    print(f"✅ Total conversas: {data['total_conversations']}")
    print(f"✅ Orçamentos gerados: {data['orcamentos_gerados']}")

if __name__ == "__main__":
    try:
        wait_for_api()
        test_vendas_metrics()
        test_vendas_config()
        test_vendas_message()
        test_metrics_updated()
        print("\n✅ Todos os testes passaram!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
