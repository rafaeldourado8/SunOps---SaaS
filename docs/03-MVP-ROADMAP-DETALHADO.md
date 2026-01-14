# 03 - MVP Roadmap Detalhado

## 🎯 Objetivo do MVP
Sistema funcional multi-tenant para criar orçamentos de energia solar com cálculos técnicos e geração de propostas.

---

## 🏗️ Stack Tecnológica Definida

### Backend
- **Django**: Admin superadmin + ORM + Auth
- **FastAPI**: APIs assíncronas + Tarefas background
- **Celery**: Processamento assíncrono
- **RabbitMQ**: Message broker

### Cache & Storage
- **Redis**: Cache de tenant info + sessions + rate limiting
- **PostgreSQL**: Database-per-tenant

### Real-time
- **SSE (Server-Sent Events)**: Dashboard updates em tempo real

### Infraestrutura
- **Docker**: Containerização
- **Terraform**: IaC para AWS
- **AWS**: Hospedagem

---

## 💰 Modelo de Cobrança (MVP - 1 Plano)

| Plano | Usuários | Agentes | Preço | Trial |
|-------|----------|---------|-------|-------|
| **Único** | 2 | 1 Vendas | R$ 300/mês | 7 dias |

**Funcionalidades incluídas**:
- ✅ Todos os módulos do dashboard
- ✅ Chat interno de suporte
- ✅ 1 Agente de vendas (IA)
- ✅ Orçamentos ilimitados
- ✅ Relatórios básicos

**Conta SuperAdmin** (você):
- Acesso a todos os tenants
- Dashboard consolidado
- Gestão de billing

---

## 🏛️ Arquitetura DDD + SOLID

### Bounded Contexts (MVP)

```
┌─────────────────────────────────────────────────────────┐
│                    SHARED KERNEL                        │
│  (Tenant Resolution, Auth, Events, Value Objects)      │
└─────────────────────────────────────────────────────────┘
           │              │              │
           ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │CADASTROS │   │ CATÁLOGO │   │ORÇAMENTOS│
    │ Context  │   │ Context  │   │ Context  │
    └──────────┘   └──────────┘   └──────────┘
```

### Estrutura de Diretórios (DDD)

```
backend/
├── shared/                          # Shared Kernel
│   ├── domain/
│   │   ├── value_objects/          # CPF, Email, Money, etc
│   │   ├── events/                 # Domain Events
│   │   └── exceptions/             # Domain Exceptions
│   ├── infrastructure/
│   │   ├── tenant/                 # Tenant Resolution
│   │   ├── database/               # Connection Manager
│   │   ├── cache/                  # Redis
│   │   └── messaging/              # RabbitMQ
│   └── application/
│       └── interfaces/             # Ports (SOLID - DIP)
│
├── contexts/
│   ├── cadastros/                  # Bounded Context
│   │   ├── domain/
│   │   │   ├── entities/          # Cliente, Vendedor, Fornecedor
│   │   │   ├── value_objects/     # Endereco, Telefone
│   │   │   ├── repositories/      # Interfaces (Port)
│   │   │   ├── services/          # Domain Services
│   │   │   └── events/            # ClienteCriado, etc
│   │   ├── application/
│   │   │   ├── use_cases/         # CriarCliente, AtualizarCliente
│   │   │   ├── dtos/              # Input/Output DTOs
│   │   │   └── validators/        # Business Rules Validation
│   │   └── infrastructure/
│   │       ├── repositories/      # Implementação (Adapter)
│   │       ├── django_models/     # Django ORM Models
│   │       └── api/               # FastAPI Routes
│   │
│   ├── catalogo/
│   │   ├── domain/
│   │   │   ├── entities/          # Produto, Marca, Cotacao
│   │   │   ├── value_objects/     # Preco, Validade
│   │   │   ├── repositories/
│   │   │   ├── services/          # CalculadoraPreco
│   │   │   └── events/
│   │   ├── application/
│   │   │   └── use_cases/         # CriarProduto, AtualizarCotacao
│   │   └── infrastructure/
│   │
│   └── orcamentos/
│       ├── domain/
│       │   ├── entities/          # Orcamento, Kit, ItemKit
│       │   ├── value_objects/     # Potencia, Geracao, Payback
│       │   ├── repositories/
│       │   ├── services/          # CalculadoraGeracao, GeradorPDF
│       │   └── events/
│       ├── application/
│       │   └── use_cases/         # CriarOrcamento, MontarKit
│       └── infrastructure/
│
├── django_admin/                   # Django Admin App
│   ├── settings.py
│   ├── urls.py
│   └── superadmin/                # Custom Admin
│
├── fastapi_app/                    # FastAPI App
│   ├── main.py
│   ├── middleware/                # Tenant, Auth, CORS
│   └── routers/                   # API Routes
│
└── celery_app/                     # Celery Tasks
    ├── tasks/
    │   ├── cotacao_alert.py
    │   └── pdf_generation.py
    └── celeryconfig.py
```

---

## 🎨 Princípios SOLID Aplicados

### 1. SRP (Single Responsibility Principle)

**Cada classe tem UMA responsabilidade**

```
❌ ERRADO:
class Cliente:
    def salvar_no_banco()
    def enviar_email()
    def calcular_desconto()

✅ CORRETO:
class Cliente (Entity)              # Regras de negócio
class ClienteRepository (Port)      # Persistência
class EmailService (Service)        # Notificação
class DescontoService (Service)     # Cálculo
```

### 2. OCP (Open/Closed Principle)

**Aberto para extensão, fechado para modificação**

```
# Interface (Port)
class CalculadoraGeracao:
    def calcular(kit: Kit) -> Geracao
        pass

# Implementações (Adapters)
class CalculadoraGeracaoSimples(CalculadoraGeracao)
class CalculadoraGeracaoAvancada(CalculadoraGeracao)  # Com sombreamento
class CalculadoraGeracaoIA(CalculadoraGeracao)        # Com ML
```

### 3. LSP (Liskov Substitution Principle)

**Subclasses devem ser substituíveis**

```
class Produto (Entity):
    def calcular_preco() -> Money

class Painel(Produto):
    def calcular_preco() -> Money  # Mesmo contrato

class Inversor(Produto):
    def calcular_preco() -> Money  # Mesmo contrato
```

### 4. ISP (Interface Segregation Principle)

**Interfaces específicas, não genéricas**

```
❌ ERRADO:
class Repository:
    def create()
    def read()
    def update()
    def delete()
    def search()
    def export()

✅ CORRETO:
class WriteRepository:
    def create()
    def update()
    def delete()

class ReadRepository:
    def read()
    def search()

class ExportRepository:
    def export()
```

### 5. DIP (Dependency Inversion Principle)

**Dependa de abstrações, não de implementações**

```
# Use Case depende de PORT (abstração)
class CriarClienteUseCase:
    def __init__(self, repository: ClienteRepository):  # Interface
        self.repository = repository

# Injeção de dependência (runtime)
repository = ClienteRepositoryPostgres()  # Implementação
use_case = CriarClienteUseCase(repository)
```

---

## 📊 Complexidade Ciclomática

### Regras

| Complexidade | Classificação | Ação |
|--------------|---------------|------|
| 1-5 | Simples | ✅ OK |
| 6-10 | Moderada | ⚠️ Revisar |
| 11-20 | Complexa | 🔴 Refatorar |
| 21+ | Muito Complexa | 🚫 Bloquear PR |

### Ferramentas

- **Python**: `radon`, `pylint`, `flake8`
- **Pre-commit hook**: Bloqueia commit se > 10
- **CI/CD**: Falha build se > 10

### Exemplo de Refatoração

```python
# ❌ Complexidade = 8
def criar_orcamento(dados):
    if not dados.get('cliente_id'):
        raise ValueError()
    if not dados.get('kit'):
        raise ValueError()
    if dados['kit']['potencia'] < 1:
        raise ValueError()
    if dados['kit']['potencia'] > 1000:
        raise ValueError()
    if not dados.get('vendedor_id'):
        raise ValueError()
    # ... mais validações
    return orcamento

# ✅ Complexidade = 2 (por função)
class OrcamentoValidator:
    def validar(self, dados):
        self._validar_cliente(dados)
        self._validar_kit(dados)
        self._validar_vendedor(dados)
    
    def _validar_cliente(self, dados):
        if not dados.get('cliente_id'):
            raise ClienteInvalidoError()
    
    def _validar_kit(self, dados):
        if not dados.get('kit'):
            raise KitInvalidoError()
        self._validar_potencia(dados['kit'])
```

---

## 🗓️ Roadmap MVP - 8 Semanas

### Sprint 1 (Semanas 1-2): Fundação

**Objetivo**: Infraestrutura multi-tenant + Auth

#### Semana 1: Setup

**Dia 1-2: Infraestrutura**
- [ ] Setup Docker Compose (Django + FastAPI + PostgreSQL + Redis + RabbitMQ)
- [ ] Configurar Terraform (básico - EC2, RDS, ElastiCache)
- [ ] Setup repositório Git + CI/CD (GitHub Actions)

**Dia 3-4: Shared Kernel**
- [ ] Tenant Resolution Middleware
- [ ] Connection Manager (database-per-tenant)
- [ ] Cache Manager (Redis)
- [ ] Event Bus (RabbitMQ)

**Dia 5: Value Objects**
- [ ] CPF, CNPJ, Email, Telefone
- [ ] Money (com moeda)
- [ ] Endereco

#### Semana 2: Auth + SuperAdmin

**Dia 1-2: Autenticação**
- [ ] Django User Model (estendido)
- [ ] JWT Token (FastAPI)
- [ ] Middleware de Auth
- [ ] Roles (SuperAdmin, Admin, Vendedor)

**Dia 3-4: Tenant Management**
- [ ] Model Tenant (banco MASTER)
- [ ] Provisionamento de Tenant (manual)
- [ ] Django Admin para Tenants
- [ ] API de Tenant Info

**Dia 5: Testes**
- [ ] Testes unitários (Shared Kernel)
- [ ] Testes de integração (Tenant Resolution)

**Entregável Sprint 1**:
- ✅ Infraestrutura rodando
- ✅ Multi-tenant funcionando
- ✅ Login/Logout
- ✅ SuperAdmin pode criar tenants

---

### Sprint 2 (Semanas 3-4): Contexto Cadastros

**Objetivo**: CRUD completo de Clientes, Vendedores, Fornecedores

#### Semana 3: Domain Layer

**Dia 1-2: Entities**
```python
# cadastros/domain/entities/cliente.py
class Cliente(Entity):
    def __init__(self, nome: str, cpf_cnpj: CpfCnpj, email: Email):
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.email = email
        self.validate()
    
    def validate(self):
        if len(self.nome) < 3:
            raise DomainException("Nome inválido")
```

- [ ] Entity: Cliente
- [ ] Entity: Vendedor
- [ ] Entity: Fornecedor
- [ ] Value Objects: CpfCnpj, Endereco
- [ ] Repository Interfaces (Ports)

**Dia 3-4: Use Cases**
- [ ] CriarClienteUseCase
- [ ] AtualizarClienteUseCase
- [ ] ListarClientesUseCase
- [ ] BuscarClientePorIdUseCase
- [ ] Validators (complexidade < 5)

**Dia 5: Domain Events**
- [ ] ClienteCriado
- [ ] ClienteAtualizado
- [ ] Event Handlers

#### Semana 4: Infrastructure + API

**Dia 1-2: Repositories**
- [ ] ClienteRepositoryPostgres (Adapter)
- [ ] Django Models (ORM)
- [ ] Migrations

**Dia 3-4: FastAPI Routes**
```python
# POST /api/v1/clientes
# GET /api/v1/clientes
# GET /api/v1/clientes/{id}
# PUT /api/v1/clientes/{id}
# DELETE /api/v1/clientes/{id}
```

**Dia 5: Django Admin**
- [ ] Admin customizado para Cliente
- [ ] Filtros e buscas
- [ ] Testes (unitários + integração)

**Entregável Sprint 2**:
- ✅ CRUD Clientes completo
- ✅ CRUD Vendedores completo
- ✅ CRUD Fornecedores completo
- ✅ Django Admin funcional
- ✅ APIs REST documentadas (Swagger)

---

### Sprint 3 (Semanas 5-6): Contexto Catálogo

**Objetivo**: Produtos + Marcas + Cotação com validade

#### Semana 5: Domain + Cotação

**Dia 1-2: Entities**
- [ ] Entity: Produto (abstrata)
- [ ] Entity: Painel (herda Produto)
- [ ] Entity: Inversor (herda Produto)
- [ ] Entity: Estrutura, Cabo, Conector
- [ ] Entity: Marca
- [ ] Entity: Cotacao

**Dia 3-4: Value Objects + Services**
- [ ] VO: Preco (Money + validade)
- [ ] VO: Especificacao (potência, tensão, etc)
- [ ] Service: CalculadoraValidade (3 dias úteis)
- [ ] Service: VerificadorCotacaoExpirada

**Dia 5: Use Cases**
- [ ] CriarProdutoUseCase
- [ ] AtualizarCotacaoUseCase
- [ ] ListarProdutosComPrecoValidoUseCase

#### Semana 6: Alerta + API

**Dia 1-2: Celery Task**
```python
# celery_app/tasks/cotacao_alert.py
@celery.task
def enviar_alerta_cotacao_segunda():
    # Para cada tenant
    # Busca cotações expiradas
    # Envia email/notificação
```
- [ ] Task: AlertaCotacaoSegunda
- [ ] Scheduler (Celery Beat)
- [ ] Email Service

**Dia 3-4: APIs**
- [ ] CRUD Produtos (todas categorias)
- [ ] CRUD Marcas
- [ ] Atualizar Cotação
- [ ] Listar Produtos Válidos

**Dia 5: Django Admin + Testes**
- [ ] Admin para Produtos (inline por tipo)
- [ ] Admin para Cotações
- [ ] Testes

**Entregável Sprint 3**:
- ✅ Catálogo completo
- ✅ Sistema de cotação com validade
- ✅ Alerta automático segunda-feira
- ✅ APIs funcionais

---

### Sprint 4 (Semanas 7-8): Contexto Orçamentos

**Objetivo**: Montar kits + Cálculos + PDF

#### Semana 7: Domain + Cálculos

**Dia 1-2: Entities**
```python
# orcamentos/domain/entities/kit.py
class Kit(Entity):
    def __init__(self):
        self.paineis: List[Painel] = []
        self.inversores: List[Inversor] = []
        self.estruturas: List[Estrutura] = []
    
    def adicionar_painel(self, painel: Painel, quantidade: int):
        self.paineis.append(ItemKit(painel, quantidade))
    
    def calcular_potencia(self) -> Potencia:
        # Soma potência dos painéis
        pass
```

- [ ] Entity: Orcamento
- [ ] Entity: Kit
- [ ] Entity: ItemKit
- [ ] VO: Potencia (kWp)
- [ ] VO: Geracao (kWh/mês)
- [ ] VO: Payback (meses)

**Dia 3-4: Services (Cálculos)**
```python
# orcamentos/domain/services/calculadora_geracao.py
class CalculadoraGeracao:
    def calcular(self, kit: Kit, hsp: float) -> Geracao:
        potencia = kit.calcular_potencia()
        kwh_mes = potencia.valor * hsp * 30 * 0.8
        return Geracao(kwh_mes)

# orcamentos/domain/services/calculadora_payback.py
class CalculadoraPayback:
    def calcular(self, investimento: Money, economia_mensal: Money) -> Payback:
        meses = investimento.valor / economia_mensal.valor
        return Payback(meses)
```

- [ ] Service: CalculadoraGeracao (complexidade < 5)
- [ ] Service: CalculadoraPayback (complexidade < 5)
- [ ] Service: CalculadoraPrecoKit

**Dia 5: Use Cases**
- [ ] CriarOrcamentoUseCase
- [ ] MontarKitUseCase
- [ ] CalcularOrcamentoUseCase

#### Semana 8: PDF + Dashboard + SSE

**Dia 1-2: Geração de PDF**
```python
# orcamentos/domain/services/gerador_pdf.py
class GeradorPDF:
    def gerar(self, orcamento: Orcamento) -> bytes:
        # WeasyPrint ou ReportLab
        # Template HTML → PDF
        pass
```

- [ ] Service: GeradorPDF
- [ ] Template HTML do orçamento
- [ ] Celery Task (geração assíncrona)

**Dia 3: APIs**
- [ ] POST /api/v1/orcamentos
- [ ] POST /api/v1/orcamentos/{id}/kit/adicionar-item
- [ ] POST /api/v1/orcamentos/{id}/calcular
- [ ] POST /api/v1/orcamentos/{id}/gerar-pdf
- [ ] GET /api/v1/orcamentos/{id}/pdf

**Dia 4: Dashboard + SSE**
```python
# fastapi_app/routers/dashboard.py
@router.get("/dashboard/stream")
async def dashboard_stream(request: Request):
    async def event_generator():
        while True:
            # Busca métricas
            data = get_dashboard_data()
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(5)
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

- [ ] Endpoint SSE
- [ ] Dashboard básico (métricas)
- [ ] Frontend (HTML + JS + SSE)

**Dia 5: Testes + Deploy**
- [ ] Testes end-to-end
- [ ] Deploy AWS (Terraform)
- [ ] Documentação

**Entregável Sprint 4 (MVP COMPLETO)**:
- ✅ Montar kit (drag-and-drop)
- ✅ Cálculos automáticos
- ✅ Gerar PDF
- ✅ Dashboard em tempo real
- ✅ Sistema deployado na AWS

---

## 🧪 Estratégia de Testes

### Pirâmide de Testes

```
        /\
       /  \  E2E (10%)
      /────\
     /      \  Integration (30%)
    /────────\
   /          \  Unit (60%)
  /────────────\
```

### Cobertura Mínima

- **Domain Layer**: 90%+ (crítico)
- **Application Layer**: 80%+
- **Infrastructure Layer**: 60%+

### Ferramentas

- **pytest**: Framework de testes
- **pytest-cov**: Cobertura
- **factory_boy**: Fixtures
- **faker**: Dados fake

---

## 🚀 Deploy AWS com Terraform

### Recursos (MVP)

```hcl
# terraform/main.tf

# VPC
resource "aws_vpc" "main" {}

# RDS PostgreSQL (Master)
resource "aws_db_instance" "master" {
  engine = "postgres"
  instance_class = "db.t3.micro"
}

# RDS PostgreSQL (Tenants)
resource "aws_db_instance" "tenants" {
  engine = "postgres"
  instance_class = "db.t3.small"
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  engine = "redis"
  node_type = "cache.t3.micro"
}

# EC2 (Django + FastAPI)
resource "aws_instance" "app" {
  ami = "ami-ubuntu"
  instance_type = "t3.small"
}

# RabbitMQ (CloudAMQP ou self-hosted)
resource "aws_instance" "rabbitmq" {
  ami = "ami-rabbitmq"
  instance_type = "t3.micro"
}

# S3 (PDFs)
resource "aws_s3_bucket" "pdfs" {}

# Route53 (DNS)
resource "aws_route53_zone" "main" {}
```

### Custo Estimado (MVP)

| Recurso | Tipo | Custo/mês |
|---------|------|-----------|
| EC2 App | t3.small | ~$15 |
| RDS Master | t3.micro | ~$15 |
| RDS Tenants | t3.small | ~$30 |
| ElastiCache | t3.micro | ~$12 |
| EC2 RabbitMQ | t3.micro | ~$8 |
| S3 + Transfer | - | ~$5 |
| **Total** | | **~$85/mês** |

---

## 📈 Métricas de Sucesso (MVP)

### Técnicas

- [ ] Complexidade ciclomática < 10 (100% do código)
- [ ] Cobertura de testes > 80%
- [ ] Tempo de resposta API < 200ms (p95)
- [ ] Uptime > 99%

### Negócio

- [ ] Criar orçamento em < 5 minutos
- [ ] Gerar PDF em < 10 segundos
- [ ] 0 bugs críticos em produção
- [ ] 5 tenants ativos (beta)

---

## 🔄 Reaproveitamento de Código

### Shared Kernel (Reutilizável)

Todos os contextos usam:
- Value Objects (CPF, Email, Money)
- Tenant Resolution
- Event Bus
- Cache Manager
- Auth

### Generators/Templates

```bash
# Criar novo bounded context
python manage.py create_context vendas

# Gera estrutura:
# contexts/vendas/domain/
# contexts/vendas/application/
# contexts/vendas/infrastructure/
```

### Base Classes

```python
# shared/domain/entity.py
class Entity(ABC):
    def __init__(self):
        self.id = None
        self.created_at = None
        self.updated_at = None
    
    @abstractmethod
    def validate(self):
        pass

# Todos os contextos herdam
class Cliente(Entity):
    pass
```

---

## 📚 Próximos Passos

1. **Revisar e aprovar roadmap**
2. **Setup ambiente local** (Docker Compose)
3. **Iniciar Sprint 1** (Semana 1)
4. **Daily standups** (15min)
5. **Review semanal**

---

## 🎓 Conceitos para Estudar

### Semana 1-2
- [ ] DDD: Entities, Value Objects, Aggregates
- [ ] SOLID: Todos os princípios
- [ ] Multi-tenancy: Database-per-tenant

### Semana 3-4
- [ ] Repository Pattern
- [ ] Use Cases (Clean Architecture)
- [ ] Domain Events

### Semana 5-6
- [ ] Celery + RabbitMQ
- [ ] Caching strategies (Redis)
- [ ] API Design (REST)

### Semana 7-8
- [ ] SSE (Server-Sent Events)
- [ ] PDF Generation
- [ ] Terraform basics
- [ ] AWS deployment

---

Quer que eu detalhe alguma sprint específica ou crie exemplos de código para algum conceito?
