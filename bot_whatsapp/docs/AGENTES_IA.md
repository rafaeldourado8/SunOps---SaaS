# 🤖 Especificação dos Agentes IA - SunOps

## 📋 Visão Geral

Sistema de agentes IA especializados para atendimento via WhatsApp com foco em vendas e suporte técnico de energia solar.

---

## 🎯 BOT DE VENDAS (Agente de Vendas IA)

### 1. Configuração e Treinamento

| Função | Descrição Detalhada |
|--------|---------------------|
| **Treinamento via prints de WhatsApp** | O bot deve ser configurável através de capturas de tela de conversas reais do WhatsApp, aprendendo padrões de atendimento da empresa |
| **Treinamento via textos** | Aceitar documentos de texto com scripts, FAQs, informações de produtos e políticas da empresa |
| **Treinamento via áudios** | Processar arquivos de áudio para extrair padrões de comunicação e informações |
| **Regras customizáveis por empresa** | Cada empresa pode definir regras específicas de atendimento |
| **Adicionar/remover regras** | Interface para gerenciar dinamicamente as regras do agente |

### 2. Atendimento e Comunicação

| Função | Descrição Detalhada |
|--------|---------------------|
| **Linguagem humanizada e natural** | O bot deve conversar como uma pessoa real, sem parecer robótico |
| **Manutenção de contexto** | Lembrar todo o histórico da conversa e não perder o fio da discussão |
| **Não sair do escopo** | Manter-se estritamente dentro dos temas configurados, sem desviar para assuntos não relacionados |
| **Não alucinar** | Nunca inventar informações que não foram configuradas. Se não souber, deve informar que vai verificar |
| **Compreender mensagens de áudio** | Transcrever e entender áudios enviados pelos clientes (desejável) |
| **Múltiplos atendentes assíncronos** | Vários bots funcionando simultaneamente atendendo diferentes clientes |

### 3. Montagem de Orçamentos

| Função | Descrição Detalhada |
|--------|---------------------|
| **Perguntas-chave configuráveis** | Fazer perguntas específicas para coletar informações do cliente (consumo, tipo de telhado, localização, etc.) |
| **Gerar orçamentos automaticamente** | Com base nas respostas, montar orçamentos completos com kits adequados |
| **Gerar PDF do orçamento** | Converter orçamento em documento PDF profissional |
| **Enviar para revisão** | Antes de enviar ao cliente, o PDF vai para aprovação do administrador |

### 4. Transferência para Humano

| Função | Descrição Detalhada |
|--------|---------------------|
| **Botão de controle pelo admin** | O administrador pode assumir a conversa a qualquer momento clicando em um botão |
| **Transição imperceptível** | O cliente não deve perceber que trocou de atendente (IA → humano) |
| **Visualização em tempo real** | Administradores podem acompanhar os chats do bot enquanto ocorrem |

### 5. Histórico e Relatórios

| Função | Descrição Detalhada |
|--------|---------------------|
| **Guardar histórico completo** | Todas as conversas ficam salvas permanentemente |
| **Relatório de conversas** | Gerar relatórios para análise posterior do atendimento |
| **Interação com outros agentes** | Possibilidade de comunicar-se com bot de suporte ou marketing (desejável) |

---

## 🛠️ BOT DE SUPORTE (Agente de Suporte IA)

### 1. Gestão de Tickets

| Função | Descrição Detalhada |
|--------|---------------------|
| **Gerar ID único por atendimento** | Cada ticket recebe um identificador único para rastreamento |
| **Relatório de ocorrências** | Gerar relatórios de todos os atendimentos realizados |
| **Relatório de tickets** | Listar tickets com status, tipo, data, resolução |

### 2. Gestão de Garantias

| Função | Descrição Detalhada |
|--------|---------------------|
| **Base única de clientes** | Acessar dados pessoais do cliente compartilhados entre módulos |
| **Histórico de reclamações** | Guardar todo histórico de conversas e reclamações anteriores |
| **Atualização de status** | Informar ao cliente automaticamente o andamento da garantia |
| **Atendimento humanizado com empatia** | Usar tom paciente, compreensivo e acolhedor |
| **Gerar link único de acompanhamento** | Criar URL criptografada para o cliente visualizar status da garantia |
| **Acesso via ID do ticket** | O link é acessado usando o número do ticket |
| **Analogias simples para leigos/idosos** | Explicar termos técnicos de forma simples e acessível (desejável) |

### 3. Monitoramento de Falhas em Inversores

| Função | Descrição Detalhada |
|--------|---------------------|
| **Integração com SolisCloud** | Conectar à API da plataforma Solis para monitorar inversores |
| **Integração com Growatt/ShinePhone** | Conectar à API da plataforma Growatt |
| **Integração com Solarman Business/Smart** | Conectar à API da plataforma Solarman |
| **Streaming de eventos em tempo real** | Receber notificações contínuas do status dos inversores |
| **Pesquisa automática sobre falhas** | Ao detectar erro, buscar automaticamente informações sobre o problema |
| **Identificar causa e solução** | Diagnosticar o problema e sugerir como resolver |
| **Aguardar 2 dias antes de notificar** | Não alarmar o cliente imediatamente; esperar para ver se o problema persiste |
| **Mensagem após 2 dias offline** | Se o sistema continuar offline, preparar mensagem ao cliente |
| **Mensagem educada e empática** | Tom de comunicação paciente e compreensivo |
| **Revisão antes do envio** | Toda mensagem automática passa pelo administrador antes de ser enviada |
| **Proteger a empresa** | Em erros internos, não declarar culpa diretamente, mas também não mentir |

### 4. Ensino de Monitoramento

| Função | Descrição Detalhada |
|--------|---------------------|
| **Ensinar uso do monitoramento** | Orientar o cliente sobre como usar os apps de monitoramento (ShinePhone, SolisCloud, etc.) |
| **Paciência especial com idosos** | Explicar de forma mais lenta, com repetições e linguagem simples |
| **Escalar para administrador** | Se não conseguir resolver remotamente, avisar o admin para intervenção manual |

---

## 📊 QUADRO COMPARATIVO: VENDAS vs SUPORTE

| Característica | Bot de Vendas | Bot de Suporte |
|----------------|---------------|----------------|
| **Foco principal** | Converter leads em vendas | Resolver problemas técnicos |
| **Gera orçamentos** | ✅ Sim | ❌ Não |
| **Monitora inversores** | ❌ Não | ✅ Sim |
| **Gestão de garantias** | ❌ Não | ✅ Sim |
| **Gera tickets** | ❌ Não | ✅ Sim |
| **Integrações** | WhatsApp | WhatsApp + APIs de monitoramento |
| **Ensina uso de apps** | ❌ Não | ✅ Sim |
| **Tempo de espera antes de agir** | Imediato | 2 dias (para falhas) |
| **Transferência para humano** | ✅ Botão instantâneo | ✅ Quando não resolver remotamente |
| **Linguagem** | Comercial/Persuasiva | Técnica/Empática |

---

## 🔐 REGRAS COMUNS A AMBOS OS BOTS

### Princípios Fundamentais

1. **Nunca alucinar** — Não inventar informações
2. **Manter contexto** — Lembrar toda a conversa
3. **Não sair do escopo** — Ficar apenas nos temas configurados
4. **Linguagem humanizada** — Parecer uma pessoa real
5. **Histórico completo** — Salvar todas as conversas
6. **Revisão pelo admin** — Mensagens críticas passam por aprovação
7. **Transição imperceptível** — Cliente não percebe troca para humano

---

## 🏗️ ARQUITETURA DE IMPLEMENTAÇÃO

### Stack Tecnológica

```
WhatsApp → Node.js Gateway → RabbitMQ → FastAPI AI Agents
                                              ↓
                                    Gemini Flash (preprocessamento)
                                              ↓
                                    Redis Cache (80% economia)
                                              ↓
                                    Gemini Pro (resposta final)
                                              ↓
                                    RabbitMQ (whatsapp_responses)
                                              ↓
                                    Node.js Gateway → WhatsApp
```

### Componentes Principais

#### 1. Preprocessamento (Gemini Flash)
- Extração de intent
- Classificação de tipo de atendimento (vendas/suporte)
- Identificação de urgência
- Detecção de transferência para humano

#### 2. Cache (Redis)
- TTL: 1 hora para respostas comuns
- TTL: 24 horas para informações de produtos
- TTL: 7 dias para FAQs
- Economia estimada: 80% de tokens

#### 3. Processamento Principal (Gemini Pro)
- Geração de respostas contextualizadas
- Montagem de orçamentos
- Diagnóstico de problemas técnicos
- Geração de relatórios

#### 4. Persistência (PostgreSQL)
- Histórico de conversas
- Tickets de suporte
- Orçamentos gerados
- Regras de negócio por empresa
- Dados de clientes e garantias

#### 5. Monitoramento (APIs Externas)
- SolisCloud API
- Growatt API
- Solarman API
- Webhooks para eventos em tempo real

---

## 📁 ESTRUTURA DE DADOS

### Conversa
```python
{
  "id": "uuid",
  "cliente_id": "uuid",
  "agente_tipo": "vendas|suporte",
  "status": "ativo|transferido|finalizado",
  "mensagens": [...],
  "contexto": {...},
  "criado_em": "timestamp",
  "atualizado_em": "timestamp"
}
```

### Ticket (Suporte)
```python
{
  "id": "TKT-2024-0001",
  "cliente_id": "uuid",
  "tipo": "garantia|falha|duvida",
  "status": "aberto|aguardando|resolvido|fechado",
  "prioridade": "baixa|media|alta|urgente",
  "descricao": "texto",
  "historico": [...],
  "link_acompanhamento": "url_criptografada",
  "criado_em": "timestamp"
}
```

### Orçamento (Vendas)
```python
{
  "id": "uuid",
  "cliente_id": "uuid",
  "conversa_id": "uuid",
  "kit_id": "uuid",
  "valor_total": "decimal",
  "status": "rascunho|revisao|aprovado|enviado",
  "pdf_url": "url",
  "aprovado_por": "admin_id",
  "criado_em": "timestamp"
}
```

### Regra de Negócio
```python
{
  "id": "uuid",
  "empresa_id": "uuid",
  "agente_tipo": "vendas|suporte",
  "tipo": "texto|audio|imagem",
  "conteudo": "...",
  "ativo": "boolean",
  "prioridade": "integer",
  "criado_em": "timestamp"
}
```

---

## 🎯 ROADMAP DE IMPLEMENTAÇÃO

### Fase 1: Base (2 semanas)
- [ ] Estrutura de agentes base
- [ ] Integração Gemini Flash + Pro
- [ ] Sistema de cache Redis
- [ ] Persistência de conversas

### Fase 2: Bot de Vendas (3 semanas)
- [ ] Treinamento via textos/prints/áudios
- [ ] Sistema de perguntas configuráveis
- [ ] Geração de orçamentos
- [ ] Geração de PDF
- [ ] Fluxo de aprovação

### Fase 3: Bot de Suporte (4 semanas)
- [ ] Sistema de tickets
- [ ] Gestão de garantias
- [ ] Integração SolisCloud API
- [ ] Integração Growatt API
- [ ] Integração Solarman API
- [ ] Sistema de notificações (2 dias)

### Fase 4: Transferência Humana (1 semana)
- [ ] Dashboard admin em tempo real
- [ ] Botão de assumir conversa
- [ ] Transição imperceptível
- [ ] Histórico unificado

### Fase 5: Relatórios e Analytics (2 semanas)
- [ ] Relatórios de conversas
- [ ] Relatórios de tickets
- [ ] Métricas de performance
- [ ] Dashboard executivo

---

## 💰 ESTIMATIVA DE CUSTOS (Gemini)

### Sem Otimização
- Gemini Pro: $0.50/1M tokens input, $1.50/1M tokens output
- Média: 1000 tokens/conversa
- 1000 conversas/dia = $20/dia = **$600/mês**

### Com Otimização (Flash + Cache)
- Gemini Flash: $0.075/1M tokens (85% das requisições)
- Cache Redis: 80% de economia
- Gemini Pro: 15% das requisições
- Custo estimado: **$120/mês** (economia de $480/mês)

---

## 🔒 SEGURANÇA E COMPLIANCE

- Criptografia de dados sensíveis (LGPD)
- Links de acompanhamento com tokens únicos
- Logs de auditoria para todas as ações
- Backup automático de conversas
- Retenção de dados configurável por empresa
