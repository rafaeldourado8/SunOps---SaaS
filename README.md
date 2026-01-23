# SunOPS - Sistema de Gestão Solar

## 🚀 Arquitetura

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL + RabbitMQ
- **Frontend**: React + Vite + Nginx
- **Arquitetura**: DDD Tático + Clean Architecture + SOLID

## 📦 Estrutura

```
SunOPS/
├── docker/
│   ├── backend/
│   │   └── Dockerfile
│   └── frontend/
│       └── Dockerfile
├── src/                    # Backend (FastAPI)
│   ├── clientes/
│   ├── propostas/
│   ├── contratos/
│   ├── premissas/
│   └── shared/
├── frontend/               # Frontend (React)
│   └── src/
├── docker-compose.yml
└── README.md
```

## 🔧 Como Rodar

### 1. Subir todos os serviços
```bash
docker-compose up -d
```

### 2. Acessar aplicação
- **Frontend**: http://localhost
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **RabbitMQ**: http://localhost:15672 (guest/guest)

### 3. Popular premissas iniciais
```bash
docker-compose exec api python seed_premissas.py
```

### 4. Ver logs
```bash
docker-compose logs -f api
docker-compose logs -f frontend
docker-compose logs -f worker
```

### 5. Parar serviços
```bash
docker-compose down
```

## 📡 Endpoints Principais

### Clientes
- `POST /api/clientes/` - Criar cliente
- `GET /api/clientes/{id}` - Obter cliente
- `POST /api/clientes/{id}/promover` - Promover para prospect

### Propostas
- `POST /api/propostas/` - Criar proposta
- `POST /api/propostas/{id}/itens` - Adicionar item (calcula preço automaticamente)
- `POST /api/propostas/{id}/desconto` - Solicitar desconto

### Premissas
- `POST /api/premissas/` - Criar premissa de preço
- `GET /api/premissas/` - Listar premissas
- `PUT /api/premissas/configuracao` - Atualizar configurações globais

### Templates
- `POST /api/templates/` - Upload de template PDF
- `GET /api/templates/` - Listar templates

## 🎨 Frontend

- Design premium preto/gradiente
- Login com timeout de 4 minutos
- Dashboard com estatísticas
- Sidebar moderna

## 🔐 Segurança

- Timeout de sessão: 4 minutos de inatividade
- JWT para autenticação
- Nginx com proxy reverso
- Timeout de requisições: 240s

## 📝 Desenvolvimento

### Backend
```bash
cd src
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🏗️ Arquitetura DDD

- **Domain**: Regras de negócio puras
- **Application**: Use Cases
- **Infrastructure**: Frameworks, DB, APIs

### Bounded Contexts
- Clientes
- Propostas
- Contratos
- Premissas
