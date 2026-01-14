# 07 - System Design Cheat Sheet (Big Tech Interviews)

## 🎯 O Framework NUNCA ESQUECER

Use o acrônimo: **"CRUDSS"**

```
C - Clarify (Esclarecer requisitos)
R - Requirements (Requisitos funcionais e não-funcionais)
U - Users (Quantos usuários?)
D - Data (Quanto de dados?)
S - Scale (Escala e crescimento)
S - Services (Quebrar em serviços)
```

---

## 📐 As 5 Fórmulas Mágicas

### 1️⃣ Fórmula do Tráfego (QPS/RPS)

```
┌─────────────────────────────────────────┐
│ RPS = DAU × Ações/Dia ÷ 86400          │
└─────────────────────────────────────────┘

Onde:
- DAU = Daily Active Users
- 86400 = segundos em 1 dia
- Ações/Dia = quantas vezes o usuário usa por dia
```

**Macete**: 
```
100k DAU × 10 ações = 1M ações/dia
1M ÷ 100k = 10 RPS (arredonda 86400 para 100k)
```

**Exemplo Prático**:
```
Instagram: 1 bilhão DAU × 50 ações/dia
= 50 bilhões ações/dia
÷ 86400 = 578k RPS

Twitter: 200M DAU × 20 tweets/dia
= 4 bilhões ações/dia
÷ 86400 = 46k RPS
```

---

### 2️⃣ Fórmula de Storage

```
┌─────────────────────────────────────────┐
│ Storage = Usuários × Dados/User × Anos │
│         × Crescimento × Replicação      │
└─────────────────────────────────────────┘
```

**Macete - Tabela de Tamanhos**:
```
Texto curto (tweet):     300 bytes
Texto médio (post):      2 KB
Imagem thumbnail:        100 KB
Imagem HD:               2 MB
Vídeo 1min (720p):       50 MB
Vídeo 1min (1080p):      100 MB
```

**Exemplo**:
```
WhatsApp: 2B usuários × 100 msgs/dia × 1 KB
= 2B × 100 × 1 KB = 200 TB/dia
× 365 dias = 73 PB/ano
× 3 (replicação) = 219 PB/ano
```

---

### 3️⃣ Fórmula de Bandwidth

```
┌─────────────────────────────────────────┐
│ Bandwidth = RPS × Tamanho Médio Request│
└─────────────────────────────────────────┘
```

**Macete - Conversões Rápidas**:
```
1 KB/s = 86 MB/dia
1 MB/s = 86 GB/dia = 2.5 TB/mês
1 GB/s = 2.5 PB/mês
```

**Exemplo**:
```
YouTube: 1M RPS × 2 MB (vídeo chunk)
= 2 TB/s = 5 PB/mês
```

---

### 4️⃣ Fórmula de Memória (Cache)

```
┌─────────────────────────────────────────┐
│ Cache = Dados Quentes × Hit Ratio       │
│ Dados Quentes = 20% dos dados totais    │
│ Hit Ratio Target = 80%                  │
└─────────────────────────────────────────┘
```

**Regra 80/20 (Pareto)**:
```
20% dos dados = 80% dos acessos
Cache 20% dos dados = 80% hit rate
```

**Exemplo**:
```
Reddit: 100 TB de posts
Dados quentes: 100 TB × 0.20 = 20 TB
Cache necessário: 20 TB (Redis cluster)
```

---

### 5️⃣ Fórmula de Servidores

```
┌─────────────────────────────────────────┐
│ Servidores = RPS ÷ RPS_por_Servidor     │
│            × Safety Factor (2x-3x)      │
└─────────────────────────────────────────┘
```

**Macete - Capacidade por Servidor**:
```
Servidor Típico (4 core, 16 GB):
- API simples: 1000 RPS
- API com DB: 500 RPS
- API com cálculos: 100 RPS
- Streaming: 50 RPS
```

**Exemplo**:
```
Netflix: 100k RPS (streaming)
Servidores = 100k ÷ 50 = 2000 servidores
× 2 (safety) = 4000 servidores
```

---

## 🧮 Números que VOCÊ PRECISA DECORAR

### Latências (De Cor!)

```
┌────────────────────────────────────────┐
│ L1 cache:           0.5 ns             │
│ L2 cache:           7 ns               │
│ RAM:                100 ns             │
│ SSD:                150 μs             │
│ HDD:                10 ms              │
│ Network (datacenter): 0.5 ms           │
│ Network (internet):  50-100 ms         │
│ Disk seek:          10 ms              │
└────────────────────────────────────────┘
```

**Macete Visual**:
```
RAM < SSD < HDD < Network
100ns < 150μs < 10ms < 50ms
```

### Throughput (De Cor!)

```
┌────────────────────────────────────────┐
│ RAM:        100 GB/s                   │
│ SSD:        1 GB/s                     │
│ HDD:        100 MB/s                   │
│ Network:    1 Gbps = 125 MB/s          │
│ Internet:   100 Mbps = 12.5 MB/s       │
└────────────────────────────────────────┘
```

### Disponibilidade (SLA)

```
┌────────────────────────────────────────┐
│ 99%      = 3.65 dias downtime/ano      │
│ 99.9%    = 8.76 horas/ano              │
│ 99.99%   = 52 minutos/ano              │
│ 99.999%  = 5 minutos/ano               │
└────────────────────────────────────────┘
```

**Macete**: Cada "9" = 10x mais caro

---

## 🎨 Padrões de Arquitetura (Decorar!)

### 1. Load Balancer Pattern

```
┌─────────┐
│ Client  │
└────┬────┘
     │
     ▼
┌─────────────┐
│Load Balancer│ ← Nginx, HAProxy, ALB
└──────┬──────┘
       │
   ┌───┴───┐
   ▼       ▼
┌─────┐ ┌─────┐
│App 1│ │App 2│
└─────┘ └─────┘
```

**Quando usar**: RPS > 1000

---

### 2. Cache Pattern

```
┌──────┐
│Client│
└───┬──┘
    │
    ▼
┌────────┐  Cache Miss  ┌──────────┐
│ Cache  │─────────────→│ Database │
│(Redis) │←─────────────│          │
└────────┘  Write Back  └──────────┘
```

**Estratégias**:
- **Cache-Aside**: App gerencia cache
- **Write-Through**: Escreve cache + DB
- **Write-Back**: Escreve cache, depois DB

**Quando usar**: Read/Write > 10:1

---

### 3. Database Sharding

```
┌─────────────────────────────────────┐
│         Shard Key: user_id          │
└─────────────────────────────────────┘
         │
    ┌────┼────┐
    ▼    ▼    ▼
┌──────┬──────┬──────┐
│Shard1│Shard2│Shard3│
│ 0-3M │ 3-6M │ 6-9M │
└──────┴──────┴──────┘
```

**Shard Keys Comuns**:
- User ID (hash)
- Geographic (região)
- Time (data)

**Quando usar**: DB > 1 TB ou QPS > 10k

---

### 4. Message Queue Pattern

```
┌─────────┐    ┌───────┐    ┌──────────┐
│Producer │───→│ Queue │───→│ Consumer │
└─────────┘    │(Kafka)│    └──────────┘
               └───────┘
```

**Quando usar**: 
- Processamento assíncrono
- Desacoplar serviços
- Picos de tráfego

---

### 5. CDN Pattern

```
┌──────┐
│Client│ (Brasil)
└───┬──┘
    │
    ▼
┌─────────┐  Cache Miss  ┌────────────┐
│CDN Edge │─────────────→│Origin Server│
│ (SP)    │←─────────────│   (US)     │
└─────────┘              └────────────┘
```

**Quando usar**: Assets estáticos, global users

---

## 🔢 Técnica do "Back of Envelope"

### Passo a Passo (3 minutos)

```
1. Arredonde TUDO
   1 milhão ≈ 1M
   86400 segundos ≈ 100k
   365 dias ≈ 400 dias

2. Use Potências de 10
   1K = 10³
   1M = 10⁶
   1B = 10⁹
   1T = 10¹²

3. Calcule Ordem de Magnitude
   Não precisa ser exato!
   100k ou 200k? Tanto faz, use 100k

4. Valide com Entrevistador
   "Assumindo X, temos Y. Faz sentido?"
```

### Exemplo Prático (Twitter)

```
Pergunta: "Design Twitter"

1. CLARIFY (30s)
   - Tweets, timeline, follow?
   - Sim, foco em tweets

2. USERS (30s)
   - DAU? 200M
   - Tweets/dia? 500M (2.5 tweets/user)

3. QPS (1min)
   - Write: 500M ÷ 100k = 5k TPS
   - Read: 200M × 100 reads ÷ 100k = 200k QPS
   - Read/Write = 40:1

4. STORAGE (1min)
   - Tweet: 300 bytes
   - 500M × 300 bytes = 150 GB/dia
   - × 365 = 55 TB/ano
   - × 3 (replicação) = 165 TB/ano

5. BANDWIDTH (30s)
   - Write: 5k × 300 bytes = 1.5 MB/s
   - Read: 200k × 300 bytes = 60 MB/s

6. ARCHITECTURE (5min)
   [Desenha diagrama]
```

---

## 🎯 Checklist de Entrevista (Imprima!)

### Fase 1: Requirements (2-3 min)

```
□ Quantos usuários? (DAU, MAU)
□ Quantas operações por usuário/dia?
□ Read-heavy ou write-heavy?
□ Latência esperada? (< 100ms, < 1s)
□ Disponibilidade? (99.9%, 99.99%)
□ Consistência? (Strong, Eventual)
□ Global ou regional?
```

### Fase 2: Estimativas (3-5 min)

```
□ QPS (read + write)
□ Storage (5 anos)
□ Bandwidth (in + out)
□ Cache size (20% dos dados)
□ Número de servidores
```

### Fase 3: High-Level Design (10 min)

```
□ Desenhar componentes principais
□ Load Balancer
□ App Servers
□ Database (SQL vs NoSQL)
□ Cache (Redis)
□ CDN (se global)
□ Message Queue (se assíncrono)
```

### Fase 4: Deep Dive (15 min)

```
□ Database schema
□ API design
□ Sharding strategy
□ Replication
□ Failover
□ Monitoring
```

### Fase 5: Bottlenecks (5 min)

```
□ Single point of failure?
□ Hotspots?
□ Scaling limits?
□ Trade-offs?
```

---

## 🧠 Mnemônicos para NUNCA ESQUECER

### 1. CAP Theorem

```
"Só Pode Escolher 2"

C - Consistency (todos veem mesmos dados)
A - Availability (sempre responde)
P - Partition Tolerance (funciona com rede particionada)

Exemplos:
- CP: MongoDB, HBase (sacrifica availability)
- AP: Cassandra, DynamoDB (sacrifica consistency)
- CA: PostgreSQL (não tolera partição)
```

### 2. ACID vs BASE

```
ACID (SQL):
A - Atomicity (tudo ou nada)
C - Consistency (regras sempre válidas)
I - Isolation (transações isoladas)
D - Durability (dados persistem)

BASE (NoSQL):
B - Basically Available
A - Soft state
S - Eventually consistent
```

### 3. Tipos de Database

```
"RINGO" (lembre da banda!)

R - Relational (PostgreSQL) → Transações
I - In-memory (Redis) → Cache
N - NoSQL Document (MongoDB) → Flexível
G - Graph (Neo4j) → Relacionamentos
O - Object Storage (S3) → Arquivos
```

---

## 📊 Tabela de Decisão Rápida

### Escolher Database

| Caso de Uso | Database | Por quê? |
|-------------|----------|----------|
| Transações financeiras | PostgreSQL | ACID |
| Cache | Redis | In-memory |
| Logs | Elasticsearch | Full-text search |
| Métricas | InfluxDB | Time-series |
| Social graph | Neo4j | Relacionamentos |
| Documentos | MongoDB | Schema flexível |
| Analytics | BigQuery | OLAP |
| Key-Value | DynamoDB | Escala horizontal |

### Escolher Message Queue

| Caso de Uso | Queue | Por quê? |
|-------------|-------|----------|
| Eventos em tempo real | Kafka | High throughput |
| Tarefas assíncronas | RabbitMQ | Confiável |
| Pub/Sub simples | Redis | Baixa latência |
| Serverless | SQS | Managed |

---

## 🎓 Perguntas Clássicas (Top 10)

### 1. Design URL Shortener (bit.ly)

```
Estimativa:
- 100M URLs/mês
- Read/Write = 100:1
- QPS: Write 40, Read 4k

Componentes:
- Hash function (MD5 → base62)
- Database (NoSQL - DynamoDB)
- Cache (Redis)
- CDN (redirect)

Key Insight: Collision handling
```

### 2. Design Instagram

```
Estimativa:
- 1B DAU
- 50M fotos/dia
- 2 MB/foto = 100 TB/dia

Componentes:
- S3 (fotos)
- CDN (CloudFront)
- PostgreSQL (metadata)
- Redis (feed cache)
- Kafka (notifications)

Key Insight: Feed generation (push vs pull)
```

### 3. Design WhatsApp

```
Estimativa:
- 2B usuários
- 100 msgs/dia/user
- 1 KB/msg = 200 TB/dia

Componentes:
- WebSocket (real-time)
- Cassandra (messages)
- Redis (online status)
- Message Queue (delivery)

Key Insight: Message delivery guarantee
```

### 4. Design Netflix

```
Estimativa:
- 200M DAU
- 2h watch/day
- 5 GB/h = 2 PB/dia

Componentes:
- S3 (vídeos)
- CDN (CloudFront)
- Encoding pipeline
- Recommendation engine

Key Insight: Adaptive bitrate streaming
```

### 5. Design Uber

```
Estimativa:
- 100M DAU
- 5 rides/day
- 500M rides/day

Componentes:
- Geospatial index (QuadTree)
- WebSocket (real-time location)
- PostgreSQL (rides)
- Redis (driver location)

Key Insight: Matching algorithm
```

### 6. Design Rate Limiter

```
Algoritmos:
- Token Bucket
- Leaky Bucket
- Fixed Window
- Sliding Window

Implementação:
- Redis (counter)
- Distributed (consistent hashing)

Key Insight: Distributed rate limiting
```

### 7. Design Notification System

```
Tipos:
- Push (mobile)
- Email
- SMS
- In-app

Componentes:
- Message Queue (Kafka)
- Workers (Celery)
- Template engine
- Delivery tracking

Key Insight: Retry logic + idempotency
```

### 8. Design Search Autocomplete

```
Estimativa:
- 1B queries/dia
- 10 suggestions/query

Componentes:
- Trie data structure
- Redis (cache)
- Elasticsearch (full-text)
- Analytics (trending)

Key Insight: Prefix matching + ranking
```

### 9. Design Web Crawler

```
Estimativa:
- 1B pages
- 100 KB/page = 100 TB

Componentes:
- URL frontier (queue)
- DNS resolver
- Robots.txt parser
- Deduplication (Bloom filter)

Key Insight: Politeness + distributed crawling
```

### 10. Design Chat System

```
Estimativa:
- 100M DAU
- 50 msgs/day
- 1 KB/msg = 5 TB/dia

Componentes:
- WebSocket (real-time)
- Cassandra (messages)
- Redis (online users)
- Message Queue (offline delivery)

Key Insight: Read receipts + group chat
```

---

## 🚀 Macete Final: Template Universal

```
┌─────────────────────────────────────────────────────┐
│ QUALQUER SISTEMA SEGUE ESTE PADRÃO:                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Client                                             │
│    ↓                                                │
│  CDN (se global)                                    │
│    ↓                                                │
│  Load Balancer                                      │
│    ↓                                                │
│  API Gateway (rate limit, auth)                     │
│    ↓                                                │
│  App Servers (stateless)                            │
│    ↓                                                │
│  Cache (Redis) ←→ Database (SQL/NoSQL)             │
│    ↓                                                │
│  Message Queue (async tasks)                        │
│    ↓                                                │
│  Workers (background jobs)                          │
│    ↓                                                │
│  Object Storage (S3)                                │
│                                                     │
└─────────────────────────────────────────────────────┘

Adicione conforme necessário:
- Search: Elasticsearch
- Analytics: Data warehouse
- Real-time: WebSocket
- ML: Recommendation engine
```

---

## 📚 Recursos para Estudar

### Livros (Ler ESTES!)

```
1. "Designing Data-Intensive Applications"
   - Martin Kleppmann
   - OBRIGATÓRIO!

2. "System Design Interview" Vol 1 & 2
   - Alex Xu
   - Específico para entrevistas

3. "Database Internals"
   - Alex Petrov
   - Deep dive em databases
```

### Sites

```
- highscalability.com (case studies reais)
- github.com/donnemartin/system-design-primer
- bytebytego.com (newsletter)
```

### Prática

```
1. Desenhe 1 sistema/dia (15 min)
2. Explique em voz alta (simula entrevista)
3. Cronometre (40 min total)
4. Revise com gabarito
```

---

## ✅ Checklist Final (Cole no Monitor!)

```
□ Clarify requirements (2 min)
□ Estimate QPS (1 min)
□ Estimate Storage (1 min)
□ Estimate Bandwidth (1 min)
□ Draw high-level (5 min)
□ Define API (3 min)
□ Design database (5 min)
□ Discuss scaling (5 min)
□ Identify bottlenecks (3 min)
□ Propose solutions (5 min)

TOTAL: 30-40 minutos
```

---

**Dica de Ouro**: Entrevistador quer ver seu PROCESSO DE PENSAMENTO, não a resposta perfeita!

Fale em voz alta, pergunte, valide premissas, mostre trade-offs!

Boa sorte! 🚀
