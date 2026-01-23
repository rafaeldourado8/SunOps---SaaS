# SunOPS - Arquitetura DDD Tático

## 🏗️ Arquitetura

**DDD Tático** + **Clean Architecture** + **SOLID** + **FastAPI** + **SQLAlchemy** + **RabbitMQ**

## 📁 Estrutura

```
src/
├── shared/                    # Shared Kernel
│   ├── domain/               # Entity, Repository, Value Objects
│   └── infrastructure/       # Database, MessageBroker, PDF
├── clientes/                 # Bounded Context
│   ├── domain/              # Entities, Repository Interface
│   ├── application/         # Use Cases
│   └── infrastructure/      # API, Repository, Models
├── propostas/               # Bounded Context
│   ├── domain/
│   ├── application/
│   └── infrastructure/
├── contratos/               # Bounded Context
│   ├── domain/
│   ├── application/
│   └── infrastructure/
├── main.py                  # FastAPI App
├── worker.py                # Message Consumer
└── docker-compose.yml       # Infraestrutura
```

## 🚀 Tecnologias

- **FastAPI** - API REST assíncrona
- **SQLAlchemy** - ORM para PostgreSQL
- **RabbitMQ** - Message Broker
- **PostgreSQL** - Banco de dados
- **Pydantic** - Validação de dados
- **FPDF** - Geração de PDF

## 🔧 Setup

### 1. Instalar dependências
```bash
cd src
pip install -r requirements.txt
```

### 2. Subir infraestrutura (Docker)
```bash
docker-compose up -d
```

### 3. Rodar API
```bash
uvicorn main:app --reload
```

### 4. Rodar Worker (em outro terminal)
```bash
python worker.py
```

## 📡 Endpoints

### Clientes
- `POST /clientes/` - Criar cliente
- `GET /clientes/{id}` - Obter cliente
- `POST /clientes/{id}/promover` - Promover para prospect

### Propostas
- `POST /propostas/` - Criar proposta
- `GET /propostas/{id}` - Obter proposta
- `POST /propostas/{id}/itens` - Adicionar item
- `POST /propostas/{id}/desconto` - Solicitar desconto

## 🎯 Fluxo Assíncrono

1. Cliente criado → Publica mensagem `cliente_criado`
2. Worker consome → Envia email de boas-vindas
3. Desconto solicitado → Publica `desconto_solicitado`
4. Worker consome → Notifica gestor

## 🗄️ Banco de Dados

PostgreSQL com SQLAlchemy. Migrations automáticas via `Base.metadata.create_all()`.

## 📨 Mensageria

RabbitMQ para processamento assíncrono:
- Envio de emails
- Notificações
- Geração de PDFs em background

## 🎨 Princípios

- **Domain-Driven Design**: Bounded Contexts isolados
- **Clean Architecture**: Domínio independente de infra
- **SOLID**: Código extensível e manutenível
- **Repository Pattern**: Abstração de persistência
- **Async Processing**: Tarefas pesadas em background
