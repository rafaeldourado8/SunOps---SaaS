# 🚀 Setup Rápido - OPS CRM

## ✅ Serviços Rodando

Todos os containers estão UP:
- ✅ PostgreSQL (5432) - master_db criado
- ✅ Redis (6379)
- ✅ RabbitMQ (5672, 15672)
- ✅ Django (8000)
- ✅ FastAPI (8001)
- ✅ Celery Worker

---

## 📋 Próximos Passos

### 1. Criar Migrations
```bash
docker-compose exec django python manage.py makemigrations
docker-compose exec django python manage.py migrate
```

### 2. Criar Superuser
```bash
docker-compose exec django python manage.py createsuperuser
# Username: admin
# Email: admin@ops-crm.com
# Password: admin123
```

### 3. Criar Tenant no Banco MASTER
```bash
docker-compose exec postgres psql -U postgres -d master_db
```

```sql
-- Criar tabela tenants (se não existir)
CREATE TABLE IF NOT EXISTS tenants (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(200) NOT NULL,
    db_name VARCHAR(100) UNIQUE NOT NULL,
    db_host VARCHAR(255) DEFAULT 'postgres',
    db_port INTEGER DEFAULT 5432,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir tenant exemplo
INSERT INTO tenants (slug, nome, db_name, ativo)
VALUES ('solar-abc', 'Solar ABC Ltda', 'tenant_solar_abc_db', TRUE);

-- Sair
\q
```

### 4. Aplicar Migrations no Tenant
```bash
# Conectar ao database do tenant
docker-compose exec postgres psql -U postgres -d tenant_solar_abc_db

# Aplicar schema (copiar do master_db)
# Ou rodar migrations apontando para tenant_solar_abc_db
```

---

## 🧪 Testar APIs

### 1. Health Check
```bash
curl http://localhost:8001/health
```

### 2. Login
```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"admin\", \"password\": \"admin123\"}"
```

Resposta:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@ops-crm.com",
    "role": "ADMIN"
  }
}
```

### 3. Criar Cliente (com tenant)
```bash
curl -X POST http://localhost:8001/api/v1/clientes \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Slug: solar-abc" \
  -H "Authorization: Bearer <SEU_TOKEN>" \
  -d '{
    "nome": "João Silva",
    "tipo_documento": "CPF",
    "numero_documento": "12345678901",
    "email": "joao@email.com",
    "telefone": "11999999999"
  }'
```

---

## 🔗 Acessos

- **Django Admin**: http://localhost:8000/admin
- **FastAPI Docs**: http://localhost:8001/docs
- **RabbitMQ Management**: http://localhost:15672
  - User: `rabbitmq`
  - Pass: `rabbitmq_dev_password`

---

## 🐛 Troubleshooting

### Ver logs
```bash
# Todos os serviços
docker-compose logs -f

# Serviço específico
docker-compose logs -f django
docker-compose logs -f fastapi
docker-compose logs -f celery
```

### Reiniciar serviço
```bash
docker-compose restart django
docker-compose restart fastapi
```

### Rebuild completo
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Acessar shell do container
```bash
docker-compose exec django bash
docker-compose exec postgres psql -U postgres
```

---

## ✅ Status Atual

| Componente | Status | Observação |
|------------|--------|------------|
| PostgreSQL | ✅ OK | master_db + tenant_solar_abc_db |
| Redis | ✅ OK | Cache funcionando |
| RabbitMQ | ✅ OK | Broker pronto |
| Django | ✅ OK | Precisa migrations |
| FastAPI | ✅ OK | APIs funcionando |
| Celery | ✅ OK | Worker rodando |

---

## 🎯 Próximo: Migrations

Execute os comandos da seção "Próximos Passos" para:
1. Criar tabelas no master_db
2. Criar superuser
3. Inserir tenant exemplo
4. Testar APIs
