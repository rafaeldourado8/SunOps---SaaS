# 06 - Contexto: Vendas

> **Linguagem Ubíqua:** Venda, Oportunidade, Pipeline, Funil, Etapa, Conversão, Perda

**Fase:** 2

---

## Diagrama de Entidades

```
┌─────────────────────────────────────────────────────────────────┐
│                      CONTEXTO VENDAS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐                                            │
│  │      VENDA      │                                            │
│  │ (Aggregate Root)│                                            │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐         ┌─────────────────┐                │
│  │   HISTÓRICO     │         │  MOTIVO PERDA   │                │
│  │     VENDA       │         │   (Value Obj)   │                │
│  │    (Entity)     │         └─────────────────┘                │
│  └─────────────────┘                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

                         FUNIL DE VENDAS
                         
    ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
    │  LEAD   │ → │QUALIFIC.│ → │PROPOSTA │ → │NEGOCIAC.│ → │FECHAMEN.│
    └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
         │             │             │             │             │
         └─────────────┴─────────────┴─────────────┴─────────────┘
                                    │
                                    ▼
                              ┌───────────┐
                              │  PERDIDA  │ (com motivo obrigatório)
                              └───────────┘
```

---

## Aggregate Root: Venda

### Venda (Aggregate Root)

Representa uma oportunidade de negócio do início ao fechamento.

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `numero` | String | ✅ | Número sequencial (ex: VND-2026-0001) |
| `cliente` | ClienteId | ✅ | FK para Cliente |
| `vendedor` | VendedorId | ✅ | FK para Vendedor |
| `orcamento` | OrcamentoId | ❌ | FK para Orçamento (se houver) |
| `status` | StatusVenda | ✅ | Aberta, Fechada, Perdida |
| `etapaFunil` | EtapaFunil | ✅ | Etapa atual no pipeline |
| `valorPrevisto` | Decimal | ❌ | Valor estimado |
| `probabilidade` | Integer | ❌ | % de chance (0-100) |
| `dataPrevisaoFechamento` | Date | ❌ | Quando espera fechar |
| `dataCriacao` | DateTime | ✅ | Data de criação |
| `dataFechamento` | DateTime | ❌ | Data de fechamento efetivo |
| `motivoPerda` | MotivoPerda | ⚠️ Condicional | **Obrigatório se status = PERDIDA** |
| `historico` | List\<HistoricoVenda\> | ✅ | Todas as mudanças |

---

### HistoricoVenda (Entity)

Registra todas as mudanças de status/etapa.

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `venda` | VendaId | ✅ | FK para Venda |
| `statusAnterior` | StatusVenda | ❌ | Status antes |
| `statusNovo` | StatusVenda | ✅ | Novo status |
| `etapaAnterior` | EtapaFunil | ❌ | Etapa antes |
| `etapaNova` | EtapaFunil | ✅ | Nova etapa |
| `observacao` | String | ❌ | Comentário do vendedor |
| `dataOcorrencia` | DateTime | ✅ | Quando ocorreu |
| `usuario` | UsuarioId | ✅ | Quem fez a mudança |

---

## Value Objects

### MotivoPerda (VO)

**⚠️ Obrigatório quando venda é marcada como PERDIDA.**

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `categoria` | CategoriaPerda | Preço, Concorrência, Desistência... |
| `descricao` | String | Descrição detalhada (**obrigatório**) |
| `concorrente` | String | Nome do concorrente (se aplicável) |

```typescript
class MotivoPerda {
  constructor(categoria: CategoriaPerda, descricao: string, concorrente?: string) {
    if (!descricao || descricao.trim().length < 10) {
      throw new Error('Descrição do motivo deve ter pelo menos 10 caracteres');
    }
    this.categoria = categoria;
    this.descricao = descricao;
    this.concorrente = concorrente;
  }
}
```

---

## Enums

```typescript
enum StatusVenda {
  ABERTA = 'ABERTA',
  FECHADA = 'FECHADA',
  PERDIDA = 'PERDIDA'
}

enum EtapaFunil {
  LEAD = 'LEAD',                    // Novo contato
  QUALIFICACAO = 'QUALIFICACAO',    // Entendendo necessidade
  PROPOSTA = 'PROPOSTA',            // Orçamento enviado
  NEGOCIACAO = 'NEGOCIACAO',        // Negociando valores/condições
  FECHAMENTO = 'FECHAMENTO'         // Aguardando assinatura
}

enum CategoriaPerda {
  PRECO = 'PRECO',                  // Achou caro
  CONCORRENCIA = 'CONCORRENCIA',    // Fechou com outro
  DESISTENCIA = 'DESISTENCIA',      // Desistiu de instalar
  PRAZO = 'PRAZO',                  // Prazo não atendeu
  FINANCEIRO = 'FINANCEIRO',        // Não conseguiu financiamento
  TECNICO = 'TECNICO',              // Problema técnico (telhado, etc)
  OUTRO = 'OUTRO'
}
```

---

## Pipeline Visual (Kanban)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PIPELINE DE VENDAS                              │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────────────────┤
│    LEAD     │ QUALIFICAÇÃO│  PROPOSTA   │ NEGOCIAÇÃO  │    FECHAMENTO       │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────────────┤
│             │             │             │             │                     │
│ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐ │   ┌─────────┐      │
│ │ João S. │ │ │ Maria L.│ │ │ Pedro R.│ │ │ Ana C.  │ │   │ Carlos M│      │
│ │ R$15mil │ │ │ R$22mil │ │ │ R$18mil │ │ │ R$35mil │ │   │ R$28mil │      │
│ │  20%    │ │ │  40%    │ │ │  60%    │ │ │  80%    │ │   │  95%    │      │
│ └─────────┘ │ └─────────┘ │ └─────────┘ │ └─────────┘ │   └─────────┘      │
│             │             │             │             │                     │
│ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐ │             │                     │
│ │ Rita P. │ │ │ José F. │ │ │ Lucia M.│ │             │                     │
│ │ R$12mil │ │ │ R$45mil │ │ │ R$20mil │ │             │                     │
│ │  20%    │ │ │  40%    │ │ │  60%    │ │             │                     │
│ └─────────┘ │ └─────────┘ │ └─────────┘ │             │                     │
│             │             │             │             │                     │
├─────────────┴─────────────┴─────────────┴─────────────┴─────────────────────┤
│ Total: R$ 195.000                                      Previsão: R$ 95.000  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Fluxo de Estados

```
                    ┌──────────────────────────────────────────┐
                    │                                          │
                    ▼                                          │
    ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
    │  LEAD   │ → │QUALIFIC.│ → │PROPOSTA │ → │NEGOCIAC.│ → │FECHAMEN.│
    └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘
         │             │             │             │             │
         │             │             │             │             ▼
         │             │             │             │      ┌─────────────┐
         │             │             │             │      │   FECHADA   │
         │             │             │             │      │  (Sucesso)  │
         │             │             │             │      └─────────────┘
         │             │             │             │
         └─────────────┴─────────────┴─────────────┴─────────────┐
                                                                 │
                                                                 ▼
                                                          ┌─────────────┐
                                                          │   PERDIDA   │
                                                          │ (c/ motivo) │
                                                          └─────────────┘
```

---

## Regras de Negócio

| ID | Regra |
|----|-------|
| RN-VND-01 | Venda **PERDIDA** exige motivo obrigatório com descrição |
| RN-VND-02 | Toda mudança de status/etapa gera registro no histórico |
| RN-VND-03 | Apenas admin pode reabrir venda perdida |
| RN-VND-04 | Venda criada a partir de orçamento herda o valor |
| RN-VND-05 | Probabilidade sugerida por etapa: Lead=20%, Qualif=40%, Proposta=60%, Negoc=80%, Fech=95% |

---

## Conversão de Orçamento para Venda

Quando um orçamento é **APROVADO**, o sistema deve:

1. Criar nova Venda com status `ABERTA`
2. Vincular orçamento à venda (`orcamentoId`)
3. Copiar valor do orçamento para `valorPrevisto`
4. Definir etapa como `PROPOSTA` (já tem proposta aprovada)
5. Emitir evento `VendaCriadaDeOrcamento`

```typescript
// Evento: OrcamentoAprovado
function onOrcamentoAprovado(evento: OrcamentoAprovado) {
  const venda = new Venda({
    cliente: evento.clienteId,
    vendedor: evento.vendedorId,
    orcamento: evento.orcamentoId,
    status: StatusVenda.ABERTA,
    etapaFunil: EtapaFunil.PROPOSTA,
    valorPrevisto: evento.valorTotal,
    probabilidade: 60
  });
  
  vendaRepository.save(venda);
  eventBus.publish(new VendaCriadaDeOrcamento(venda.id));
}
```

---

## Eventos de Domínio

| Evento | Quando | Dados |
|--------|--------|-------|
| `VendaAberta` | Nova venda criada | vendaId, clienteId, vendedorId |
| `VendaMudouEtapa` | Moveu no funil | vendaId, etapaAnterior, etapaNova |
| `VendaFechada` | Status = FECHADA | vendaId, valorFinal, dataFechamento |
| `VendaPerdida` | Status = PERDIDA | vendaId, motivoPerda |
| `VendaCriadaDeOrcamento` | Veio de orçamento aprovado | vendaId, orcamentoId |

---

## Relatórios

### Relatório de Vendas por Status

```sql
SELECT 
  status,
  COUNT(*) as quantidade,
  SUM(valor_previsto) as valor_total
FROM vendas
WHERE data_criacao BETWEEN :inicio AND :fim
GROUP BY status
```

### Relatório de Vendas Perdidas por Motivo

```sql
SELECT 
  motivo_perda_categoria as categoria,
  COUNT(*) as quantidade,
  SUM(valor_previsto) as valor_perdido
FROM vendas
WHERE status = 'PERDIDA'
  AND data_fechamento BETWEEN :inicio AND :fim
GROUP BY motivo_perda_categoria
ORDER BY quantidade DESC
```

### Relatório por Vendedor

```sql
SELECT 
  v.nome as vendedor,
  COUNT(CASE WHEN vd.status = 'FECHADA' THEN 1 END) as fechadas,
  COUNT(CASE WHEN vd.status = 'PERDIDA' THEN 1 END) as perdidas,
  COUNT(CASE WHEN vd.status = 'ABERTA' THEN 1 END) as abertas,
  SUM(CASE WHEN vd.status = 'FECHADA' THEN vd.valor_previsto ELSE 0 END) as valor_fechado
FROM vendas vd
JOIN vendedores v ON vd.vendedor_id = v.id
WHERE vd.data_criacao BETWEEN :inicio AND :fim
GROUP BY v.id, v.nome
ORDER BY valor_fechado DESC
```
