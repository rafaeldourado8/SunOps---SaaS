# 🚀 Guia de Uso - Agentes IA

## 📦 Instalação

### 1. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite `.env` e adicione sua chave do Gemini:
```env
GEMINI_API_KEY=sua_chave_aqui
```

### 2. Obter chave do Gemini

1. Acesse: https://makersuite.google.com/app/apikey
2. Crie uma nova API Key
3. Cole no arquivo `.env`

### 3. Iniciar stack completa

```bash
docker-compose up -d
```

Isso iniciará:
- ✅ FastAPI (porta 8000)
- ✅ PostgreSQL Master + Replica
- ✅ Redis (cache)
- ✅ RabbitMQ (filas)
- ✅ WhatsApp Gateway (porta 3001)
- ✅ **WhatsApp AI Agent Consumer**

## 📱 Testar Agentes

### 1. Conectar WhatsApp

```bash
# Ver QR Code
docker-compose logs -f whatsapp-gateway
```

Ou abra: `bot_whatsapp/examples/qrcode-frontend.html`

### 2. Enviar mensagem de teste

**Para Bot de Vendas:**
```
Olá, gostaria de um orçamento para energia solar
```

**Para Bot de Suporte:**
```
Meu inversor está offline, pode me ajudar?
```

### 3. Monitorar processamento

```bash
# Logs do agente IA
docker-compose logs -f whatsapp-agent

# Logs do gateway
docker-compose logs -f whatsapp-gateway

# RabbitMQ Management
http://localhost:15672 (guest/guest)
```

## 🔄 Fluxo Completo

```
1. Cliente envia mensagem no WhatsApp
   ↓
2. Gateway Node.js recebe e publica em RabbitMQ (whatsapp_messages)
   ↓
3. WhatsApp Agent Consumer processa:
   - Classifica intent (vendas/suporte)
   - Preprocessa com Gemini Flash
   - Verifica cache Redis (80% economia)
   - Gera resposta com Gemini Pro
   - Publica em RabbitMQ (whatsapp_responses)
   ↓
4. Gateway Node.js consome resposta
   ↓
5. Envia para WhatsApp com "digitando..."
```

## 🤖 Agentes Disponíveis

### VendasAgent
- Coleta informações (consumo, telhado, localização)
- Gera orçamentos automaticamente
- Linguagem persuasiva e natural
- Transfere para humano quando solicitado

### SuporteAgent
- Gera tickets únicos
- Monitora inversores (aguarda 2 dias)
- Gestão de garantias
- Linguagem empática e paciente
- Ensina uso de apps de monitoramento

## 📊 Cache Redis

### TTLs Configurados

- **Preprocessamento (Flash)**: 1 hora
- **Respostas comuns**: 30 minutos
- **FAQs**: 24 horas
- **Informações de produtos**: 24 horas

### Economia Estimada

- Sem cache: $600/mês
- Com cache: $120/mês
- **Economia: $480/mês (80%)**

## 🔧 Desenvolvimento Local

### Rodar apenas o consumer (sem Docker)

```bash
cd backend

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
export RABBITMQ_URL=amqp://guest:guest@localhost:5672
export REDIS_URL=redis://localhost:6379/0
export GEMINI_API_KEY=sua_chave

# Rodar consumer
python -m src.adapters.whatsapp_agent
```

### Testar com consumer Python de exemplo

```bash
cd bot_whatsapp/examples

# Instalar pika
pip install pika

# Rodar consumer de teste
python consumer-example.py
```

## 📝 Estrutura do Código

```
backend/src/adapters/whatsapp_agent/
├── agents/
│   ├── base.py           # Interface base
│   ├── vendas.py         # Bot de Vendas
│   └── suporte.py        # Bot de Suporte
├── services/
│   ├── gemini.py         # Integração Gemini
│   └── cache.py          # Cache Redis
├── consumers/
│   └── whatsapp.py       # Consumer RabbitMQ
└── __main__.py           # Entry point
```

## 🐛 Troubleshooting

### Consumer não inicia

```bash
# Verificar logs
docker-compose logs whatsapp-agent

# Verificar se RabbitMQ está rodando
docker-compose ps rabbitmq

# Verificar filas
http://localhost:15672/#/queues
```

### Gemini retorna erro

```bash
# Verificar API Key
echo $GEMINI_API_KEY

# Testar manualmente
curl -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$GEMINI_API_KEY"
```

### Cache não funciona

```bash
# Verificar Redis
docker-compose exec redis redis-cli ping

# Ver chaves no cache
docker-compose exec redis redis-cli KEYS "*"

# Limpar cache
docker-compose exec redis redis-cli FLUSHALL
```

## 🎯 Próximos Passos

1. [ ] Implementar geração de PDF para orçamentos
2. [ ] Integrar APIs de monitoramento (SolisCloud, Growatt, Solarman)
3. [ ] Criar dashboard admin para visualizar conversas em tempo real
4. [ ] Implementar botão de "assumir conversa"
5. [ ] Adicionar suporte a áudio (Whisper)
6. [ ] Implementar treinamento via prints/textos/áudios
7. [ ] Criar sistema de regras customizáveis por empresa

## 📚 Referências

- [Gemini API Docs](https://ai.google.dev/docs)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html)
- [Redis Caching Patterns](https://redis.io/docs/manual/patterns/)
