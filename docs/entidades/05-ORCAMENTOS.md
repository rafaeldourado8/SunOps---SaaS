# 05 - Contexto: Orçamentos

> **Linguagem Ubíqua:** Kit, Orçamento, Proposta, Item, Cálculo de Geração, Template, Payback

**Fase:** 1 (MVP Core) - ⚠️ **PRIORIDADE MÁXIMA**

---

## Diagrama de Entidades

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONTEXTO ORÇAMENTOS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐         ┌─────────────────┐                │
│  │       KIT       │         │    ORÇAMENTO    │                │
│  │ (Aggregate Root)│         │ (Aggregate Root)│                │
│  └────────┬────────┘         └────────┬────────┘                │
│           │                           │                          │
│           ▼                           ▼                          │
│  ┌─────────────────┐         ┌─────────────────┐                │
│  │    ITEM KIT     │         │   PARÂMETROS    │                │
│  │    (Entity)     │         │    CÁLCULO      │                │
│  └─────────────────┘         │   (Value Obj)   │                │
│                              └────────┬────────┘                │
│                                       │                          │
│                                       ▼                          │
│                              ┌─────────────────┐                │
│                              │   RESULTADO     │                │
│                              │    CÁLCULO      │                │
│                              │   (Value Obj)   │                │
│                              └─────────────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Aggregate Root: Kit

### Kit (Aggregate Root)

Conjunto de produtos que compõem um sistema solar.

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `nome` | String | ✅ | Nome do kit (ex: "Kit 600kWh 4.5 kWp") |
| `descricao` | String | ❌ | Descrição do kit |
| `itens` | List\<ItemKit\> | ✅ | Lista de itens do kit |
| `potenciaTotalKwp` | Decimal | 🔄 Calculado | Soma das potências |
| `geracaoEstimadaKwh` | Decimal | 🔄 Calculado | Geração mensal estimada |
| `valorTotal` | Decimal | 🔄 Calculado | Soma dos valores dos itens |
| `template` | Boolean | ✅ | É template reutilizável? |
| `criadoPor` | UsuarioId | ✅ | Quem criou |
| `dataCriacao` | DateTime | ✅ | Data de criação |
| `dataAtualizacao` | DateTime | ✅ | Última atualização |

---

### ItemKit (Entity)

Produto específico dentro de um kit.

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `produto` | ProdutoId | ✅ | FK para Produto |
| `produtoSnapshot` | ProdutoSnapshot | ✅ | Cópia dos dados do produto |
| `quantidade` | Integer | ✅ | Quantidade do item |
| `precoUnitario` | Decimal | ✅ | Preço no momento da inclusão |
| `precoTotal` | Decimal | 🔄 Calculado | quantidade × precoUnitario |
| `ordem` | Integer | ✅ | Ordem de exibição (drag-drop) |
| `observacao` | String | ❌ | Observação específica |

**Regra:** `precoTotal = quantidade × precoUnitario`

---

## Aggregate Root: Orçamento

### Orcamento (Aggregate Root)

Proposta comercial gerada para um cliente.

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `numero` | String | ✅ | Número sequencial (ex: ORC-2026-0001) |
| `cliente` | ClienteId | ✅ | FK para Cliente |
| `vendedor` | VendedorId | ✅ | FK para Vendedor |
| `kit` | Kit (embedded) | ✅ | Cópia do kit no momento |
| `parametrosCalculo` | ParametrosCalculo | ✅ | Dados de entrada |
| `resultadoCalculo` | ResultadoCalculo | 🔄 Calculado | Resultado dos cálculos |
| `status` | StatusOrcamento | ✅ | Status atual |
| `condicoesComerciais` | CondicoesComerciais | ❌ | Desconto, prazo, etc |
| `dataValidade` | Date | ✅ | Validade da proposta |
| `dataCriacao` | DateTime | ✅ | Data de criação |
| `dataAprovacao` | DateTime | ❌ | Data de aprovação |
| `motivoRejeicao` | String | ❌ | Se rejeitado, por quê |

---

## Value Objects

### ParametrosCalculo (VO)

Dados de entrada para cálculo de geração.

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `consumoMedioKwh` | Decimal | Consumo médio mensal do cliente |
| `tarifaKwh` | Decimal | Valor do kWh da concessionária |
| `orientacaoTelhado` | OrientacaoTelhado | Norte, Sul, Leste, Oeste... |
| `inclinacaoGraus` | Integer | Inclinação do telhado em graus |
| `regiao` | String | Cidade/Estado para irradiação |
| `sombreamento` | NivelSombreamento | Nenhum, Parcial, Significativo |

---

### ResultadoCalculo (VO)

Resultado do cálculo de geração e payback.

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `potenciaSistemaKwp` | Decimal | Potência total do sistema |
| `geracaoMensalKwh` | Decimal | Geração estimada mensal |
| `geracaoAnualKwh` | Decimal | Geração estimada anual |
| `economiaAnualReais` | Decimal | Economia em R$/ano |
| `paybackMeses` | Integer | Tempo de retorno em meses |
| `coberturaConsumo` | Decimal | % do consumo coberto |
| `fatorCapacidade` | Decimal | Fator de capacidade utilizado |

---

### CondicoesComerciais (VO)

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `descontoPercentual` | Decimal | % de desconto aplicado |
| `descontoValor` | Decimal | Desconto em R$ |
| `valorFinal` | Decimal | Valor com desconto |
| `formaPagamento` | FormaPagamento | À vista, Parcelado, Financiamento |
| `parcelas` | Integer | Número de parcelas |
| `taxaFinanciamento` | Decimal | Taxa de juros se financiado |
| `observacoes` | String | Condições especiais |

---

## 🧮 Regras de Cálculo de Geração

### Fórmula Base

```
geracaoPainel = potenciaWp × fatorPerda × diasMes × horasSolPico
```

**Onde:**
- `potenciaWp` = Potência do painel (ex: 700W)
- `fatorPerda` = 0.7 (perdas por temperatura, sujeira, etc)
- `diasMes` = 30 dias
- `horasSolPico` = 4.2h (média Brasil)

**Exemplo:**
```
700W × 0.7 × 30 × 4.2 = 61.74 kWh/mês por painel
```

---

### Cálculo Completo

```
geracaoTotal = geracaoPainel × qtdPaineis × fatorOrientacao × fatorSombreamento
```

---

### Fatores de Orientação

| Orientação | Fator |
|------------|-------|
| Norte | 1.00 |
| Nordeste / Noroeste | 0.95 |
| Leste / Oeste | 0.85 |
| Sudeste / Sudoeste | 0.80 |
| Sul | 0.70 |

---

### Fatores de Sombreamento

| Sombreamento | Fator |
|--------------|-------|
| Nenhum | 1.00 |
| Parcial (até 10%) | 0.90 |
| Significativo (>10%) | 0.75 |

---

### Cálculo de Payback

```
economiaAnual = geracaoAnualKwh × tarifaKwh
paybackMeses = valorSistema / (economiaAnual / 12)
```

**Exemplo:**
```
Geração anual: 7.200 kWh
Tarifa: R$ 0,85/kWh
Economia anual: 7.200 × 0,85 = R$ 6.120

Valor sistema: R$ 25.000
Payback: 25.000 / (6.120 / 12) = 49 meses ≈ 4 anos
```

---

### Cálculo de Cobertura

```
coberturaPercentual = (geracaoMensalKwh / consumoMedioKwh) × 100
```

**Exemplo:**
```
Geração: 600 kWh/mês
Consumo: 500 kWh/mês
Cobertura: (600 / 500) × 100 = 120%
```

---

## Regras de Negócio do Kit

| ID | Regra |
|----|-------|
| RN-KIT-01 | Kit deve ter itens de **no mínimo 2 categorias diferentes** |
| RN-KIT-02 | Potência total é soma das potências de painéis |
| RN-KIT-03 | Estruturas: 1 kit para cada 4 painéis (arredondar para cima) |
| RN-KIT-04 | Cabos padrão: 2 rolos (preto + vermelho) por kit |
| RN-KIT-05 | Template não pode ser editado após uso em orçamento |
| RN-KIT-06 | Preço do item é snapshot (foto) no momento da inclusão |

---

## Sugestões Automáticas

O sistema deve sugerir automaticamente:

### Estruturas
```typescript
function sugerirEstruturas(qtdPaineis: number, tipoTelhado: TipoTelhado): number {
  const kitsPorTipo = {
    CERAMICO: 4,
    FIBROCIMENTO: 4,
    ZINCO: 4,
    LAJE: 4,
    SOLO: 0 // Manual
  };
  
  const paineisporKit = kitsPorTipo[tipoTelhado];
  if (paineisporKit === 0) return 0; // Solo = configuração manual
  
  return Math.ceil(qtdPaineis / paineisporKit);
}
```

### Cabos
```typescript
function sugerirCabos(): { preto: number, vermelho: number } {
  return { preto: 1, vermelho: 1 }; // Sempre 1 de cada
}
```

---

## Enums

```typescript
enum StatusOrcamento {
  EM_ELABORACAO = 'EM_ELABORACAO',
  AGUARDANDO_REVISAO = 'AGUARDANDO_REVISAO',
  AGUARDANDO_CLIENTE = 'AGUARDANDO_CLIENTE',
  APROVADO = 'APROVADO',
  REJEITADO = 'REJEITADO',
  EXPIRADO = 'EXPIRADO'
}

enum OrientacaoTelhado {
  NORTE = 'NORTE',
  SUL = 'SUL',
  LESTE = 'LESTE',
  OESTE = 'OESTE',
  NORDESTE = 'NORDESTE',
  NOROESTE = 'NOROESTE',
  SUDESTE = 'SUDESTE',
  SUDOESTE = 'SUDOESTE'
}

enum NivelSombreamento {
  NENHUM = 'NENHUM',
  PARCIAL = 'PARCIAL',
  SIGNIFICATIVO = 'SIGNIFICATIVO'
}

enum FormaPagamento {
  A_VISTA = 'A_VISTA',
  PARCELADO = 'PARCELADO',
  FINANCIAMENTO = 'FINANCIAMENTO'
}
```

---

## Eventos de Domínio

| Evento | Quando | Dados |
|--------|--------|-------|
| `KitCriado` | Novo kit salvo | kitId, nome, valorTotal |
| `KitAtualizado` | Kit modificado | kitId, camposAlterados |
| `TemplateCriado` | Kit salvo como template | kitId, nome |
| `OrcamentoCriado` | Nova proposta | orcamentoId, clienteId, valorTotal |
| `OrcamentoAprovado` | Cliente aprovou | orcamentoId, dataAprovacao |
| `OrcamentoRejeitado` | Cliente rejeitou | orcamentoId, motivo |
| `OrcamentoExpirado` | Passou validade | orcamentoId |

---

## Exemplo de Uso

```typescript
// Criar kit
const kit = new Kit({
  nome: 'Kit Residencial 600kWh',
  template: true
});

// Adicionar painéis
kit.adicionarItem({
  produto: painelOSDA700W,
  quantidade: 10,
  precoUnitario: 890.00
});

// Adicionar inversor
kit.adicionarItem({
  produto: inversorSolis5kWp,
  quantidade: 1,
  precoUnitario: 3500.00
});

// Sistema valida: tem 2 categorias? ✅
// Sistema calcula automaticamente:
// - potenciaTotalKwp: 7.0 kWp (10 × 700W)
// - valorTotal: R$ 12.400,00

// Criar orçamento
const orcamento = new Orcamento({
  cliente: clienteId,
  vendedor: vendedorId,
  kit: kit.clonar(), // Snapshot do kit
  parametrosCalculo: {
    consumoMedioKwh: 500,
    tarifaKwh: 0.85,
    orientacaoTelhado: 'NORTE',
    sombreamento: 'NENHUM'
  }
});

// Sistema calcula ResultadoCalculo automaticamente
console.log(orcamento.resultadoCalculo);
// {
//   potenciaSistemaKwp: 7.0,
//   geracaoMensalKwh: 617.4,
//   geracaoAnualKwh: 7408.8,
//   economiaAnualReais: 6297.48,
//   paybackMeses: 24,
//   coberturaConsumo: 123.48
// }
```
