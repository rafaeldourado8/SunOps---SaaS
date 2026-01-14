# OPS CRM - Sistema de Gestão para Energia Solar

CRM multi-tenant especializado para empresas de energia solar fotovoltaica.

## 🎯 Características

- **Multi-tenant**: Database-per-tenant para isolamento total
- **DDD**: Domain-Driven Design com bounded contexts
- **SOLID**: Princípios aplicados em todo código
- **Arquitetura**: Django + FastAPI + Celery + RabbitMQ + Redis + PostgreSQL

## 🚀 Quick Start

### Pré-requisitos

- Docker e Docker Compose
- Python 3.11+
- Git

### Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd OPS\ -\ CRM

# Copie o arquivo de ambiente
cp .env.example .env

# Suba os containers
docker-compose up -d

# Aguarde os serviços iniciarem (30-60s)
docker-compose logs -f
```

### Acessar Serviços

- **Django Admin**: http://localhost:8000/admin
- **FastAPI Docs**: http://localhost:8001/docs
- **RabbitMQ Management**: http://localhost:15672 (user: rabbitmq, pass: rabbitmq_dev_password)

## 📁 Estrutura do Projeto

```
OPS - CRM/
├── backend/              # Código Python
│   ├── shared/          # Shared Kernel (DDD)
│   ├── contexts/        # Bounded Contexts
│   ├── django_admin/    # Django Admin
│   ├── fastapi_app/     # FastAPI
│   └── celery_app/      # Celery Tasks
├── docs/                # Documentação
├── scripts/             # Scripts SQL e utilitários
└── docker-compose.yml   # Orquestração
```

## 🗺️ Roadmap

- [x] Setup infraestrutura
- [ ] Sprint 1: Fundação (Semanas 1-2)
- [ ] Sprint 2: Cadastros (Semanas 3-4)
- [ ] Sprint 3: Catálogo (Semanas 5-6)
- [ ] Sprint 4: Orçamentos (Semanas 7-8)

Ver [docs/03-MVP-ROADMAP-DETALHADO.md](docs/03-MVP-ROADMAP-DETALHADO.md)

## 📚 Documentação

- [Bounded Contexts](docs/01-BOUNDED-CONTEXTS.md)
- [Roadmap de Fases](docs/02-ROADMAP-FASES.md)
- [MVP Detalhado](docs/03-MVP-ROADMAP-DETALHADO.md)
- [Capacity Planning](docs/04-CAPACITY-PLANNING.md)
- [Multi-Tenancy](docs/05-MULTI-TENANCY-EXPLICADO.md)
- [System Design Cheat Sheet](docs/07-SYSTEM-DESIGN-CHEAT-SHEET.md)

## 🧪 Testes

```bash
# Rodar testes
docker-compose exec django pytest

# Com cobertura
docker-compose exec django pytest --cov
```

## 📝 Licença

Proprietário - Todos os direitos reservados
