# 04 - Capacity Planning & Cost Calculator

## 📊 Metodologia de Cálculo

Este documento contém todas as fórmulas e cálculos para dimensionar infraestrutura de aplicações SaaS multi-tenant.

---

## 🎯 Premissas do Projeto

### Modelo de Negócio
- **Arquitetura**: Multi-tenant (database-per-tenant)
- **Plano MVP**: R$ 300/mês (2 usuários + 1 agente IA)
- **Trial**: 7 dias gratuito
- **Crescimento esperado**: 10 tenants/mês (conservador)

### Perfil de Uso (MVP)
- **Usuários por tenant**: 2
- **Sessões simultâneas**: 60% (1.2 usuários online)
- **Requests por usuário/hora**: 120 (2 req/min)
- **Horário comercial**: 8h-18h (10h/dia)
- **Dias úteis**: 22 dias/mês

---

## 📐 Fórmulas Base

### 1. Cálculo de Usuários Ativos

```
Total de Usuários = Tenants × Usuários por Tenant
Usuários Simultâneos = Total de Usuários × Taxa de Concorrência
Usuários no Pico = Usuários Simultâneos × Fator de Pico
```

**Exemplo (10 tenants)**:
```
Total = 10 × 2 = 20 usuários
Simultâneos = 20 × 0.60 = 12 usuários
Pico (30% acima) = 12 × 1.30 = 15.6 ≈ 16 usuários
```

### 2. Cálculo de Requests

```
Requests/Hora = Usuários Simultâneos × Requests por Usuário/Hora
Requests/Segundo (RPS) = Requests/Hora ÷ 3600
RPS no Pico = RPS × Fator de Pico
```

**Exemplo (10 tenants)**:
```
Req/Hora = 12 × 120 = 1,440 req/h
RPS = 1,440 ÷ 3,600 = 0.4 req/s
RPS Pico = 0.4 × 1.30 = 0.52 req/s
```

### 3. Cálculo de Throughput de Dados

```
Tamanho Médio Request = Payload JSON (KB)
Tamanho Médio Response = Payload JSON + Assets (KB)
Throughput = RPS × (Request Size + Response Size)
```

**Exemplo**:
```
Request = 2 KB (JSON)
Response = 50 KB (JSON + imagens pequenas)
Throughput = 0.52 × (2 + 50) = 27 KB/s = 0.027 MB/s
```

---

## 💾 Dimensionamento de Storage

### Fórmula Geral

```
Storage Total = Storage por Tenant × Número de Tenants × Fator de Crescimento
```

### Breakdown por Entidade

#### Clientes
```
Registros por Tenant/Mês = 10 (conservador)
Tamanho por Registro = 2 KB (JSON com endereço)
Storage/Tenant/Mês = 10 × 2 KB = 20 KB
Storage/Tenant/Ano = 20 KB × 12 = 240 KB
```

#### Produtos (Catálogo)
```
Produtos por Tenant = 200 (catálogo completo)
Tamanho por Produto = 5 KB (specs + preço)
Imagens por Produto = 3 × 100 KB = 300 KB
Storage/Tenant = (5 KB + 300 KB) × 200 = 61 MB
```

#### Orçamentos
```
Orçamentos/Tenant/Mês = 30
Tamanho por Orçamento = 10 KB (kit + cálculos)
PDF por Orçamento = 500 KB
Storage/Tenant/Mês = 30 × (10 KB + 500 KB) = 15.3 MB
Storage/Tenant/Ano = 15.3 MB × 12 = 183.6 MB
```

#### Logs e Auditoria
```
Eventos/Tenant/Dia = 500
Tamanho por Evento = 1 KB
Retenção = 90 dias
Storage/Tenant = 500 × 1 KB × 90 = 45 MB
```

### Storage Total por Tenant (Ano 1)

```
Clientes:     0.24 MB
Produtos:    61.00 MB
Orçamentos: 183.60 MB
Logs:        45.00 MB
Outros:      10.00 MB (vendedores, fornecedores, etc)
─────────────────────
TOTAL:      299.84 MB ≈ 300 MB/tenant/ano
```

### Projeção Multi-Tenant

| Tenants | Storage (GB) | Com Overhead 30% | Com Backup 2x |
|---------|--------------|------------------|---------------|
| 10      | 3.0          | 3.9              | 7.8           |
| 50      | 15.0         | 19.5             | 39.0          |
| 100     | 30.0         | 39.0             | 78.0          |
| 500     | 150.0        | 195.0            | 390.0         |

**Fórmula**:
```
Storage Real = (Storage Base × Tenants × 1.30) × 2
```

---

## 🖥️ Dimensionamento de Compute (CPU/RAM)

### Fórmula de CPU

```
CPU Necessária = (RPS × Tempo de Processamento) ÷ Núcleos Disponíveis
```

**Premissas**:
- Tempo médio de processamento: 50ms (0.05s)
- Eficiência por core: 80%

**Exemplo (10 tenants)**:
```
RPS Pico = 0.52 req/s
CPU = (0.52 × 0.05) ÷ 0.80 = 0.0325 cores
Arredondando: 1 core (sobra de capacidade)
```

### Fórmula de RAM

#### RAM para Aplicação

```
RAM Base = 512 MB (Django + FastAPI)
RAM por Request Concorrente = 10 MB
RAM para Cache = 20% do total
RAM Total = (RAM Base + (Concurrent Requests × RAM/Request)) × 1.20
```

**Exemplo (10 tenants)**:
```
Concurrent Requests = 16 (pico)
RAM App = 512 + (16 × 10) = 672 MB
RAM com Cache = 672 × 1.20 = 806 MB ≈ 1 GB
```

#### RAM para Database Connections

```
Conexões por Tenant = 5 (pool)
RAM por Conexão = 5 MB
RAM DB Connections = Tenants × Conexões × RAM/Conexão
```

**Exemplo (10 tenants)**:
```
RAM = 10 × 5 × 5 MB = 250 MB
```

#### RAM Total

```
RAM Total = RAM App + RAM DB Connections + RAM OS
RAM Total = 1 GB + 0.25 GB + 0.5 GB = 1.75 GB ≈ 2 GB
```

### Tabela de Dimensionamento

| Tenants | RPS Pico | CPU Cores | RAM (GB) | Instância AWS |
|---------|----------|-----------|----------|---------------|
| 1-10    | 0.52     | 1         | 2        | t3.small      |
| 11-50   | 2.60     | 2         | 4        | t3.medium     |
| 51-100  | 5.20     | 2         | 8        | t3.large      |
| 101-500 | 26.00    | 4         | 16       | t3.xlarge     |

---

## 🗄️ Dimensionamento de Database

### Fórmula de Conexões

```
Conexões Totais = Tenants × Pool Size × Safety Factor
Max Connections PostgreSQL = Conexões Totais × 1.50
```

**Exemplo (10 tenants)**:
```
Conexões = 10 × 5 × 1.20 = 60
Max Connections = 60 × 1.50 = 90
```

### Fórmula de IOPS

```
IOPS = (Writes/s + Reads/s) × Safety Factor
Writes/s = RPS × 0.30 (30% são writes)
Reads/s = RPS × 0.70 (70% são reads)
```

**Exemplo (10 tenants)**:
```
Writes = 0.52 × 0.30 = 0.156 w/s
Reads = 0.52 × 0.70 = 0.364 r/s
IOPS = (0.156 + 0.364) × 2.0 = 1.04 IOPS
```

### RAM para PostgreSQL

```
RAM Base = 256 MB (PostgreSQL overhead)
Shared Buffers = 25% da RAM disponível
Effective Cache = 50% da RAM disponível
Work Mem = RAM / Max Connections
```

**Exemplo (RDS db.t3.small = 2 GB)**:
```
Shared Buffers = 2 GB × 0.25 = 512 MB
Effective Cache = 2 GB × 0.50 = 1 GB
Work Mem = 2 GB / 90 = 22 MB
```

### Tabela de Dimensionamento Database

| Tenants | Storage (GB) | IOPS | Conexões | RAM (GB) | RDS Instance |
|---------|--------------|------|----------|----------|--------------|
| 1-10    | 20           | 100  | 90       | 2        | db.t3.micro  |
| 11-50   | 50           | 500  | 300      | 4        | db.t3.small  |
| 51-100  | 100          | 1000 | 600      | 8        | db.t3.medium |
| 101-500 | 500          | 3000 | 3000     | 16       | db.t3.large  |

---

## 🔴 Dimensionamento de Redis (Cache)

### Fórmula de Cache Size

```
Cache Hit Ratio Target = 80%
Dados Quentes = Storage Total × 0.20 (20% dos dados)
Cache Size = Dados Quentes × Tenants × Safety Factor
```

**Exemplo (10 tenants)**:
```
Storage/Tenant = 300 MB
Dados Quentes = 300 MB × 0.20 = 60 MB
Cache = 60 MB × 10 × 1.50 = 900 MB ≈ 1 GB
```

### Objetos em Cache

#### Tenant Info
```
Tenants = 10
Tamanho por Tenant = 5 KB (connection string, config)
Total = 10 × 5 KB = 50 KB
```

#### Session Data
```
Usuários Simultâneos = 16
Tamanho por Session = 10 KB
Total = 16 × 10 KB = 160 KB
```

#### Query Cache
```
Queries Populares = 100
Tamanho Médio = 50 KB
Total = 100 × 50 KB = 5 MB
```

#### Total Redis

```
Tenant Info:    0.05 MB
Sessions:       0.16 MB
Query Cache:    5.00 MB
Overhead 20%:   1.04 MB
─────────────────────
TOTAL:          6.25 MB ≈ 10 MB (com margem)
```

### Tabela de Dimensionamento Redis

| Tenants | Cache Size (MB) | ElastiCache Instance |
|---------|-----------------|----------------------|
| 1-10    | 256             | cache.t3.micro       |
| 11-50   | 512             | cache.t3.small       |
| 51-100  | 1024            | cache.t3.medium      |
| 101-500 | 2048            | cache.t3.large       |

---

## 📨 Dimensionamento de Message Queue (RabbitMQ)

### Fórmula de Mensagens

```
Mensagens/Dia = Eventos de Domínio × Tenants
Mensagens/Segundo = Mensagens/Dia ÷ 86400
Queue Size = Mensagens/Segundo × Tempo de Retenção (s)
```

**Exemplo (10 tenants)**:
```
Eventos/Tenant/Dia = 500
Mensagens/Dia = 500 × 10 = 5,000
Mensagens/s = 5,000 ÷ 86,400 = 0.058 msg/s
Queue Size (1h retenção) = 0.058 × 3,600 = 209 mensagens
```

### Storage para Mensagens

```
Tamanho Médio Mensagem = 2 KB
Storage = Queue Size × Tamanho Mensagem × Safety Factor
```

**Exemplo**:
```
Storage = 209 × 2 KB × 2.0 = 836 KB ≈ 1 MB
```

### RAM para RabbitMQ

```
RAM Base = 256 MB (RabbitMQ overhead)
RAM por Mensagem = 1 KB
RAM Total = RAM Base + (Queue Size × RAM/Mensagem) × Queues
```

**Exemplo (5 queues)**:
```
RAM = 256 MB + (209 × 1 KB × 5) = 256 MB + 1 MB = 257 MB ≈ 512 MB
```

### Tabela de Dimensionamento RabbitMQ

| Tenants | Msg/s | Queue Size | RAM (MB) | Instance     |
|---------|-------|------------|----------|--------------|
| 1-10    | 0.06  | 200        | 512      | t3.micro     |
| 11-50   | 0.29  | 1000       | 1024     | t3.small     |
| 51-100  | 0.58  | 2000       | 2048     | t3.medium    |
| 101-500 | 2.90  | 10000      | 4096     | t3.large     |

---

## 📊 Dimensionamento de Bandwidth

### Fórmula de Tráfego

```
Tráfego/Mês = (Request Size + Response Size) × RPS × Segundos/Mês
Segundos/Mês = 30 dias × 10h/dia × 3600s/h = 1,080,000s
```

**Exemplo (10 tenants)**:
```
Request = 2 KB
Response = 50 KB
RPS = 0.52
Tráfego = (2 + 50) KB × 0.52 × 1,080,000
Tráfego = 29,203,200 KB = 27.8 GB/mês
```

### Breakdown de Tráfego

```
API Requests:     30% = 8.3 GB
Dashboard SSE:    10% = 2.8 GB
PDF Downloads:    40% = 11.1 GB
Assets (CSS/JS):  20% = 5.6 GB
```

### Tabela de Bandwidth

| Tenants | Tráfego/Mês (GB) | AWS Data Transfer Cost |
|---------|------------------|------------------------|
| 1-10    | 28               | $2.52 (0.09/GB)        |
| 11-50   | 140              | $12.60                 |
| 51-100  | 280              | $25.20                 |
| 101-500 | 1400             | $126.00                |

---

## 💰 Cálculo de Custos AWS (MVP - 10 Tenants)

### Compute (EC2)

#### App Server (Django + FastAPI)
```
Instância: t3.small
vCPU: 2
RAM: 2 GB
Custo: $0.0208/hora
Custo/Mês: $0.0208 × 730h = $15.18
```

#### RabbitMQ Server
```
Instância: t3.micro
vCPU: 2
RAM: 1 GB
Custo: $0.0104/hora
Custo/Mês: $0.0104 × 730h = $7.59
```

**Total Compute: $22.77**

---

### Database (RDS PostgreSQL)

#### Master Database
```
Instância: db.t3.micro
vCPU: 2
RAM: 1 GB
Storage: 20 GB (SSD)
Custo Instância: $0.017/hora × 730h = $12.41
Custo Storage: 20 GB × $0.115/GB = $2.30
Backup: 20 GB × $0.095/GB = $1.90
Total: $16.61
```

#### Tenants Database
```
Instância: db.t3.small
vCPU: 2
RAM: 2 GB
Storage: 50 GB (SSD)
Custo Instância: $0.034/hora × 730h = $24.82
Custo Storage: 50 GB × $0.115/GB = $5.75
Backup: 50 GB × $0.095/GB = $4.75
Total: $35.32
```

**Total Database: $51.93**

---

### Cache (ElastiCache Redis)

```
Instância: cache.t3.micro
RAM: 0.5 GB
Custo: $0.017/hora
Custo/Mês: $0.017 × 730h = $12.41
```

**Total Cache: $12.41**

---

### Storage (S3)

```
PDFs Gerados/Mês: 300 (30 orçamentos × 10 tenants)
Tamanho Médio: 500 KB
Storage/Mês: 300 × 500 KB = 150 MB = 0.15 GB
Custo Storage: 0.15 GB × $0.023/GB = $0.003
Requests (PUT): 300 × $0.005/1000 = $0.0015
Requests (GET): 900 × $0.0004/1000 = $0.00036
Total: $0.005 ≈ $0.01
```

**Total S3: $0.01**

---

### Data Transfer

```
Tráfego/Mês: 28 GB
Primeiro 1 GB: Grátis
Restante: 27 GB × $0.09/GB = $2.43
```

**Total Transfer: $2.43**

---

### Outros Serviços

#### Route53 (DNS)
```
Hosted Zone: $0.50/mês
Queries: 1M queries × $0.40/1M = $0.40
Total: $0.90
```

#### CloudWatch (Monitoring)
```
Métricas: 50 métricas × $0.30 = $15.00
Logs: 5 GB × $0.50/GB = $2.50
Total: $17.50
```

#### Certificate Manager (SSL)
```
Custo: $0 (grátis para certificados públicos)
```

**Total Outros: $18.40**

---

## 📋 Resumo de Custos (10 Tenants)

| Serviço | Custo/Mês | % do Total |
|---------|-----------|------------|
| Compute (EC2) | $22.77 | 21.0% |
| Database (RDS) | $51.93 | 47.9% |
| Cache (Redis) | $12.41 | 11.4% |
| Storage (S3) | $0.01 | 0.0% |
| Data Transfer | $2.43 | 2.2% |
| Outros (DNS, Monitoring) | $18.40 | 17.0% |
| **TOTAL** | **$107.95** | **100%** |

### Arredondamento
```
Custo Real: $107.95
Margem de Segurança (20%): $21.59
TOTAL ESTIMADO: $129.54 ≈ $130/mês
```

---

## 📈 Projeção de Crescimento

### Fórmula de Escala

```
Custo(n) = Custo_Base + (Custo_Variável × Tenants)

Onde:
Custo_Base = Infraestrutura fixa (Master DB, DNS, etc)
Custo_Variável = Custo incremental por tenant
```

### Breakdown de Custos

```
Custo Base (fixo):
- Master DB: $16.61
- DNS: $0.90
- Monitoring: $17.50
Total Base: $35.01

Custo Variável (por tenant):
- Compute: $22.77 ÷ 10 = $2.28/tenant
- Tenants DB: $35.32 ÷ 10 = $3.53/tenant
- Cache: $12.41 ÷ 10 = $1.24/tenant
- Transfer: $2.43 ÷ 10 = $0.24/tenant
Total Variável: $7.29/tenant
```

### Tabela de Projeção

| Tenants | Custo Base | Custo Variável | Total/Mês | Receita (R$300) | Lucro Bruto |
|---------|------------|----------------|-----------|-----------------|-------------|
| 10      | $35        | $73            | $108      | R$ 3,000        | R$ 2,460    |
| 20      | $35        | $146           | $181      | R$ 6,000        | R$ 5,095    |
| 50      | $50        | $365           | $415      | R$ 15,000       | R$ 12,925   |
| 100     | $70        | $729           | $799      | R$ 30,000       | R$ 26,005   |
| 200     | $100       | $1,458         | $1,558    | R$ 60,000       | R$ 52,210   |

**Conversão USD → BRL: 1 USD = R$ 5.00**

---

## 🎯 Break-Even Analysis

### Fórmula

```
Break-Even = Custo Fixo ÷ (Receita por Tenant - Custo Variável por Tenant)
```

**Cálculo**:
```
Custo Fixo Mensal: $35
Receita/Tenant: R$ 300 = $60
Custo Variável/Tenant: $7.29
Margem/Tenant: $60 - $7.29 = $52.71

Break-Even = $35 ÷ $52.71 = 0.66 tenants
```

**Resultado**: Com **1 tenant pagante**, já cobre custos fixos.

---

## 🔧 Otimizações de Custo

### 1. Reserved Instances (1 ano)

```
Economia: 30-40%
EC2 t3.small: $15.18 → $10.63 (-30%)
RDS db.t3.small: $24.82 → $17.37 (-30%)
Economia Total: ~$12/mês
```

### 2. Spot Instances (Dev/Test)

```
Economia: 70-90%
Usar para ambientes não-produção
```

### 3. Auto-Scaling

```
Escalar para t3.micro fora do horário comercial
Economia: 50% (12h/dia)
EC2: $15.18 → $7.59
```

### 4. S3 Lifecycle Policies

```
PDFs > 90 dias → S3 Glacier
Custo: $0.023/GB → $0.004/GB (-83%)
```

### 5. CloudFront CDN

```
Cache de assets estáticos
Reduz Data Transfer: 28 GB → 10 GB
Economia: $1.62/mês
```

### Custo Otimizado (10 Tenants)

| Item | Original | Otimizado | Economia |
|------|----------|-----------|----------|
| Compute | $22.77 | $15.94 | $6.83 |
| Database | $51.93 | $36.35 | $15.58 |
| Transfer | $2.43 | $0.90 | $1.53 |
| **TOTAL** | **$108** | **$72** | **$36 (33%)** |

---

## 📊 Métricas de Capacidade

### SLA Targets

```
Uptime: 99.5% = 3.6h downtime/mês
Response Time (p95): < 200ms
Response Time (p99): < 500ms
Error Rate: < 0.1%
```

### Limites de Escala (por instância)

#### t3.small (App Server)
```
Max RPS: 10 req/s
Max Usuários Simultâneos: 100
Max Tenants: 50
```

#### db.t3.small (Database)
```
Max Connections: 300
Max IOPS: 3000
Max Storage: 200 GB
```

### Quando Escalar?

```
CPU > 70% por 5 minutos → Escalar
RAM > 80% por 5 minutos → Escalar
Disk > 85% → Adicionar storage
Connections > 80% do max → Escalar DB
```

---

## 🧮 Calculadora Rápida

### Template de Cálculo

```python
# Inputs
tenants = 10
usuarios_por_tenant = 2
requests_por_usuario_hora = 120
taxa_concorrencia = 0.60
fator_pico = 1.30

# Cálculos
usuarios_totais = tenants * usuarios_por_tenant
usuarios_simultaneos = usuarios_totais * taxa_concorrencia
usuarios_pico = usuarios_simultaneos * fator_pico

requests_hora = usuarios_simultaneos * requests_por_usuario_hora
rps = requests_hora / 3600
rps_pico = rps * fator_pico

# Storage
storage_por_tenant_gb = 0.3  # 300 MB
storage_total_gb = storage_por_tenant_gb * tenants * 1.3 * 2  # overhead + backup

# Custos
custo_base = 35
custo_por_tenant = 7.29
custo_total = custo_base + (custo_por_tenant * tenants)

# Output
print(f"Usuários no pico: {usuarios_pico:.0f}")
print(f"RPS no pico: {rps_pico:.2f}")
print(f"Storage total: {storage_total_gb:.1f} GB")
print(f"Custo mensal: ${custo_total:.2f}")
```

---

## 📚 Referências e Fontes

### AWS Pricing (Região us-east-1)
- EC2: https://aws.amazon.com/ec2/pricing/
- RDS: https://aws.amazon.com/rds/postgresql/pricing/
- ElastiCache: https://aws.amazon.com/elasticache/pricing/
- S3: https://aws.amazon.com/s3/pricing/
- Data Transfer: https://aws.amazon.com/ec2/pricing/on-demand/

### Benchmarks
- PostgreSQL: 1000 IOPS = ~100 req/s (queries simples)
- Redis: 100k ops/s (single instance)
- RabbitMQ: 20k msg/s (single instance)

### Fórmulas de Capacidade
- Google SRE Book: https://sre.google/books/
- AWS Well-Architected Framework
- Martin Kleppmann - Designing Data-Intensive Applications

---

## ✅ Checklist de Validação

Antes de provisionar infraestrutura:

- [ ] Calculou usuários simultâneos no pico?
- [ ] Estimou RPS com margem de segurança?
- [ ] Dimensionou storage com crescimento de 1 ano?
- [ ] Incluiu overhead de 30% em todos os recursos?
- [ ] Calculou custos com margem de 20%?
- [ ] Definiu métricas de auto-scaling?
- [ ] Planejou estratégia de backup?
- [ ] Considerou otimizações de custo?
- [ ] Validou break-even point?
- [ ] Documentou premissas?

---

**Última atualização**: 2024
**Versão**: 1.0
**Autor**: Capacity Planning Template

Use este documento como base para qualquer projeto SaaS!
