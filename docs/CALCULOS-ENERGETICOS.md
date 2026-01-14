# Cálculos Energéticos - Sistema Profissional

## ✅ Implementado

Sistema completo de cálculos energéticos seguindo as melhores práticas do mercado de energia solar.

---

## 📊 Value Objects

### TipoLigacao
- Monofásica (30 kWh disponibilidade)
- Bifásica (50 kWh disponibilidade)
- Trifásica (100 kWh disponibilidade)

### Tensao
- 127V, 220V, 380V

### ClasseTarifaria
- B1, B2, B3, A4

### Tarifa
- TE (Tarifa de Energia)
- TUSD (Tarifa de Uso do Sistema de Distribuição)
- Total = TE + TUSD

### Localizacao
- Latitude, Longitude, Cidade

### HistoricoConsumo
- 1 a 12 meses de consumo
- Calcula média mensal automaticamente

### HSP (Horas de Sol Pleno)
- Valor médio diário
- Fonte (CRESESB, PVGIS, API)
- Inclinação (0° a 90°)
- Azimute (-180° a 180°)

---

## 🏢 Entities

### UnidadeConsumidora
Representa a UC do cliente com:
- Histórico de consumo
- Tipo de ligação
- Tensão
- Classe tarifária
- Tarifa
- Localização

**Propriedades calculadas:**
- `consumo_medio`: Média mensal em kWh
- `geracao_necessaria`: Consumo médio - custo de disponibilidade

---

## ⚙️ Services de Cálculo

### 1. CalculadoraDimensionamento

**Calcula potência necessária do sistema:**

```python
potencia_kWp = geracao_necessaria / (HSP × 30 × fator_perdas)
```

- Fator de perdas: 0.75 a 0.82 (padrão: 0.80)
- Considera: sujeira, cabeamento, inversor, mismatch, temperatura

**Exemplo:**
```python
hsp = HSP(Decimal("5.0"), "CRESESB")
potencia = CalculadoraDimensionamento.calcular_potencia_sistema(
    geracao_necessaria=Decimal("370"),
    hsp=hsp,
    fator_perdas=Decimal("0.80")
)
# Resultado: 3.08 kWp
```

---

### 2. CalculadoraPotenciaInstalada

**Calcula potência instalada real:**

```python
potencia_instalada = qtd_modulos × potencia_modulo
```

**Calcula relação DC/AC:**

```python
dc_ac_ratio = potencia_instalada / potencia_inversor
```

- Ideal: 1.10 ≤ DC/AC ≤ 1.30

**Exemplo:**
```python
potencia = CalculadoraPotenciaInstalada.calcular(
    qtd_modulos=8,
    potencia_modulo=Decimal("0.550")
)
# Resultado: 4.4 kWp

ratio = CalculadoraPotenciaInstalada.calcular_dc_ac_ratio(
    potencia_instalada=Decimal("4.4"),
    potencia_inversor=Decimal("4.0")
)
# Resultado: 1.1 (dentro do ideal)
```

---

### 3. ValidadorEletrico

**Valida parâmetros elétricos obrigatórios:**

✅ Tensão máxima string < Vmax inversor  
✅ Tensão mínima MPPT > Vmin inversor  
✅ Corrente < Imax inversor

**Exemplo:**
```python
ValidadorEletrico.validar_tensao_string(
    tensao_string=Decimal("400"),
    vmax_inversor=Decimal("600"),
    vmin_mppt=Decimal("150")
)
# Resultado: True
```

---

### 4. CalculadoraGeracao

**Geração mensal:**

```python
geracao_mensal = potencia_instalada × HSP × 30 × fator_perdas
```

**Geração anual:**

```python
geracao_anual = geracao_mensal × 12
```

**Geração com degradação:**

```python
geracao_ano_n = geracao_ano_1 × (1 - degradacao)^n
```

- Taxa de degradação: 0.5% a 0.8% ao ano (padrão: 0.7%)

**Exemplo:**
```python
hsp = HSP(Decimal("5.0"), "CRESESB")
geracao_mensal = CalculadoraGeracao.calcular_geracao_mensal(
    potencia_instalada=Decimal("4.4"),
    hsp=hsp,
    fator_perdas=Decimal("0.80")
)
# Resultado: 528 kWh/mês

geracao_anual = CalculadoraGeracao.calcular_geracao_anual(geracao_mensal)
# Resultado: 6.336 kWh/ano
```

---

### 5. CalculadoraEconomia

**Economia mensal:**

```python
economia_mensal = geracao_mensal × tarifa_kWh
```

**Payback simples:**

```python
payback_anos = custo_total / economia_anual
```

**Economia com Lei 14.300 (Fio B):**

```python
economia_real = geracao × (tarifa - fioB)
```

**Exemplo:**
```python
economia_mensal = CalculadoraEconomia.calcular_economia_mensal(
    geracao_mensal=Decimal("528"),
    tarifa_kwh=Decimal("0.80")
)
# Resultado: R$ 422,40/mês

payback = CalculadoraEconomia.calcular_payback_simples(
    custo_total=Decimal("20000"),
    economia_anual=Decimal("5068.80")
)
# Resultado: 3.95 anos
```

---

### 6. CalculadoraFinanciamento

**Parcela (Sistema Price):**

```python
PMT = financiamento × i / (1 - (1 + i)^-n)
```

**Delta mensal:**

```python
delta_mensal = economia_mensal - parcela
```

- ✅ Viável se parcela < economia

**Exemplo:**
```python
parcela = CalculadoraFinanciamento.calcular_parcela(
    valor_financiado=Decimal("20000"),
    taxa_juros_mensal=Decimal("0.01"),  # 1% a.m.
    num_parcelas=60
)
# Resultado: R$ 444,89

delta = CalculadoraFinanciamento.calcular_delta_mensal(
    economia_mensal=Decimal("422.40"),
    parcela=parcela
)
# Resultado: -R$ 22,49 (não viável)
```

---

### 7. CalculadoraVPL

**Valor Presente Líquido:**

```python
VPL = -custo_inicial + Σ (FCt / (1 + taxa)^t)
```

**Exemplo:**
```python
fluxos = [Decimal("5000")] * 25  # 25 anos
vpls = CalculadoraVPL.calcular(
    custo_inicial=Decimal("20000"),
    fluxos_caixa=fluxos,
    taxa_desconto=Decimal("0.08")
)
# Resultado: VPL > 0 (investimento viável)
```

---

### 8. CalculadoraTIR

**Fluxo de caixa para 25 anos:**

```python
FC0 = -custo_inicial
FC1..25 = economia_anual - O&M
```

**Exemplo:**
```python
fluxos = CalculadoraTIR.calcular_fluxo_caixa(
    custo_inicial=Decimal("20000"),
    economia_anual=Decimal("5000"),
    custo_om_anual=Decimal("200"),
    anos=25
)
# Resultado: [-20000, 4800, 4800, ..., 4800]
```

---

### 9. CalculadoraOM

**Custo de Operação e Manutenção:**

```python
O&M = custo_sistema × percentual
```

- Percentual: 0.5% a 1% do CAPEX/ano (padrão: 1%)

**Exemplo:**
```python
om = CalculadoraOM.calcular_anual(
    custo_sistema=Decimal("20000"),
    percentual=Decimal("0.01")
)
# Resultado: R$ 200/ano
```

---

## 🧪 Testes

**15 testes passando (100%)**

```bash
docker-compose exec django pytest tests/test_calculos_energeticos.py -v
```

Cobertura:
- ✅ Value Objects (TipoLigacao, Tarifa, HSP, etc)
- ✅ Entity UnidadeConsumidora
- ✅ Dimensionamento de sistema
- ✅ Potência instalada e DC/AC ratio
- ✅ Validação elétrica
- ✅ Geração mensal/anual
- ✅ Degradação de módulos
- ✅ Economia e payback
- ✅ Lei 14.300 (Fio B)
- ✅ Financiamento
- ✅ VPL e TIR
- ✅ O&M

---

## 🔥 Erros Fatais EVITADOS

❌ ~~Ignorar custo de disponibilidade~~ → ✅ Implementado  
❌ ~~Ignorar perdas~~ → ✅ Fator de perdas obrigatório  
❌ ~~Usar HSP fixo nacional~~ → ✅ HSP por localização  
❌ ~~Zerar 100% do consumo~~ → ✅ Desconta custo disponibilidade  
❌ ~~Não validar elétrica~~ → ✅ ValidadorEletrico completo  
❌ ~~Não simular Lei 14.300~~ → ✅ Cálculo com Fio B

---

## 📐 Fórmulas Implementadas

| Cálculo | Fórmula | Status |
|---------|---------|--------|
| Consumo Médio | soma(12m) / 12 | ✅ |
| Geração Necessária | consumo - disponibilidade | ✅ |
| Potência Sistema | necessária / (HSP × 30 × perdas) | ✅ |
| Potência Instalada | qtd × potência_módulo | ✅ |
| DC/AC Ratio | instalada / inversor | ✅ |
| Geração Mensal | instalada × HSP × 30 × perdas | ✅ |
| Geração Anual | mensal × 12 | ✅ |
| Degradação | ano1 × (1 - taxa)^n | ✅ |
| Economia Mensal | geração × tarifa | ✅ |
| Payback | custo / economia_anual | ✅ |
| Fio B | geração × (tarifa - fioB) | ✅ |
| Financiamento PMT | valor × i / (1 - (1+i)^-n) | ✅ |
| VPL | Σ (FC / (1+taxa)^t) | ✅ |
| O&M | custo × % | ✅ |

---

## 🎯 Próximos Passos

1. **Integração com APIs de irradiação:**
   - CRESESB
   - PVGIS
   - NASA POWER

2. **Relatórios automáticos:**
   - Proposta comercial
   - Memorial descritivo
   - ART/CREA
   - Simulação ANEEL

3. **Interface FastAPI:**
   - Endpoints para cálculos
   - Validação de sistemas
   - Geração de propostas

---

## 📚 Arquitetura

```
contexts/orcamentos/
├── domain/
│   ├── value_objects/
│   │   ├── dados_uc.py      # TipoLigacao, Tensao, Tarifa, etc
│   │   └── hsp.py            # Horas de Sol Pleno
│   ├── entities/
│   │   └── unidade_consumidora.py
│   └── services/
│       └── calculos_energeticos.py  # 9 calculadoras
└── tests/
    └── test_calculos_energeticos.py  # 15 testes
```

**Princípios aplicados:**
- ✅ DDD (Value Objects, Entities, Services)
- ✅ SOLID (Single Responsibility, cada calculadora uma função)
- ✅ Complexidade < 5 (métodos simples e diretos)
- ✅ Imutabilidade (Value Objects frozen)
- ✅ Validação rigorosa (todos os inputs validados)
