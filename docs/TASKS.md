# 📋 TASKS - SunOps MAB

## 🎯 OBJETIVO
Transformar o protótipo em sistema funcional completo, sem dados mock, com todas as features implementadas.

---

## 1️⃣ INFRAESTRUTURA & AUTENTICAÇÃO

### 1.1 Backend - Autenticação
- [x] Django Admin configurado
- [x] Migrations aplicadas
- [x] Superuser criado
- [x] Endpoint `/api/v1/auth/login` retornando token JWT
- [x] Endpoint `/api/v1/auth/me` validando token
- [x] Frontend salvando token no localStorage
- [x] Frontend enviando token em todas requisições
- [x] Teste: Login com admin@sunops.com / admin123
- [x] Teste: Acesso ao dashboard após login

### 1.2 Backend - FastAPI Base
- [x] FastAPI rodando na porta 8001
- [x] Endpoint `/health` retornando status
- [x] Conexão com PostgreSQL validada
- [x] Conexão com Redis validada
- [x] Conexão com RabbitMQ validada
- [x] Teste: `curl http://localhost:8001/health`
- [x] Teste: `docker-compose exec api python -c "from src.adapters.infrastructure.database.config import engine; print('DB OK')"`

---

## 2️⃣ CANVAS DE WORKFLOWS (FEATURE CENTRAL)

### 2.1 Backend - Workflows
- [x] Model `Workflow` (id, name, user_id, data_json, created_at, updated_at)
- [x] Model `WorkflowExecution` (id, workflow_id, status, started_at, finished_at, logs)
- [x] Endpoint `POST /api/v1/workflows` - Criar workflow
- [x] Endpoint `GET /api/v1/workflows` - Listar workflows
- [x] Endpoint `GET /api/v1/workflows/{id}` - Buscar workflow
- [x] Endpoint `PUT /api/v1/workflows/{id}` - Atualizar workflow
- [x] Endpoint `DELETE /api/v1/workflows/{id}` - Deletar workflow
- [x] Endpoint `POST /api/v1/workflows/{id}/execute` - Executar workflow
- [x] Endpoint `GET /api/v1/workflows/{id}/executions` - Histórico de execuções
- [x] Teste: Criar workflow via API
- [x] Teste: Executar workflow e verificar logs

### 2.2 Frontend - Canvas
- [x] Remover dados mock do WorkflowCanvas
- [x] Integrar com API para salvar workflow
- [x] Botão "Salvar" funcionando
- [x] Botão "Executar" funcionando
- [ ] Botão "Histórico" mostrando execuções
- [ ] Validação: nodes obrigatórios configurados
- [ ] Validação: sem ciclos inválidos
- [ ] Status em tempo real dos nodes
- [x] Teste: Criar workflow no canvas e salvar
- [x] Teste: Executar workflow e ver resultado

### 2.3 Sistema de Nodes
- [x] Model `Node` (nodes salvos dentro de workflow.data_json)
- [x] Tipos: agent_vendas, agent_suporte, whatsapp, inversor, pdf_generator
- [x] Endpoint `GET /api/v1/workflows/node-types` - Listar tipos
- [x] Frontend: NodePalette com tipos reais
- [x] Frontend: ConfigPanel salvando configurações
- [x] Teste: Arrastar node para canvas
- [x] Teste: Configurar node e salvar

---

## 3️⃣ AGENTE DE VENDAS

### 3.1 Backend - Agente de Vendas
- [x] Model `Conversation` (id, phone, agent_type, context_json, created_at)
- [x] Model `Message` (id, conversation_id, role, content, created_at)
- [x] Service `VendasAgent` integrado com Gemini
- [x] Manutenção de contexto por cliente
- [x] Coleta de dados guiada
- [x] Geração de orçamento automático
- [x] Endpoint `POST /api/v1/agents/vendas/config` - Configurar agente
- [x] Endpoint `GET /api/v1/agents/vendas/metrics` - Métricas do agente
- [x] Teste: Enviar mensagem e receber resposta contextualizada
- [x] Teste: Gerar orçamento após coleta de dados

### 3.2 Frontend - Agente de Vendas
- [x] Node "Bot de Vendas" no canvas
- [x] ConfigPanel com:
  - [x] Seleção de modelo IA
  - [x] Prompt de sistema customizável
  - [x] Regras de negócio
- [x] Métricas em tempo real
- [x] Teste: Configurar agente no canvas
- [x] Teste: Ver métricas atualizando

---

## 4️⃣ AGENTE DE SUPORTE

### 4.1 Backend - Agente de Suporte
- [x] Model `Ticket` (id, ticket_number, phone, status, created_at)
- [x] Service `SuporteAgent` integrado com Gemini
- [x] Geração de ID único de ticket
- [x] Gestão de garantias
- [x] Integração com Monitor Inversor
- [x] Aguardar 2 dias antes de notificar
- [x] Endpoint `POST /api/v1/agents/suporte/config` - Configurar agente
- [x] Endpoint `GET /api/v1/agents/suporte/metrics` - Métricas do agente
- [x] Endpoint `GET /api/v1/tickets` - Listar tickets
- [x] Teste: Criar ticket automaticamente
- [x] Teste: Verificar SLA < 2h

### 4.2 Frontend - Agente de Suporte
- [x] Node "Bot de Suporte" no canvas
- [x] ConfigPanel com configurações
- [x] Métricas em tempo real
- [x] Lista de tickets no dashboard
- [x] Teste: Configurar agente no canvas
- [x] Teste: Ver tickets criados

---

## 5️⃣ INTEGRAÇÃO WHATSAPP

### 5.1 Backend - WhatsApp
- [x] WhatsApp Gateway rodando
- [x] QR Code gerado e exibido
- [x] Conexão estabelecida
- [x] Recebimento de mensagens funcionando
- [x] Envio de mensagens funcionando
- [x] RabbitMQ recebendo mensagens
- [x] Consumer processando mensagens
- [x] Roteamento para agentes correto
- [x] Teste: Escanear QR Code
- [x] Teste: Enviar mensagem e receber resposta

### 5.2 Frontend - WhatsApp
- [x] Página de configuração do WhatsApp
- [x] Exibição do QR Code via WebSocket
- [x] Status de conexão em tempo real
- [x] Botão "Conectar WhatsApp"
- [x] Botão "Desconectar WhatsApp"
- [x] Node "WhatsApp" no canvas
- [x] Métricas: mensagens/dia
- [x] Teste: Conectar WhatsApp pelo frontend
- [x] Teste: Ver status atualizado

---

## 6️⃣ MONITOR DE INVERSORES

### 6.1 Backend - Monitor
- [ ] Model `Inverter` (id, serial, platform, status, last_check)
- [ ] Model `InverterEvent` (id, inverter_id, event_type, data_json, created_at)
- [ ] Service `InverterMonitor` para SolisCloud
- [ ] Service `InverterMonitor` para Growatt
- [ ] Service `InverterMonitor` para Solarman
- [ ] Detecção automática de falhas
- [ ] Análise de causa provável
- [ ] Aguardar 2 dias antes de notificar
- [ ] Endpoint `POST /api/v1/inverters` - Cadastrar inversor
- [ ] Endpoint `GET /api/v1/inverters` - Listar inversores
- [ ] Endpoint `GET /api/v1/inverters/{id}/events` - Eventos do inversor
- [ ] Teste: Cadastrar inversor
- [ ] Teste: Simular falha e verificar notificação

### 6.2 Frontend - Monitor
- [ ] Node "Monitor Inversor" no canvas
- [ ] Página de gestão de inversores
- [ ] Lista de inversores cadastrados
- [ ] Status online/offline
- [ ] Histórico de eventos
- [ ] Teste: Cadastrar inversor pelo frontend
- [ ] Teste: Ver eventos em tempo real

---

## 7️⃣ GERADOR DE ORÇAMENTOS

### 7.1 Backend - Orçamentos
- [ ] Model `Kit` (id, name, is_template, data_json)
- [ ] Model `ItemKit` (id, kit_id, categoria, nome, preco, quantidade)
- [ ] Model `Orcamento` (id, kit_id, cliente_nome, status, pdf_url)
- [ ] Service `PDFGenerator` com template
- [ ] Cálculo automático de kWp e kWh
- [ ] Validação de categorias mínimas
- [ ] Endpoint `POST /api/v1/kits` - Criar kit
- [ ] Endpoint `GET /api/v1/kits` - Listar kits
- [ ] Endpoint `POST /api/v1/orcamentos` - Criar orçamento
- [ ] Endpoint `GET /api/v1/orcamentos` - Listar orçamentos
- [ ] Endpoint `GET /api/v1/orcamentos/{id}/pdf` - Baixar PDF
- [ ] Teste: Criar kit com itens
- [ ] Teste: Gerar orçamento e baixar PDF

### 7.2 Frontend - Orçamentos
- [ ] Página "Monte Seu Kit"
- [ ] Drag-and-drop de itens
- [ ] Cálculo automático de totais
- [ ] Validação de regras de negócio
- [ ] Página "Orçamentos"
- [ ] Lista de orçamentos
- [ ] Botão "Gerar PDF"
- [ ] Node "Gerador PDF" no canvas
- [ ] Teste: Criar kit pelo frontend
- [ ] Teste: Gerar orçamento e baixar PDF

---

## 8️⃣ DASHBOARD

### 8.1 Backend - Dashboard
- [ ] Endpoint `GET /api/v1/dashboard/stats` - Estatísticas gerais
- [ ] Endpoint `GET /api/v1/dashboard/agents` - Status dos agentes
- [ ] Endpoint `GET /api/v1/dashboard/activity` - Atividade recente
- [ ] Endpoint `GET /api/v1/dashboard/system` - Status do sistema
- [ ] Teste: Buscar estatísticas
- [ ] Teste: Verificar dados em tempo real

### 8.2 Frontend - Dashboard
- [ ] Remover dados mock do Dashboard
- [ ] Integrar com API real
- [ ] Cards de estatísticas dinâmicos
- [ ] Status do sistema em tempo real
- [ ] Lista de agentes com métricas reais
- [ ] Atividade recente da API
- [ ] Teste: Ver dashboard atualizado
- [ ] Teste: Verificar métricas corretas

---

## 9️⃣ CONFIGURAÇÕES

### 9.1 Backend - Configurações
- [ ] Model `CompanySettings` (id, company_id, settings_json)
- [ ] Endpoint `GET /api/v1/settings` - Buscar configurações
- [ ] Endpoint `PUT /api/v1/settings` - Atualizar configurações
- [ ] Regras comerciais
- [ ] Regras de linguagem
- [ ] Regras de responsabilidade
- [ ] Teste: Salvar configurações
- [ ] Teste: Aplicar regras nos agentes

### 9.2 Frontend - Configurações
- [ ] Página de configurações
- [ ] Formulário de regras globais
- [ ] Configuração de integrações
- [ ] Teste: Salvar configurações pelo frontend
- [ ] Teste: Ver configurações aplicadas

---

## 🔟 TESTES FINAIS E2E

### 10.1 Fluxo Completo - Vendas
- [ ] Conectar WhatsApp
- [ ] Criar workflow com Agente de Vendas
- [ ] Cliente envia mensagem
- [ ] Agente coleta dados
- [ ] Orçamento gerado automaticamente
- [ ] PDF enviado ao cliente
- [ ] Teste: Fluxo completo sem erros

### 10.2 Fluxo Completo - Suporte
- [ ] Criar workflow com Agente de Suporte
- [ ] Cliente reporta problema
- [ ] Ticket criado automaticamente
- [ ] Monitor detecta falha no inversor
- [ ] Aguarda 2 dias
- [ ] Mensagem preparada para revisão
- [ ] Mensagem enviada ao cliente
- [ ] Teste: Fluxo completo sem erros

### 10.3 Fluxo Completo - Canvas
- [ ] Criar workflow complexo
- [ ] Conectar múltiplos nodes
- [ ] Salvar workflow
- [ ] Executar workflow
- [ ] Ver histórico de execuções
- [ ] Ver logs detalhados
- [ ] Teste: Workflow executado com sucesso

---

## 1️⃣1️⃣ OTIMIZAÇÕES E POLISH

### 11.1 Performance
- [ ] Cache Redis implementado
- [ ] Queries otimizadas
- [ ] Índices no banco de dados
- [ ] Lazy loading no frontend
- [ ] Teste: Tempo de resposta < 200ms

### 11.2 UX/UI
- [ ] Loading states em todas as ações
- [ ] Mensagens de erro amigáveis
- [ ] Confirmações antes de deletar
- [ ] Toasts de sucesso/erro
- [ ] Teste: UX fluida e responsiva

### 11.3 Segurança
- [ ] Validação de inputs
- [ ] Sanitização de dados
- [ ] Rate limiting
- [ ] CORS configurado
- [ ] Teste: Tentativas de SQL injection bloqueadas

---

## 📊 PROGRESSO GERAL

**Total de Tasks**: 150+
**Concluídas**: 70
**Progresso**: ~47%

---

## 🚀 PRÓXIMOS PASSOS IMEDIATOS

1. ✅ Corrigir autenticação (login funcionando)
2. ⏳ Implementar endpoints de workflows
3. ⏳ Remover dados mock do canvas
4. ⏳ Integrar WhatsApp com frontend
5. ⏳ Implementar agentes IA

---

## 📝 NOTAS

- Cada task deve ser testada individualmente
- Testes com `docker-compose exec` garantem ambiente real
- Marcar `[x]` apenas quando 100% funcional
- Priorizar features core antes de polish
- Documentar decisões técnicas importantes

---

**Última atualização**: 2026-01-13
**Responsável**: Dev Team
**Status**: 🟡 Em Desenvolvimento
