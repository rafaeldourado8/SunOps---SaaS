# 02 - Roadmap de Fases

## Visão Geral do Plano de Entrega

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           TIMELINE                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  FASE 1          FASE 2          FASE 3          FASE 4                 │
│  ═══════         ═══════         ═══════         ═══════                │
│  Semanas         Semanas         Semanas         Semanas                │
│   1-8             9-14           15-18           19-26                  │
│                                                                          │
│  ┌───────┐      ┌───────┐      ┌───────┐      ┌───────────┐            │
│  │ MVP   │ ──→  │Vendas │ ──→  │Dashb. │ ──→  │Integrações│            │
│  │ Core  │      │Contrat│      │Suporte│      │    IA     │            │
│  └───────┘      └───────┘      └───────┘      └───────────┘            │
│                                                                          │
│  🔴 CRÍTICA     🟡 ALTA        🟡 ALTA        🟢 MÉDIA                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Resumo das Fases

| Fase | Nome | Duração | Contextos | Entregável Principal |
|------|------|---------|-----------|---------------------|
| **1** | MVP Core | 6-8 sem | Cadastros, Catálogo, Orçamentos | Gerar propostas com cálculos |
| **2** | Vendas | 4-6 sem | Vendas, Contratos | Pipeline e formalização |
| **3** | Dashboard | 4 sem | Relatórios, Suporte básico | Visão gerencial |
| **4** | Integrações | 6-8 sem | Monitoramento, IA, Marketing | Automação completa |

---

## FASE 1: MVP Core (Semanas 1-8)

### 🎯 Objetivo
> Sistema funcional para criar kits, calcular geração e gerar propostas comerciais.

### Contextos
- ✅ Cadastros (completo)
- ✅ Catálogo (completo)
- ✅ Orçamentos (completo)

### Funcionalidades

| ID | Funcionalidade | Prioridade |
|----|----------------|------------|
| F1.01 | CRUD Clientes | Essencial |
| F1.02 | CRUD Vendedores | Essencial |
| F1.03 | CRUD Fornecedores | Essencial |
| F1.04 | CRUD Produtos (Painel, Inversor, Estrutura, Cabo, Conector) | Essencial |
| F1.05 | CRUD Marcas | Essencial |
| F1.06 | Cotação de Preços (validade 3 dias) | Essencial |
| F1.07 | Alerta de Cotação (segunda-feira) | Importante |
| F1.08 | Monte Seu Kit (drag-and-drop) | Essencial |
| F1.09 | Templates de Kit reutilizáveis | Essencial |
| F1.10 | Cálculo de Geração (kWh/mês) | Essencial |
| F1.11 | Cálculo de Payback | Essencial |
| F1.12 | Criar Orçamento | Essencial |
| F1.13 | Exportar PDF do Orçamento | Essencial |
| F1.14 | Dashboard Básico | Importante |
| F1.15 | Login/Autenticação | Essencial |

### Sprints

| Sprint | Semanas | Entregas |
|--------|---------|----------|
| 1 | 1-2 | Setup + CRUD Clientes + Vendedores + Auth |
| 2 | 3-4 | CRUD Fornecedores + Marcas + Produtos (base) |
| 3 | 5-6 | Produtos especializados + Cotação + Alerta |
| 4 | 7-8 | Monte Seu Kit + Cálculos + PDF + Dashboard |

### ✅ Critérios de Aceite
- [ ] Cadastrar cliente com todos os dados
- [ ] Cadastrar produto com preço e fornecedor
- [ ] Sistema calcula validade de 3 dias úteis
- [ ] Alerta de cotação segunda-feira
- [ ] Montar kit com mínimo 2 categorias
- [ ] Calcular potência (kWp) e geração (kWh)
- [ ] Calcular payback
- [ ] Gerar PDF do orçamento

---

## FASE 2: Vendas e Contratos (Semanas 9-14)

### 🎯 Objetivo
> Transformar orçamentos aprovados em vendas e formalizar em contratos.

### Contextos
- ✅ Vendas (completo)
- ✅ Contratos (completo)
- 🔄 Cadastros (extensão: Integradores)

### Funcionalidades

| ID | Funcionalidade | Prioridade |
|----|----------------|------------|
| F2.01 | CRUD Integradores | Importante |
| F2.02 | Converter Orçamento → Venda | Essencial |
| F2.03 | Pipeline de Vendas (Kanban) | Essencial |
| F2.04 | Registrar Perda (motivo obrigatório) | Essencial |
| F2.05 | Histórico de Vendas | Importante |
| F2.06 | Gerar Contrato | Essencial |
| F2.07 | Parcelas do Contrato | Essencial |
| F2.08 | Relatório de Vendas | Essencial |
| F2.09 | Relatório por Vendedor | Importante |
| F2.10 | Meta de Vendas | Desejável |

### Sprints

| Sprint | Semanas | Entregas |
|--------|---------|----------|
| 5 | 9-10 | Integradores + Conversão Orçamento→Venda |
| 6 | 11-12 | Pipeline Kanban + Histórico + Perda |
| 7 | 13-14 | Contratos + Parcelas + Relatórios |

---

## FASE 3: Dashboard Completo (Semanas 15-18)

### 🎯 Objetivo
> Visão gerencial completa com indicadores e suporte básico.

### Contextos
- ✅ Dashboard/Relatórios (novo)
- ✅ Suporte (básico)

### Funcionalidades

| ID | Funcionalidade | Prioridade |
|----|----------------|------------|
| F3.01 | Dashboard Executivo | Essencial |
| F3.02 | Gráfico de Vendas (evolução) | Essencial |
| F3.03 | Funil Visual | Importante |
| F3.04 | Ranking Vendedores | Importante |
| F3.05 | Abertura de Ticket | Essencial |
| F3.06 | Gestão de Tickets | Essencial |
| F3.07 | Link de Acompanhamento (garantia) | Importante |
| F3.08 | Exportar Relatórios (PDF/Excel) | Importante |
| F3.09 | Filtros Avançados | Importante |

### Sprints

| Sprint | Semanas | Entregas |
|--------|---------|----------|
| 8 | 15-16 | Dashboard + Gráficos + KPIs |
| 9 | 17-18 | Tickets + Suporte + Exportação |

---

## FASE 4: Integrações e IA (Semanas 19-26)

### 🎯 Objetivo
> Automatizar atendimento com IA e integrar monitoramento de inversores.

### Contextos
- ✅ Monitoramento (completo)
- ✅ Agentes IA (completo)
- ✅ Marketing (básico)

### Funcionalidades

| ID | Funcionalidade | Prioridade |
|----|----------------|------------|
| F4.01 | Integração SolisCloud | Alta |
| F4.02 | Integração Growatt | Alta |
| F4.03 | Integração Solarman | Média |
| F4.04 | Detecção de Falhas | Alta |
| F4.05 | Regra dos 2 Dias | Essencial |
| F4.06 | Revisão de Mensagem (admin) | Essencial |
| F4.07 | Agente de Vendas (WhatsApp) | Alta |
| F4.08 | Configurar Agente | Alta |
| F4.09 | Takeover Humano | Essencial |
| F4.10 | Histórico de Conversas | Essencial |
| F4.11 | Agente de Suporte | Média |
| F4.12 | Ensino de Monitoramento | Média |
| F4.13 | Campanhas de Marketing | Baixa |

### Sprints

| Sprint | Semanas | Entregas |
|--------|---------|----------|
| 10 | 19-20 | Integração SolisCloud + Alertas |
| 11 | 21-22 | Integração Growatt/Solarman |
| 12 | 23-24 | Agente de Vendas + Configuração |
| 13 | 25-26 | Agente Suporte + Marketing + Ajustes |

---

## Dependências

```
FASE 1 ──────┬──→ FASE 2 ──→ FASE 4
             │
             └──→ FASE 3 ──→ FASE 4
```

- **Fase 1** é pré-requisito para todas
- **Fase 2** depende de Fase 1 (Orçamento → Venda)
- **Fase 3** pode iniciar em paralelo com Fase 2
- **Fase 4** depende de Fases 1 e 2 completas

---

## Marcos (Milestones)

| Marco | Data Estimada | Entregável |
|-------|---------------|------------|
| M1 | Semana 8 | MVP funcionando - Gerar orçamentos |
| M2 | Semana 14 | Pipeline de vendas completo |
| M3 | Semana 18 | Dashboard gerencial |
| M4 | Semana 26 | Sistema completo com IA |
