# 06 - Dimensionamento Real: 2 Tenants Iniciais

## 🎯 Cenário Real do MVP

```
Tenants Iniciais: 2 empresas
Plano: R$ 300/mês cada
Receita Inicial: R$ 600/mês
```

---

## 👥 Cálculo de Usuários (2 Tenants)

### Fórmula Aplicada

```python
tenants = 2
usuarios_por_tenant = 2
taxa_atividade_diaria = 0.40      # 40% usam por dia
taxa_concorrencia = 0.60          # 60% online ao mesmo tempo
fator_pico = 1.5                  # 50% acima da média

# Cálculos
usuarios_cadastrados = 2 × 2 = 4 usuários
dau = 4 × 0.40 = 1.6 usuários/dia
simultaneos_medio = 1.6 × 0.60 = 0.96 ≈ 1 usuário online
simultaneos_pico = 1 × 1.5 = 1.5 ≈ 2 usuários no pico
```

### Resultado

```
┌─────────────────────────────────────────┐
│ USUÁRIOS (2 Tenants)                    │
├─────────────────────────────────────────┤
│ Cadastrados:        4 usuários          │
│ DAU (40%):          1.6 usuários/dia    │
│ Simultâneos médio:  1 usuário           │
│ Simultâneos pico:   2 usuários          │
└─────────────────────────────────────────┘
```

---

## 📊 Cálculo de Requests (2 Tenants)

### Fórmula

```python
usuarios_simultaneos_medio = 1
usuarios_simultaneos_pico = 2
requests_por_usuario_hora = 120  # 2 req/min

# Requests por hora
req_hora_medio = 1 × 120 = 120 req/h
req_hora_pico = 2 × 120 = 240 req/h

# Requests por segundo
rps_medio = 120 ÷ 3,600 = 0.033 req/s
rps_pico = 240 ÷ 3,600 = 0.067 req/s
```

### Resultado

```
┌─────────────────────────────────────────┐
│ REQUESTS (2 Tenants)                    │
├─────────────────────────────────────────┤
│ Req/Hora (médio):   120 req/h          │
│ Req/Hora (pico):    240 req/h          │
│ RPS (médio):        0.033 req/s        │
│ RPS (pico):         0.067 req/s        │
└─────────────────────────────────────────┘

Traduzindo: 1 request a cada 15 segundos!
```

---

## 💾 Storage (2 Tenants)

### Por Tenant (Ano 1)

```
Clientes:     50 × 2 KB = 100 KB
Vendedores:   2 × 2 KB = 4 KB
Fornecedores: 20 × 2 KB = 40 KB
Marcas:       10 × 1 KB = 10 KB
Produtos:     200 × 5 KB = 1 MB
Orçamentos:   360 × 10 KB = 3.6 MB
PDFs:         360 × 500 KB = 180 MB
Logs:         45 MB
─────────────────────────────
TOTAL/Tenant: ~230 MB
```

### Total (2 Tenants)

```
Dados:        2 × 230 MB = 460 MB
Overhead 30%: 460 × 1.3 = 598 MB
Backup 2x:    598 × 2 = 1.196 GB ≈ 1.2 GB

Arredondando: 2 GB (com muita margem)
```

---

## 🖥️ Dimensionamento de Infraestrutura

### Compute (CPU/RAM)

```
RPS Pico: 0.067 req/s
Tempo de processamento: 50ms

CPU necessária:
= (0.067 × 0.05) ÷ 0.80
= 0.0042 cores
≈ 0.01 core (praticamente nada!)

RAM necessária:
Base: 512 MB (Django + FastAPI)
Concurrent requests: 2 × 10 MB = 20 MB
Cache: 20% = 106 MB
Total: 638 MB ≈ 1 GB
```

**Instância Mínima**: t3.micro (1 vCPU, 1 GB RAM)

### Database

```
Conexões:
Pool por tenant: 5
Total: 2 × 5 = 10 conexões
Max connections: 10 × 1.5 = 15

Storage: 5 GB (com muita margem)

IOPS: < 50 (muito baixo)
```

**Instância Mínima**: db.t3.micro (1 GB RAM, 20 GB storage)

### Cache (Redis)

```
Tenant info: 2 × 5 KB = 10 KB
Sessions: 2 × 10 KB = 20 KB
Query cache: 5 MB
Total: ~5 MB
```

**Instância Mínima**: cache.t3.micro (512 MB)

### Message Queue (RabbitMQ)

```
Mensagens/dia: 2 × 500 = 1,000 msg/dia
Mensagens/s: 1,000 ÷ 86,400 = 0.012 msg/s
Queue size: 0.012 × 3,600 = 43 mensagens (1h retenção)

RAM: 256 MB (base) + 43 KB = 256 MB
```

**Instância Mínima**: t3.micro (1 GB RAM)

### Bandwidth

```
Request: 2 KB
Response: 50 KB
RPS médio: 0.033

Throughput: 0.033 × 52 KB = 1.7 KB/s

Tráfego/Mês:
= 1.7 KB/s × 1,080,000s (30 dias × 10h × 3600s)
= 1,836,000 KB
= 1.75 GB/mês
```

---

## 💰 Custo AWS (2 Tenants) - Otimizado

### Opção 1: Tudo Separado (Não Recomendado)

```
EC2 App (t3.micro)           $7.59
EC2 RabbitMQ (t3.micro)      $7.59
RDS Master (db.t3.micro)     $16.61
RDS Tenants (db.t3.micro)    $16.61
ElastiCache (t3.micro)       $12.41
S3 Storage (1 GB)            $0.02
Data Transfer (2 GB)         $0.18
Route53                      $0.90
CloudWatch                   $5.00
─────────────────────────────────
TOTAL                        $67.91/mês
```

**Conversão**: $67.91 × R$ 5.00 = **R$ 339.55/mês**

```
Receita: R$ 600/mês
Custo: R$ 339.55/mês
Lucro: R$ 260.45/mês (43% margem)
```

### Opção 2: Consolidado (Recomendado MVP)

```
┌─────────────────────────────────────────┐
│ 1 EC2 t3.small (2 vCPU, 2 GB RAM)      │
│ - Django                                │
│ - FastAPI                               │
│ - RabbitMQ                              │
│ - Redis (Docker)                        │
│ Custo: $15.18/mês                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 1 RDS db.t3.micro (1 GB RAM, 20 GB)    │
│ - master_db                             │
│ - tenant_1_db                           │
│ - tenant_2_db                           │
│ Custo: $16.61/mês                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ S3 + Transfer + Route53                 │
│ Custo: $1.10/mês                        │
└─────────────────────────────────────────┘

TOTAL: $32.89/mês
```

**Conversão**: $32.89 × R$ 5.00 = **R$ 164.45/mês**

```
Receita: R$ 600/mês
Custo: R$ 164.45/mês
Lucro: R$ 435.55/mês (73% margem)
```

---

## 🚀 Opção 3: Máximo Custo-Benefício (Recomendado!)

### Usar AWS Lightsail

```
┌─────────────────────────────────────────┐
│ Lightsail Instance (2 GB RAM, 1 vCPU)  │
│ - Docker Compose:                       │
│   - Django                              │
│   - FastAPI                             │
│   - PostgreSQL (todos os bancos)        │
│   - Redis                               │
│   - RabbitMQ                            │
│ - 60 GB SSD                             │
│ - 3 TB Transfer                         │
│                                         │
│ Custo: $10/mês                          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Route53 (DNS)                           │
│ Custo: $0.90/mês                        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ S3 (Backup dos bancos)                  │
│ Custo: $0.50/mês                        │
└─────────────────────────────────────────┘

TOTAL: $11.40/mês
```

**Conversão**: $11.40 × R$ 5.00 = **R$ 57/mês**

```
Receita: R$ 600/mês
Custo: R$ 57/mês
Lucro: R$ 543/mês (90% margem!)
```

---

## 📊 Comparação de Opções

| Opção | Custo/Mês | Lucro/Mês | Margem | Escalabilidade | Complexidade |
|-------|-----------|-----------|--------|----------------|--------------|
| **Separado** | R$ 340 | R$ 260 | 43% | ⭐⭐⭐⭐⭐ | Alta |
| **Consolidado** | R$ 164 | R$ 436 | 73% | ⭐⭐⭐⭐ | Média |
| **Lightsail** | R$ 57 | R$ 543 | 90% | ⭐⭐⭐ | Baixa |

---

## 🎯 Recomendação: Lightsail para MVP

### Por quê?

```
✅ Custo fixo e previsível ($10/mês)
✅ Suficiente para 2-10 tenants
✅ Setup simples (Docker Compose)
✅ 3 TB de transfer (mais que suficiente)
✅ 60 GB SSD (suficiente para 20+ tenants)
✅ Backup automático (+$1/mês)
✅ Snapshot para migração futura
```

### Quando migrar para EC2/RDS?

```
Migrar quando:
- Mais de 10 tenants
- Mais de 50 usuários simultâneos
- RPS > 5 req/s
- Storage > 40 GB
- Precisa de alta disponibilidade (multi-AZ)

Estimativa: 6-12 meses após lançamento
```

---

## 🗄️ Configuração Lightsail (Docker Compose)

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    deploy:
      resources:
        limits:
          memory: 512M

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    deploy:
      resources:
        limits:
          memory: 128M

  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    deploy:
      resources:
        limits:
          memory: 256M

  django:
    build: ./django_admin
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - rabbitmq
    deploy:
      resources:
        limits:
          memory: 512M

  fastapi:
    build: ./fastapi_app
    ports:
      - "8001:8001"
    depends_on:
      - postgres
      - redis
      - rabbitmq
    deploy:
      resources:
        limits:
          memory: 384M

  celery:
    build: ./celery_app
    depends_on:
      - postgres
      - redis
      - rabbitmq
    deploy:
      resources:
        limits:
          memory: 256M

volumes:
  postgres_data:
```

### Uso de Recursos

```
PostgreSQL:  512 MB RAM
Redis:       128 MB RAM
RabbitMQ:    256 MB RAM
Django:      512 MB RAM
FastAPI:     384 MB RAM
Celery:      256 MB RAM
─────────────────────
TOTAL:       2048 MB (2 GB)

Lightsail tem 2 GB RAM = Perfeito!
```

---

## 📈 Projeção de Crescimento (Lightsail)

| Tenants | Usuários | DAU | RPS | Storage | Lightsail | Custo | Receita | Lucro |
|---------|----------|-----|-----|---------|-----------|-------|---------|-------|
| 2       | 4        | 1.6 | 0.07| 2 GB    | $10       | R$ 57 | R$ 600  | R$ 543|
| 5       | 10       | 4   | 0.17| 5 GB    | $10       | R$ 57 | R$ 1.500| R$ 1.443|
| 10      | 20       | 8   | 0.33| 10 GB   | $10       | R$ 57 | R$ 3.000| R$ 2.943|
| 15      | 30       | 12  | 0.50| 15 GB   | $20       | R$ 114| R$ 4.500| R$ 4.386|
| 20      | 40       | 16  | 0.67| 20 GB   | $20       | R$ 114| R$ 6.000| R$ 5.886|

**Nota**: Lightsail $20/mês = 4 GB RAM, 80 GB SSD

---

## 🔄 Plano de Migração Futura

### Quando Migrar (Sinais)

```
🔴 MIGRAR URGENTE:
- CPU > 80% por mais de 1 hora
- RAM > 90%
- Storage > 80%
- Response time > 1s

🟡 PLANEJAR MIGRAÇÃO:
- Mais de 20 tenants
- RPS > 1 req/s
- Storage > 40 GB
- Precisa de SLA 99.9%
```

### Migração Lightsail → AWS

```
1. Criar snapshot do Lightsail
2. Exportar para EC2 AMI
3. Provisionar:
   - EC2 t3.small (app)
   - RDS db.t3.small (database)
   - ElastiCache t3.micro (redis)
4. Migrar dados (pg_dump/restore)
5. Testar
6. Trocar DNS
7. Desligar Lightsail

Tempo: 4-6 horas
Downtime: < 30 minutos
```

---

## 💡 Otimizações Adicionais

### 1. Usar Cloudflare (Grátis)

```
✅ CDN grátis
✅ SSL grátis
✅ DDoS protection
✅ Cache de assets
✅ Reduz 50% do tráfego

Economia: ~$5/mês em transfer
```

### 2. Backup Automático

```
# Script de backup diário
#!/bin/bash

# Backup PostgreSQL
docker exec postgres pg_dumpall -U postgres | gzip > backup_$(date +%Y%m%d).sql.gz

# Upload para S3
aws s3 cp backup_$(date +%Y%m%d).sql.gz s3://seu-bucket/backups/

# Manter últimos 30 dias
find . -name "backup_*.sql.gz" -mtime +30 -delete

Custo S3: $0.50/mês (30 backups × 50 MB)
```

### 3. Monitoramento Grátis

```
- Uptime Robot (grátis): Monitora uptime
- Grafana Cloud (grátis): Métricas
- Sentry (grátis): Error tracking

Custo: $0
```

---

## ✅ Configuração Final Recomendada (2 Tenants)

```
┌─────────────────────────────────────────────────────┐
│ INFRAESTRUTURA MVP (2 Tenants)                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Hospedagem:                                         │
│ └─ AWS Lightsail $10/mês (2 GB RAM, 60 GB SSD)    │
│                                                     │
│ DNS:                                                │
│ └─ Route53 $0.90/mês                               │
│                                                     │
│ CDN:                                                │
│ └─ Cloudflare Free                                 │
│                                                     │
│ Backup:                                             │
│ └─ S3 $0.50/mês                                    │
│                                                     │
│ Monitoramento:                                      │
│ └─ Uptime Robot + Grafana Cloud (Free)            │
│                                                     │
├─────────────────────────────────────────────────────┤
│ CUSTO TOTAL: $11.40/mês = R$ 57/mês               │
├─────────────────────────────────────────────────────┤
│ RECEITA: R$ 600/mês                                │
│ LUCRO: R$ 543/mês (90% margem)                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎓 Lições Aprendidas

### 1. Não Otimize Prematuramente

```
❌ ERRADO: Provisionar para 100 tenants desde o início
✅ CERTO: Começar pequeno, escalar conforme necessário
```

### 2. Margem de Lucro Alta no Início

```
Com 2 tenants: 90% margem
Com 10 tenants: 98% margem
Com 50 tenants: 95% margem

SaaS escala MUITO bem!
```

### 3. Infraestrutura Simples = Menos Bugs

```
Lightsail + Docker Compose:
- Fácil de debugar
- Fácil de fazer backup
- Fácil de migrar
```

---

## 📋 Checklist de Deploy

- [ ] Criar conta AWS
- [ ] Provisionar Lightsail $10/mês
- [ ] Configurar Docker Compose
- [ ] Criar bancos (master + 2 tenants)
- [ ] Deploy aplicação
- [ ] Configurar Route53
- [ ] Configurar Cloudflare
- [ ] Setup backup automático S3
- [ ] Configurar monitoramento
- [ ] Testar provisionamento de tenant
- [ ] Documentar credenciais

---

**Resumo**: Com apenas 2 tenants, use **Lightsail $10/mês**. Lucro de **R$ 543/mês** (90% margem)!

Quer que eu crie o docker-compose.yml completo e os scripts de deploy?
