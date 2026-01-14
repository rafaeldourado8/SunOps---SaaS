@echo off
echo.
echo ========================================
echo SISTEMA OPS CRM - ORCAMENTO AUTOMATICO
echo ========================================
echo.
echo CLIENTE: Rafael
echo CIDADE: Itapora-MS
echo CONTA: R$ 350,00/mes
echo.
echo Gerando orcamento via API...
echo.

curl -s -X POST "http://localhost:8001/api/orcamentos/gerar" ^
  -H "Content-Type: application/json" ^
  -d "{\"nome_cliente\":\"Rafael\",\"cidade\":\"Campo Grande\",\"conta_energia\":350}" > orcamento.json

echo ORCAMENTO GERADO!
echo.
echo ========================================
echo RESULTADO:
echo ========================================
echo.

type orcamento.json

echo.
echo.
echo ========================================
echo Arquivo salvo: orcamento.json
echo ========================================
echo.
echo Abra o arquivo para ver detalhes completos
echo ou acesse: http://localhost:8001/docs
echo.
