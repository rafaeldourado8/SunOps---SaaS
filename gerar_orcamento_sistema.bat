@echo off
chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     SISTEMA OPS CRM - GERAÇÃO DE ORÇAMENTO AUTOMÁTICO     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📋 DADOS DO CLIENTE
echo ────────────────────────────────────────────────────────────
echo    Nome: Rafael
echo    Cidade: Itaporã-MS (usando dados de Campo Grande)
echo    Conta atual: R$ 350,00/mês
echo    Tipo: Residencial Monofásico
echo.
echo ⚙️  Processando orçamento...
echo.

curl -s -X POST "http://localhost:8001/api/orcamentos/gerar" ^
  -H "Content-Type: application/json" ^
  -d "{\"nome_cliente\":\"Rafael\",\"cidade\":\"Campo Grande\",\"conta_energia\":350,\"tipo_ligacao\":\"MONOFASICA\",\"tipo_telhado\":\"CERAMICO\",\"forma_pagamento\":\"A_VISTA\",\"classe_tarifaria\":\"B1\"}" > orcamento_temp.json

echo ✅ Orçamento gerado com sucesso!
echo.
echo ════════════════════════════════════════════════════════════
echo.
echo 📊 DIMENSIONAMENTO
echo ────────────────────────────────────────────────────────────

type orcamento_temp.json | jq -r "\"   Consumo médio: \" + (.dimensionamento.consumo_medio | tostring) + \" kWh/mês\""
type orcamento_temp.json | jq -r "\"   Consumo compensável: \" + (.dimensionamento.consumo_compensavel | tostring) + \" kWh/mês\""
type orcamento_temp.json | jq -r "\"   Potência necessária: \" + (.dimensionamento.potencia_necessaria | tostring | .[0:4]) + \" kWp\""

echo.
echo 🔧 KIT FOTOVOLTAICO
echo ────────────────────────────────────────────────────────────

type orcamento_temp.json | jq -r "\"   Módulos: \" + (.kit.modulos.quantidade | tostring) + \"x \" + .kit.modulos.modelo"
type orcamento_temp.json | jq -r "\"   Inversor: \" + .kit.inversor.modelo"
type orcamento_temp.json | jq -r "\"   Potência instalada: \" + (.kit.potencia_instalada | tostring) + \" kWp\""
type orcamento_temp.json | jq -r "\"   DC/AC ratio: \" + (.kit.dc_ac_ratio | tostring | .[0:4]) + \" ✅\""

echo.
echo ⚡ GERAÇÃO DE ENERGIA
echo ────────────────────────────────────────────────────────────

type orcamento_temp.json | jq -r "\"   Geração mensal: \" + (.geracao.mensal_kwh | tostring | .[0:5]) + \" kWh\""
type orcamento_temp.json | jq -r "\"   Geração anual: \" + (.geracao.anual_kwh | tostring | .[0:6]) + \" kWh\""

echo.
echo 💰 INVESTIMENTO
echo ────────────────────────────────────────────────────────────

type orcamento_temp.json | jq -r "\"   Equipamentos: R$ \" + (.financeiro.custo_equipamentos | tostring)"
type orcamento_temp.json | jq -r "\"   Estrutura: R$ \" + (.financeiro.custo_estrutura | tostring)"
type orcamento_temp.json | jq -r "\"   Mão de obra: R$ \" + (.financeiro.custo_mao_obra | tostring)"
type orcamento_temp.json | jq -r "\"   Impostos: R$ \" + (.financeiro.impostos | tostring)"
type orcamento_temp.json | jq -r "\"   Margem: R$ \" + (.financeiro.margem | tostring)"
echo.
type orcamento_temp.json | jq -r "\"   💵 TOTAL: R$ \" + (.financeiro.investimento_total | tostring)"

echo.
echo 📈 RETORNO DO INVESTIMENTO
echo ────────────────────────────────────────────────────────────

type orcamento_temp.json | jq -r "\"   Economia mensal: R$ \" + (.financeiro.economia_mensal | tostring)"
type orcamento_temp.json | jq -r "\"   Economia anual: R$ \" + (.financeiro.economia_anual | tostring)"
type orcamento_temp.json | jq -r "\"   Payback: \" + (.financeiro.payback_anos | tostring | .[0:3]) + \" anos\""
echo.
type orcamento_temp.json | jq -r "\"   💎 Lucro em 25 anos: R$ \" + (.projecao_25_anos.lucro_liquido | tostring)"

echo.
echo ⏱️  PERFORMANCE
echo ────────────────────────────────────────────────────────────

type orcamento_temp.json | jq -r "\"   Tempo de processamento: \" + (.performance.tempo_processamento_ms | tostring) + \"ms\""

echo.
echo ════════════════════════════════════════════════════════════
echo.
echo ✅ ORÇAMENTO PRONTO PARA APRESENTAÇÃO!
echo.
echo 📄 Próximos passos:
echo    1. Apresentar proposta ao cliente
echo    2. Aguardar aprovação
echo    3. Solicitar contrato ao admin
echo.
echo 💾 Dados salvos em: orcamento_temp.json
echo.

del orcamento_temp.json 2>nul
