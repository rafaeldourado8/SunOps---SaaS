# 🌞 SunOps MAB - Sistema de Gestão Solar com IA

Sistema completo de gestão para empresas de energia solar com agentes IA para atendimento via WhatsApp.

## 🏗️ Arquitetura

```
WhatsApp → Gateway Node.js → RabbitMQ → AI Agents (FastAPI)
                                              ↓
                                    Gemini Flash + Pro
                                              ↓
                                    Redis Cache (80% economia)
                                              ↓
                                    PostgreSQL (Master/Replica)
```

## 🚀 Quick Start

### 1. Configurar ambiente

```bash
cp .env.example .env
# Adicione sua GEMINI_API_KEY
```

### 2. Iniciar stack completa

```bash
docker-compose up -d
```

### 3. Ver QR Code do WhatsApp

```bash
docker-compose logs -f whatsapp-gateway
```

Ou abra: `bot_whatsapp/examples/qrcode-frontend.html`

### 4. Testar agentes

```bash
cd bot_whatsapp
python test-agents.py vendas    # Testa bot de vendas
python test-agents.py suporte   # Testa bot de suporte
python test-agents.py monitor   # Monitora respostas
```

## 📦 Serviços

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| **Frontend** | 80 | Interface web React + Vite |
| **FastAPI** | 8000 | API REST principal |
| **PostgreSQL Master** | 5432 | Banco de dados (write) |
| **PostgreSQL Replica** | 5433 | Banco de dados (read) |
| **Redis** | 6379 | Cache para economia de tokens |
| **RabbitMQ** | 5672 | Message broker |
| **RabbitMQ Management** | 15672 | Interface web (guest/guest) |
| **WhatsApp Gateway** | 3001 | Gateway Node.js + WebSocket |
| **WhatsApp AI Agent** | - | Consumer de mensagens |

## 🤖 Agentes IA

### Bot de Vendas
- ✅ Coleta informações do cliente
- ✅ Gera orçamentos automaticamente
- ✅ Linguagem persuasiva e natural
- ✅ Transfere para humano quando solicitado

### Bot de Suporte
- ✅ Gera tickets únicos
- ✅ Monitora inversores (aguarda 2 dias)
- ✅ Gestão de garantias
- ✅ Linguagem empática e paciente
- ✅ Ensina uso de apps de monitoramento

## 📚 Documentação

- [Arquitetura WhatsApp](bot_whatsapp/docs/WHATSAPP_ARQUITETURA.md)
- [Especificação dos Agentes IA](bot_whatsapp/docs/AGENTES_IA.md)
- [Guia de Uso dos Agentes](bot_whatsapp/docs/AGENTES_USO.md)
- [README WhatsApp Gateway](bot_whatsapp/docs/README.md)
- [Quick Start](bot_whatsapp/docs/QUICKSTART.md)
- [Deploy Docker](bot_whatsapp/docs/DOCKER.md)

## 💰 Economia de Custos

### Sem Otimização
- Gemini Pro: $0.50/1M tokens input
- 1000 conversas/dia = **$600/mês**

### Com Otimização (Flash + Cache)
- Gemini Flash: 85% das requisições
- Redis Cache: 80% de economia
- Custo estimado: **$120/mês**
- **Economia: $480/mês**

## 🛠️ Stack Tecnológica

### Backend
- FastAPI (async)
- PostgreSQL 15 (master-slave replication)
- SQLAlchemy (async)
- Alembic (migrations)
- Redis (cache)
- RabbitMQ (message broker)
- Celery (background tasks)

### Frontend
- React 18
- TypeScript
- Vite
- TailwindCSS
- Zustand (state management)
- React Router
- Framer Motion

### WhatsApp Gateway
- Node.js 18
- whatsapp-web.js
- WebSocket (QR code streaming)
- RabbitMQ (pika)

### AI Agents
- Google Gemini 1.5 Flash (preprocessamento)
- Google Gemini 1.5 Pro (resposta final)
- Redis (cache inteligente)

### Arquitetura
- Clean Architecture
- Domain-Driven Design (DDD)
- SOLID Principles
- Event Sourcing
- CQRS (Command Query Responsibility Segregation)

## 📁 Estrutura do Projeto

```
SunOps/
├── backend/                    # FastAPI + Domain Layer
│   ├── src/
│   │   ├── core/
│   │   │   ├── domain/        # Entidades, VOs, Aggregates
│   │   │   └── application/   # Use Cases, DTOs, Ports
│   │   └── adapters/
│   │       ├── fastapi_app/   # API REST
│   │       ├── infrastructure/# Repositories, Database
│   │       └── whatsapp_agent/# AI Agents
│   └── alembic/               # Migrations
├── frontend/                  # React + TypeScript
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── hooks/             # Custom hooks
│   │   ├── stores/            # Zustand stores
│   │   └── types/             # TypeScript types
│   └── Dockerfile             # Multi-stage build
├── bot_whatsapp/              # WhatsApp Gateway (Node.js)
│   ├── src/
│   │   ├── config/
│   │   ├── services/          # RabbitMQ, WebSocket, WhatsApp
│   │   └── handlers/          # Message, Response
│   ├── examples/              # Frontend QR Code, Consumer Python
│   └── docs/                  # Documentação completa
└── docker-compose.yml         # Stack completa
```

## 🧪 Testes

### Backend (28 testes unitários)

```bash
cd backend
pytest src/core/tests/ -v --cov=src/core/domain
```

### Integração WhatsApp

```bash
cd bot_whatsapp
npm run test:rabbitmq
python test-agents.py monitor
```

## 🔐 Variáveis de Ambiente

```env
# Database
POSTGRES_PASSWORD=changeme

# Gemini AI
GEMINI_API_KEY=your_key_here
```

## 📊 Monitoramento

- **Frontend**: http://localhost
- **FastAPI Docs**: http://localhost:8000/docs
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)
- **WebSocket QR Code**: ws://localhost:3001

## 🎯 Roadmap

### ✅ Fase 1: Domínio (100%)
- [x] Value Objects, Entities, Aggregates
- [x] Domain Events, Services
- [x] 28 testes unitários (95%+ coverage)

### ✅ Fase 2: Aplicação (100%)
- [x] 6 Use Cases
- [x] DTOs, Repository Ports

### ✅ Fase 3: Infraestrutura (100%)
- [x] PostgreSQL Master/Replica
- [x] SQLAlchemy Models
- [x] Repositories async
- [x] Alembic Migrations

### ✅ Fase 4: API (100%)
- [x] 8 endpoints REST
- [x] Pydantic validation
- [x] OpenAPI docs

### ✅ Fase 5: WhatsApp Gateway (100%)
- [x] Node.js Gateway
- [x] QR Code (terminal + WebSocket)
- [x] RabbitMQ integration
- [x] Message/Response handlers

### ✅ Fase 6: AI Agents (100%)
- [x] Base Agent interface
- [x] VendasAgent
- [x] SuporteAgent
- [x] Gemini Flash + Pro integration
- [x] Redis Cache service
- [x] RabbitMQ Consumer

### 🚧 Fase 7: Features Avançadas (0%)
- [ ] Geração de PDF para orçamentos
- [ ] Integração APIs de monitoramento (SolisCloud, Growatt, Solarman)
- [ ] Dashboard admin em tempo real
- [ ] Botão "assumir conversa"
- [ ] Suporte a áudio (Whisper)
- [ ] Treinamento via prints/textos/áudios
- [ ] Sistema de regras customizáveis

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

MIT
