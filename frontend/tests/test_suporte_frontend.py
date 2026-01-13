#!/usr/bin/env python3
"""Teste E2E - Frontend Agente de Suporte"""

import requests
import sys
import time

API_BASE = "http://api:8000/api/v1"

def wait_for_api():
    print("⏳ Aguardando API...")
    for i in range(60):
        try:
            r = requests.get(f"http://api:8000/health", timeout=5)
            if r.status_code == 200:
                print("✅ API disponível")
                return
        except Exception as e:
            if i % 10 == 0:
                print(f"   Tentativa {i}/60")
            time.sleep(2)
    raise Exception("API não respondeu")

def test_node_types():
    """Teste 1: Verificar se agent_suporte está nos tipos de nodes"""
    print("\n📦 Teste 1: Verificar tipos de nodes")
    r = requests.get(f"{API_BASE}/workflows/node-types")
    assert r.status_code == 200
    types = r.json()
    bot_suporte = next((t for t in types if t['type'] == 'agent_suporte'), None)
    assert bot_suporte is not None, "agent_suporte não encontrado nos tipos"
    print(f"✅ Node agent_suporte encontrado: {bot_suporte['name']}")

def test_config_endpoint():
    """Teste 2: Configurar agente de suporte"""
    print("\n⚙️  Teste 2: Configurar agente")
    config = {
        "model": "gemini-pro",
        "systemPrompt": "Você é agente de suporte",
        "rules": ["Criar ticket", "Verificar garantia"]
    }
    r = requests.post(f"{API_BASE}/agents/suporte/config", json={"config": config})
    assert r.status_code in [200, 201]
    print("✅ Configuração salva")

def test_metrics_endpoint():
    """Teste 3: Buscar métricas"""
    print("\n📊 Teste 3: Buscar métricas")
    r = requests.get(f"{API_BASE}/agents/suporte/metrics")
    assert r.status_code == 200
    data = r.json()
    assert "total_tickets" in data
    assert "open_tickets" in data
    assert "avg_sla_hours" in data
    print(f"✅ Métricas: {data['total_tickets']} tickets, SLA {data['avg_sla_hours']}h")

def test_tickets_list():
    """Teste 4: Listar tickets"""
    print("\n📋 Teste 4: Listar tickets")
    r = requests.get(f"{API_BASE}/agents/tickets")
    assert r.status_code == 200
    data = r.json()
    assert "tickets" in data
    print(f"✅ {len(data['tickets'])} tickets encontrados")

if __name__ == "__main__":
    try:
        wait_for_api()
        test_node_types()
        test_config_endpoint()
        test_metrics_endpoint()
        test_tickets_list()
        print("\n✅ Todos os testes do frontend passaram!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
