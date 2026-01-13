#!/bin/bash

echo "🧪 Testando Autenticação SunOps"
echo "================================"
echo ""

# Teste 1: Login
echo "1️⃣ Testando login..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@sunops.com","password":"admin123"}')

ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$ACCESS_TOKEN" ]; then
  echo "❌ FALHOU: Token não retornado"
  echo "Response: $LOGIN_RESPONSE"
  exit 1
else
  echo "✅ PASSOU: Token recebido"
fi

echo ""

# Teste 2: Validar token
echo "2️⃣ Testando endpoint /me com token..."
ME_RESPONSE=$(curl -s http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $ACCESS_TOKEN")

EMAIL=$(echo $ME_RESPONSE | grep -o '"email":"[^"]*' | cut -d'"' -f4)

if [ "$EMAIL" = "admin@sunops.com" ]; then
  echo "✅ PASSOU: Token validado, usuário autenticado"
else
  echo "❌ FALHOU: Token inválido"
  echo "Response: $ME_RESPONSE"
  exit 1
fi

echo ""

# Teste 3: Verificar campos retornados
echo "3️⃣ Verificando campos do usuário..."
HAS_ID=$(echo $ME_RESPONSE | grep -o '"id":[0-9]*')
HAS_FULL_NAME=$(echo $ME_RESPONSE | grep -o '"full_name":"[^"]*')
HAS_IS_ACTIVE=$(echo $ME_RESPONSE | grep -o '"is_active":true')

if [ -n "$HAS_ID" ] && [ -n "$HAS_FULL_NAME" ] && [ -n "$HAS_IS_ACTIVE" ]; then
  echo "✅ PASSOU: Todos os campos presentes"
else
  echo "❌ FALHOU: Campos faltando"
  echo "Response: $ME_RESPONSE"
  exit 1
fi

echo ""
echo "================================"
echo "✅ Todos os testes passaram!"
echo ""
echo "📊 Resumo:"
echo "  - Login: ✅"
echo "  - Token JWT: ✅"
echo "  - Validação: ✅"
echo "  - Campos: ✅"
echo ""
echo "🎯 Próximo passo: Testar no navegador"
echo "   URL: http://localhost"
echo "   Email: admin@sunops.com"
echo "   Senha: admin123"
