"""Fluxo completo de orçamento - Rafael em Itaporã-MS."""
import sys
sys.path.insert(0, '/app')

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from decimal import Decimal
from contexts.orcamentos.application.dtos.orcamento_dto import InputOrcamento
from contexts.orcamentos.application.use_cases.gerar_orcamento_automatico import MotorOrcamentoAutomatico

print("=" * 60)
print("ORÇAMENTO AUTOMÁTICO - SISTEMA FOTOVOLTAICO")
print("=" * 60)
print()

# Dados do cliente
print("📋 DADOS DO CLIENTE")
print("-" * 60)
print("Nome: Rafael")
print("Cidade: Itaporã-MS")
print("Conta de energia: R$ 350,00/mês")
print("Tipo de ligação: Monofásica (padrão residencial)")
print()

# Calcular consumo aproximado
tarifa_media = Decimal("0.80")  # R$/kWh média
consumo_kwh = int(350 / float(tarifa_media))  # ~437 kWh

print(f"💡 Consumo estimado: {consumo_kwh} kWh/mês")
print()

# Gerar orçamento
print("⚙️ GERANDO ORÇAMENTO AUTOMÁTICO...")
print("-" * 60)

input_data = InputOrcamento(
    cidade="Campo Grande",  # Capital mais próxima com dados HSP
    consumo_mensal_kwh=consumo_kwh,
    tipo_ligacao="MONOFASICA",
    tipo_telhado="CERAMICO",
    forma_pagamento="A_VISTA",
    classe_tarifaria="B1"
)

motor = MotorOrcamentoAutomatico()
output = motor.executar(input_data)

print()
print("=" * 60)
print("✅ PROPOSTA COMERCIAL GERADA")
print("=" * 60)
print()

print("📊 DIMENSIONAMENTO DO SISTEMA")
print("-" * 60)
print(f"Consumo médio: {output.consumo_medio} kWh/mês")
print(f"Consumo compensável: {output.consumo_compensavel} kWh/mês")
print(f"Potência necessária: {output.potencia_necessaria:.2f} kWp")
print()

print("🔧 KIT FOTOVOLTAICO SUGERIDO")
print("-" * 60)
print(f"Módulos: {output.kit.qtd_modulos}x {output.kit.modulo_nome}")
print(f"Inversor: {output.kit.inversor_nome}")
print(f"Potência instalada: {output.kit.potencia_instalada} kWp")
print(f"Relação DC/AC: {output.kit.dc_ac_ratio:.2f} {'✅' if output.kit.dc_ac_valido else '⚠️'}")
print()

print("⚡ GERAÇÃO DE ENERGIA")
print("-" * 60)
print(f"Geração mensal: {output.geracao_mensal:.0f} kWh/mês")
print(f"Geração anual: {output.geracao_anual:.0f} kWh/ano")
print(f"HSP utilizado: {output.hsp_utilizado} horas/dia")
print(f"Fator de perdas: {output.fator_perdas}")
print()

print("💰 ANÁLISE FINANCEIRA")
print("-" * 60)
print(f"Custo dos equipamentos: R$ {output.financeiro.custo_equipamentos:,.2f}")
print(f"Custo da estrutura: R$ {output.financeiro.custo_estrutura:,.2f}")
print(f"Mão de obra: R$ {output.financeiro.custo_mao_obra:,.2f}")
print(f"Impostos (16.5%): R$ {output.financeiro.impostos:,.2f}")
print(f"Margem (15%): R$ {output.financeiro.margem:,.2f}")
print()
print(f"💵 INVESTIMENTO TOTAL: R$ {output.financeiro.custo_total:,.2f}")
print()

print("📈 RETORNO DO INVESTIMENTO")
print("-" * 60)
print(f"Economia mensal: R$ {output.financeiro.economia_mensal:,.2f}")
print(f"Economia anual: R$ {output.financeiro.economia_anual:,.2f}")
print(f"⏱️  Payback: {output.financeiro.payback_anos:.1f} anos")
print()

# Economia em 25 anos
economia_25_anos = output.financeiro.economia_anual * 25
lucro_liquido = economia_25_anos - output.financeiro.custo_total
print(f"💎 Economia em 25 anos: R$ {economia_25_anos:,.2f}")
print(f"💰 Lucro líquido: R$ {lucro_liquido:,.2f}")
print()

if output.alertas:
    print("⚠️ ALERTAS")
    print("-" * 60)
    for alerta in output.alertas:
        print(f"• {alerta}")
    print()

print("⏱️ PERFORMANCE")
print("-" * 60)
print(f"Tempo de processamento: {output.tempo_processamento_ms}ms")
print()

print("=" * 60)
print("📄 PRÓXIMOS PASSOS")
print("=" * 60)
print("1. ✅ Proposta técnica gerada")
print("2. 📋 Aguardando aprovação do cliente")
print("3. 📝 Após aprovação: gerar contrato")
print("4. 🏗️  Instalação e homologação")
print()

print("💡 OBSERVAÇÕES:")
print("-" * 60)
print("• Sistema dimensionado para Itaporã-MS")
print("• Valores incluem equipamentos, instalação e homologação")
print("• Garantia de 25 anos nos módulos")
print("• Garantia de 5 anos no inversor")
print("• Economia calculada com tarifa média de R$ 0,80/kWh")
print()

print("=" * 60)
print("Proposta válida por 7 dias")
print("Vendedor: Sistema Automático")
print("Data:", output.kit.potencia_instalada)
print("=" * 60)
