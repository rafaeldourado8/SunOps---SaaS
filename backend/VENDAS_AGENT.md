# 🤖 Agente de Vendas - Implementação

## ✅ Implementado

### Models
- **Conversation**: Armazena conversas por telefone e tipo de agente
- **Message**: Histórico de mensagens (user/assistant)

### Repository
- **ConversationRepository**: 
  - `get_or_create_conversation()`: Busca ou cria conversa
  - `add_message()`: Adiciona mensagem ao histórico
  - `get_messages()`: Busca últimas mensagens
  - `update_context()`: Atualiza contexto da conversa

### Service
- **VendasAgentService**:
  - Mantém contexto por cliente
  - Coleta dados guiados (consumo, telhado, localização)
  - Extração automática de informações
  - Transferência para humano
  - Geração de orçamento (integração futura)

### Endpoints
- `POST /api/v1/agents/vendas/message`: Processar mensagem
- `POST /api/v1/agents/vendas/config`: Configurar agente
- `GET /api/v1/agents/vendas/metrics`: Métricas do agente

## 🧪 Testar

```bash
# 1. Aplicar migration
cd backend
docker-compose exec api alembic upgrade head

# 2. Rodar testes
python test_vendas_agent.py
```

## 📊 Fluxo de Conversa

```
Cliente: "Olá, quero um orçamento"
Bot: "Olá! Para fazer um orçamento personalizado, preciso de algumas informações..."

Cliente: "Minha conta vem 450 kWh por mês"
Bot: "Ótimo! Estou anotando essas informações. Qual é o tipo do seu telhado?"

Cliente: "Meu telhado é de cerâmica"
Bot: "Perfeito! Vou preparar um orçamento personalizado para você."
```

## 🔄 Próximos Passos

1. Integrar com Gemini Flash/Pro
2. Implementar geração automática de orçamento
3. Adicionar métricas reais do banco
4. Integrar com WhatsApp Gateway
5. Dashboard de conversas ativas
