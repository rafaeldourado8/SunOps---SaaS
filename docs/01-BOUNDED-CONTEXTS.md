# 01 - Bounded Contexts

## Visão Geral

O SunwOps é dividido em **9 Bounded Contexts**, cada um com sua própria linguagem ubíqua e responsabilidades.

---

## Mapa de Contextos

| # | Contexto | Responsabilidade | Fase |
|---|----------|------------------|------|
| 1 | **Cadastros (Identity)** | Gestão de pessoas: clientes, vendedores, integradores, fornecedores | 1 |
| 2 | **Catálogo** | Produtos solares: painéis, inversores, estruturas, cabos, conectores | 1 |
| 3 | **Orçamentos** | Montagem de kits, cálculos de geração, propostas comerciais | 1 |
| 4 | **Vendas** | Pipeline comercial, funil de vendas, conversão | 2 |
| 5 | **Contratos** | Formalização, assinaturas, documentos legais | 2 |
| 6 | **Suporte** | Tickets, garantias, atendimento ao cliente | 3 |
| 7 | **Monitoramento** | Integração com inversores, detecção de falhas | 4 |
| 8 | **Agentes IA** | Chatbots de vendas, suporte e marketing | 4 |
| 9 | **Marketing** | Campanhas, automações, comunicação | 4 |

---

## Relações entre Contextos

### Fluxo de Dados (Upstream → Downstream)

```
Cadastros ──────┬──→ Orçamentos
                ├──→ Vendas
                ├──→ Suporte
                └──→ Contratos

Catálogo ───────────→ Orçamentos

Orçamentos ─────────→ Vendas

Vendas ─────────────→ Contratos

Contratos ──────────→ Suporte

Monitoramento ──────→ Suporte

Agentes IA ─────┬──→ Vendas
                ├──→ Suporte
                └──→ Marketing
```

---

## Tipos de Integração

| De | Para | Padrão | Mecanismo |
|----|------|--------|-----------|
| Cadastros | Todos | **Shared Kernel** | Entidades compartilhadas via ID |
| Catálogo | Orçamentos | **Customer-Supplier** | API síncrona |
| Orçamentos | Vendas | **Customer-Supplier** | Evento de domínio |
| Monitoramento | Suporte | **Published Language** | Eventos assíncronos (fila) |
| Agentes IA | Vendas | **Anti-Corruption Layer** | Adapter para cada plataforma |

---

## Linguagem Ubíqua por Contexto

### Cadastros
> Cliente, Vendedor, Integrador, Fornecedor, Pessoa, Documento, Endereço

### Catálogo
> Produto, Painel, Inversor, Estrutura, Cabo, Conector, Marca, Cotação, Preço

### Orçamentos
> Kit, Orçamento, Proposta, Item, Cálculo de Geração, Template, Payback

### Vendas
> Venda, Oportunidade, Pipeline, Funil, Etapa, Conversão, Perda

### Contratos
> Contrato, Parcela, Assinatura, Garantia, Instalação

### Suporte
> Ticket, Atendimento, Solução, SLA, Prioridade

### Monitoramento
> Planta, Inversor, Alerta, Falha, Geração, Status

### Agentes IA
> Agente, Conversa, Mensagem, Takeover, Configuração

### Marketing
> Campanha, Lead, Automação, Sequência

---

## Regra de Ouro

> **Cada contexto é independente.** 
> 
> Mudanças em um contexto não devem quebrar outros.
> Comunicação entre contextos é feita por eventos ou APIs bem definidas.
