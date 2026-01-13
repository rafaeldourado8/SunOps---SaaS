#!/bin/bash

echo "🚀 Testing Vendas Agent"
echo ""

BASE_URL="http://localhost:8001/api/v1"
PHONE="+5511999999999"

echo "📞 Test 1: Initial contact"
curl -X POST "$BASE_URL/agents/vendas/message" \
  -H "Content-Type: application/json" \
  -d "{\"phone\": \"$PHONE\", \"message\": \"Olá, quero um orçamento\"}" \
  2>/dev/null | python -m json.tool
echo ""
echo ""

echo "📞 Test 2: Provide consumption"
curl -X POST "$BASE_URL/agents/vendas/message" \
  -H "Content-Type: application/json" \
  -d "{\"phone\": \"$PHONE\", \"message\": \"Minha conta vem 450 kWh por mês\"}" \
  2>/dev/null | python -m json.tool
echo ""
echo ""

echo "📞 Test 3: Provide roof type"
curl -X POST "$BASE_URL/agents/vendas/message" \
  -H "Content-Type: application/json" \
  -d "{\"phone\": \"$PHONE\", \"message\": \"Meu telhado é de cerâmica\"}" \
  2>/dev/null | python -m json.tool
echo ""
echo ""

echo "📞 Test 4: Request human transfer"
curl -X POST "$BASE_URL/agents/vendas/message" \
  -H "Content-Type: application/json" \
  -d "{\"phone\": \"$PHONE\", \"message\": \"Quero falar com um atendente\"}" \
  2>/dev/null | python -m json.tool
echo ""
echo ""

echo "📊 Test 5: Get metrics"
curl -X GET "$BASE_URL/agents/vendas/metrics" \
  -H "Content-Type: application/json" \
  2>/dev/null | python -m json.tool
echo ""
echo ""

echo "⚙️ Test 6: Configure agent"
curl -X POST "$BASE_URL/agents/vendas/config" \
  -H "Content-Type: application/json" \
  -d '{"config": {"model": "gemini-1.5-flash", "temperature": 0.7}}' \
  2>/dev/null | python -m json.tool
echo ""

echo "✅ Tests completed!"
