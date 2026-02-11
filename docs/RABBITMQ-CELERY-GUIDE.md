# 🚀 Implementação RabbitMQ + Celery - CRM Solar

## 📋 O que foi implementado

### 1. **Mensageria Assíncrona**
- ✅ RabbitMQ como message broker
- ✅ Celery para processamento de tasks
- ✅ Redis como result backend
- ✅ Celery Beat para tarefas agendadas

### 2. **Otimizações Gunicorn**
```bash
# Antes (LENTO)
--workers 2 --timeout 120

# Depois (RÁPIDO)
--workers 4 --threads 4 --worker-class gthread 
--worker-tmp-dir /dev/shm --max-requests 1000 
--max-requests-jitter 100 --keep-alive 5
```

**Melhorias:**
- Workers aumentados de 2 → 4
- Threads adicionadas (4 por worker = 16 conexões simultâneas)
- Worker class gthread (melhor para I/O)
- Uso de /dev/shm (RAM) para arquivos temporários
- Max requests para evitar memory leaks
- Keep-alive otimizado

### 3. **Cache Inteligente**
- Dashboard: cache de 5 minutos
- PDFs: cache de 1 hora
- Métricas: atualização assíncrona

### 4. **Tasks Assíncronas**
```python
# Geração de PDF (antes bloqueava request)
gerar_pdf_orcamento_async.delay(orcamento_id)

# Cálculo de métricas (background)
calcular_dashboard_metrics.delay()

# Processamento de orçamento
processar_orcamento_async.delay(data)
```

---

## 🔧 Como usar

### Desenvolvimento Local

```bash
# 1. Subir todos os serviços
docker-compose up -d

# 2. Verificar logs
docker-compose logs -f celery_worker
docker-compose logs -f backend

# 3. Acessar RabbitMQ Management
http://localhost:15672
# User: guest / Pass: guest
```

### Produção Otimizada

```bash
# 1. Usar compose otimizado
docker-compose -f docker-compose.prod-optimized.yml up -d

# 2. Monitorar workers
docker-compose exec celery_worker celery -A config inspect active

# 3. Ver estatísticas
docker-compose exec celery_worker celery -A config inspect stats
```

---

## 📊 Monitoramento

### RabbitMQ Dashboard
```
URL: http://localhost:15672
User: guest
Pass: guest
```

**O que monitorar:**
- Queues: número de mensagens pendentes
- Consumers: workers conectados
- Message rates: throughput

### Celery Flower (Opcional)
```bash
# Adicionar ao docker-compose
flower:
  build: ./backend
  command: celery -A config flower --port=5555
  ports:
    - "5555:5555"
  depends_on:
    - rabbitmq
    - redis
```

---

## 🐛 Troubleshooting

### Problema: Tasks não executam

```bash
# Verificar workers
docker-compose ps celery_worker

# Ver logs
docker-compose logs celery_worker

# Reiniciar worker
docker-compose restart celery_worker
```

### Problema: RabbitMQ não conecta

```bash
# Verificar saúde
docker-compose exec rabbitmq rabbitmq-diagnostics ping

# Ver conexões
docker-compose exec rabbitmq rabbitmqctl list_connections

# Reiniciar
docker-compose restart rabbitmq
```

### Problema: Gunicorn ainda lento

```bash
# Verificar workers ativos
docker-compose exec backend ps aux | grep gunicorn

# Aumentar workers (ajustar conforme CPU)
# Fórmula: (2 x CPU cores) + 1
# Ex: 4 cores = 9 workers

# Verificar memória
docker stats backend
```

### Problema: Cache não funciona

```bash
# Testar Redis
docker-compose exec redis redis-cli ping
# Deve retornar: PONG

# Ver chaves
docker-compose exec redis redis-cli KEYS "*"

# Limpar cache
docker-compose exec redis redis-cli FLUSHDB
```

---

## 📈 Otimizações de Banco

### PostgreSQL (já configurado)
```sql
-- Verificar conexões
SELECT count(*) FROM pg_stat_activity;

-- Ver queries lentas
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

### Índices importantes
```python
# Adicionar em models.py
class Meta:
    indexes = [
        models.Index(fields=['cliente', '-data_criacao']),
        models.Index(fields=['vendedor', 'forma_pagamento']),
    ]
```

---

## 🔥 Performance Esperada

### Antes
- Dashboard: 2-5 segundos
- Geração PDF: 10-30 segundos (bloqueante)
- Listagem: 1-3 segundos
- Gunicorn: 2 workers, timeout frequente

### Depois
- Dashboard: 200-500ms (com cache)
- Geração PDF: 200ms (assíncrono) + background
- Listagem: 300-800ms
- Gunicorn: 4 workers + 4 threads = 16 conexões simultâneas

---

## 🚀 Próximos Passos

### 1. Adicionar mais tasks assíncronas
```python
# backend/apps/clientes/tasks.py
@shared_task
def enviar_email_boas_vindas(cliente_id):
    # Enviar email em background
    pass

@shared_task
def gerar_relatorio_mensal():
    # Relatório agendado
    pass
```

### 2. Configurar Celery Beat
```python
# settings.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'atualizar-dashboard-diario': {
        'task': 'apps.orcamentos.tasks.calcular_dashboard_metrics',
        'schedule': crontab(hour=0, minute=0),
    },
}
```

### 3. Adicionar retry automático
```python
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def task_com_retry(self):
    try:
        # código
        pass
    except Exception as exc:
        raise self.retry(exc=exc)
```

---

## 📝 Variáveis de Ambiente

Adicionar ao `.env`:

```bash
# RabbitMQ
RABBITMQ_USER=guest
RABBITMQ_PASS=guest
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Gunicorn
GUNICORN_WORKERS=4
GUNICORN_THREADS=4
GUNICORN_TIMEOUT=120
```

---

## ✅ Checklist de Deploy

- [ ] RabbitMQ rodando e acessível
- [ ] Celery workers ativos (mínimo 2)
- [ ] Redis funcionando
- [ ] Cache configurado
- [ ] Gunicorn com workers otimizados
- [ ] Logs sendo monitorados
- [ ] Backup de RabbitMQ configurado
- [ ] Alertas de fila cheia
- [ ] Métricas de performance

---

## 🆘 Suporte

**Logs importantes:**
```bash
# Backend
docker-compose logs -f backend

# Celery
docker-compose logs -f celery_worker

# RabbitMQ
docker-compose logs -f rabbitmq

# Todos
docker-compose logs -f
```

**Comandos úteis:**
```bash
# Reiniciar tudo
docker-compose restart

# Rebuild
docker-compose up -d --build

# Limpar tudo
docker-compose down -v
docker-compose up -d --build
```

---

**Desenvolvido para alta performance e escalabilidade** 🚀
