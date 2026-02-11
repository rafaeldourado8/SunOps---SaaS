# 🚀 Deploy RabbitMQ + Celery no Servidor

## 📍 Localização do Projeto
```bash
cd /home/ubuntu/sunops
# ou
cd ~/sunops
```

## 🔧 Instalação Rápida

### 1. Atualizar código
```bash
cd ~/sunops
git pull origin main
```

### 2. Parar containers
```bash
docker-compose down
```

### 3. Atualizar dependências
```bash
cd backend
pip install -r requirements.txt
# ou rebuild containers
cd ..
docker-compose build --no-cache
```

### 4. Iniciar com RabbitMQ
```bash
docker-compose up -d
```

### 5. Verificar serviços
```bash
docker-compose ps
```

Deve mostrar:
- backend (running)
- celery_worker (running)
- celery_beat (running)
- rabbitmq (running)
- redis (running)
- db (running)

---

## 📊 Monitoramento

### Ver logs
```bash
# Backend
docker-compose logs -f backend

# Celery Worker
docker-compose logs -f celery_worker

# RabbitMQ
docker-compose logs -f rabbitmq

# Todos
docker-compose logs -f
```

### Verificar workers Celery
```bash
docker-compose exec celery_worker celery -A config inspect active
docker-compose exec celery_worker celery -A config inspect stats
```

### Acessar RabbitMQ Management
```
URL: http://SEU_IP:15672
User: guest
Pass: guest
```

---

## 🐛 Troubleshooting

### Problema: Containers não sobem
```bash
# Ver erro específico
docker-compose logs backend
docker-compose logs celery_worker

# Rebuild completo
docker-compose down -v
docker-compose up -d --build
```

### Problema: RabbitMQ não conecta
```bash
# Verificar saúde
docker-compose exec rabbitmq rabbitmq-diagnostics ping

# Reiniciar
docker-compose restart rabbitmq
sleep 10
docker-compose restart celery_worker
```

### Problema: Celery não processa tasks
```bash
# Ver workers
docker-compose exec celery_worker celery -A config inspect active

# Reiniciar worker
docker-compose restart celery_worker

# Ver logs detalhados
docker-compose logs --tail=100 celery_worker
```

### Problema: Gunicorn timeout
```bash
# Verificar workers
docker-compose exec backend ps aux | grep gunicorn

# Deve mostrar: 1 master + 4 workers

# Reiniciar
docker-compose restart backend
```

---

## 🔥 Comandos Úteis

### Limpar cache Redis
```bash
docker-compose exec redis redis-cli FLUSHDB
```

### Reiniciar tudo
```bash
docker-compose restart
```

### Ver uso de recursos
```bash
docker stats
```

### Entrar no container
```bash
docker-compose exec backend bash
docker-compose exec celery_worker bash
```

---

## ✅ Checklist Pós-Deploy

- [ ] `docker-compose ps` - todos running
- [ ] `docker-compose logs backend` - sem erros
- [ ] `docker-compose logs celery_worker` - workers iniciados
- [ ] Acessar frontend: http://SEU_IP
- [ ] Testar login
- [ ] Testar dashboard (deve carregar rápido)
- [ ] Gerar PDF (deve retornar task_id)

---

## 📈 Performance Esperada

| Operação | Tempo |
|----------|-------|
| Dashboard | < 500ms |
| Listagem | < 800ms |
| Gerar PDF | < 200ms (async) |

---

## 🆘 Suporte Emergencial

### Rollback rápido
```bash
cd ~/sunops
git log --oneline -5  # ver commits
git reset --hard COMMIT_HASH
docker-compose down
docker-compose up -d --build
```

### Logs completos
```bash
docker-compose logs > logs.txt
cat logs.txt
```
