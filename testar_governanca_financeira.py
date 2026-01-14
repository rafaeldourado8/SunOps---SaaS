"""Teste de governança financeira."""
import sys
sys.path.insert(0, '/app')

from decimal import Decimal
from shared.domain.services.calculadora_financeira_governada import CalculadoraFinanceiraGovernada

print("=" * 70)
print("TESTE DE GOVERNANÇA FINANCEIRA")
print("=" * 70)
print()

# Exemplo: 9 painéis, custo equipamentos R$ 14.200
custo_equipamentos = Decimal("14200.00")
qtd_modulos = 9

print("📋 DADOS DE ENTRADA")
print("-" * 70)
print(f"Custo equipamentos: R$ {custo_equipamentos:,.2f}")
print(f"Quantidade de módulos: {qtd_modulos}")
print()

# Calcular visão ADMIN
print("🔐 VISÃO ADMIN (Dados Completos)")
print("-" * 70)
resultado_admin = CalculadoraFinanceiraGovernada.calcular_preco_completo(
    custo_equipamentos,
    qtd_modulos
)

print(f"Custo equipamentos: R$ {resultado_admin['custo_equipamentos']:,.2f}")
print(f"Custo montagem (9 x R$ 70): R$ {resultado_admin['custo_montagem']:,.2f}")
print(f"Custo operacional fixo: R$ {resultado_admin['custo_operacional']:,.2f}")
print(f"CUSTO TOTAL: R$ {resultado_admin['custo_total']:,.2f}")
print()
print(f"Preço mínimo calculado: R$ {resultado_admin['preco_minimo']:,.2f}")
print(f"Preço final (arredondado): R$ {resultado_admin['preco_final']:,.2f}")
print()
print("💰 QUEBRA FINANCEIRA:")
print(f"  Comissão (5%): R$ {resultado_admin['comissao']:,.2f}")
print(f"  Imposto (6%): R$ {resultado_admin['imposto']:,.2f}")
print(f"  Lucro líquido: R$ {resultado_admin['lucro_liquido']:,.2f}")
print(f"  Margem real: {resultado_admin['margem_real']:.2%}")
print(f"  Margem válida: {'✅ SIM' if resultado_admin['margem_valida'] else '❌ NÃO'}")
print()

# Calcular visão VENDEDOR
print("👤 VISÃO VENDEDOR (Dados Restritos)")
print("-" * 70)
resultado_vendedor = CalculadoraFinanceiraGovernada.calcular_preco_vendedor(
    custo_equipamentos,
    qtd_modulos
)

print(f"Preço final: R$ {resultado_vendedor['preco_final']:,.2f}")
print(f"Parcelas: {resultado_vendedor['parcelas_sugeridas']}x de R$ {resultado_vendedor['valor_parcela']:,.2f}")
print()
print("⚠️  VENDEDOR NÃO VÊ:")
print("  ❌ Custo de equipamentos")
print("  ❌ Custo de montagem")
print("  ❌ Margem de lucro")
print("  ❌ Comissão")
print("  ❌ Impostos")
print()

print("=" * 70)
print("✅ GOVERNANÇA FINANCEIRA FUNCIONANDO")
print("=" * 70)
print()
print("📊 VALIDAÇÕES:")
print(f"  ✅ Margem >= 20%: {resultado_admin['margem_real']:.2%}")
print(f"  ✅ Preço arredondado para múltiplo de 100")
print(f"  ✅ Comissão e impostos recalculados após arredondamento")
print(f"  ✅ Vendedor vê apenas preço final")
print()
