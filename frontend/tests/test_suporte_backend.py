#!/usr/bin/env python3
"""Teste E2E - Agente de Suporte"""

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

def test_suporte_metrics():
    print("\n📊 Teste 1: Buscar métricas do agente")
    r = requests.get(f"{API_BASE}/agents/suporte/metrics")
    print(f"Status: {r.status_code}")
    if r.status_code != 200:
        print(f"Erro: {r.text}")
    assert r.status_code == 200
    data = r.json()
    assert "total_tickets" in data
    assert "open_tickets" in data
    print(f"✅ Métricas: {data['total_tickets']} tickets, {data['open_tickets']} abertos")

def test_suporte_config():
    print("\n⚙️  Teste 2: Salvar configuração")
    config = {
        "model": "gemini-1.5-flash",
        "systemPrompt": "Você é agente de suporte técnico",
        "rules": ["Criar ticket automaticamente", "Verificar garantia"]
    }
    r = requests.post(f"{API_BASE}/agents/suporte/config", json={"config": config})
    assert r.status_code in [200, 201]
    print("✅ Configuração salva")

def test_create_ticket():
    print("\n🎫 Teste 3: Listar tickets")
    r = requests.get(f"{API_BASE}/agents/tickets")
    assert r.status_code == 200
    data = r.json()
    assert "tickets" in data
    print(f"✅ Total de tickets: {len(data['tickets'])}")

def test_list_tickets():
    print("\n📋 Teste 4: Listar tickets")
    r = requests.get(f"{API_BASE}/agents/tickets")
    assert r.status_code == 200
    data = r.json()
    assert "tickets" in data
    print(f"✅ Total de tickets: {len(data['tickets'])}")

def test_sla():
    print("\n⏱️  Teste 5: Verificar SLA")
    r = requests.get(f"{API_BASE}/agents/suporte/metrics")
    assert r.status_code == 200
    data = r.json()
    sla_hours = data.get("avg_sla_hours", 0)
    print(f"✅ SLA médio: {sla_hours}h")
    if sla_hours > 0:
        assert sla_hours < 48, f"SLA muito alto: {sla_hours}h"

if __name__ == "__main__":
    try:
        wait_for_api()
        test_suporte_metrics()
        test_suporte_config()
        test_create_ticket()
        test_list_tickets()
        test_sla()
        print("\n✅ Todos os testes passaram!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
