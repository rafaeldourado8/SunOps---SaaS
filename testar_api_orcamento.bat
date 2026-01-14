@echo off
echo ========================================
echo GERANDO ORCAMENTO VIA API
echo ========================================
echo.
echo Cliente: Rafael
echo Cidade: Itapora-MS
echo Conta: R$ 350,00/mes
echo.
echo Chamando API...
echo.

curl -X POST "http://localhost:8001/api/orcamentos/gerar" ^
  -H "Content-Type: application/json" ^
  -d "{\"nome_cliente\":\"Rafael\",\"cidade\":\"Campo Grande\",\"conta_energia\":350,\"tipo_ligacao\":\"MONOFASICA\",\"tipo_telhado\":\"CERAMICO\",\"forma_pagamento\":\"A_VISTA\",\"classe_tarifaria\":\"B1\"}"

echo.
echo.
echo ========================================
echo ORCAMENTO GERADO!
echo ========================================
