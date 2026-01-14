# 🎓 Guia de Aprendizado: Construindo o OPS CRM

## 📚 Índice de Aprendizado

Este guia te ensina **PASSO A PASSO** como construir o sistema, explicando cada conceito.

---

## 🏗️ PARTE 1: Entendendo a Arquitetura

### O que vamos construir?

```
┌─────────────────────────────────────────────────────┐
│                    USUÁRIO                          │
│         (Empresa de Energia Solar)                  │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              NAVEGADOR WEB                          │
│   solar-abc.seucrm.com                             │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│           NOSSA APLICAÇÃO                           │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐               │
│  │   DJANGO     │  │   FASTAPI    │               │
│  │   (Admin)    │  │   (APIs)     │               │
│  └──────┬───────┘  └──────┬───────┘               │
│         │                  │                        │
│         └────────┬─────────┘                        │
│                  ▼                                   │
│         ┌────────────────┐                          │
│         │   POSTGRESQL   │                          │
│         │  (3 bancos)    │                          │
│         └────────────────┘                          │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  REDIS   │  │ RABBITMQ │  │  CELERY  │        │
│  │ (Cache)  │  │ (Fila)   │  │ (Tasks)  │        │
│  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────┘
```

### Por que cada componente?

#### 1. **Django** (Framework Web)
```
O QUE É: Framework Python para web
POR QUÊ: Tem admin pronto, ORM poderoso, seguro
USA PARA: Painel administrativo, gerenciar dados
```

#### 2. **FastAPI** (Framework de APIs)
```
O QUE É: Framework Python moderno para APIs
POR QUÊ: Rápido, assíncrono, documentação automática
USA PARA: APIs REST que o frontend consome
```

#### 3. **PostgreSQL** (Banco de Dados)
```
O QUE É: Banco de dados relacional
POR QUÊ: Robusto, ACID, suporta JSON, multi-tenant
USA PARA: Armazenar todos os dados (clientes, produtos, etc)
```

#### 4. **Redis** (Cache)
```
O QUE É: Banco de dados em memória (RAM)
POR QUÊ: Extremamente rápido (100x mais que PostgreSQL)
USA PARA: Cache de dados frequentes, sessões
```

#### 5. **RabbitMQ** (Fila de Mensagens)
```
O QUE É: Sistema de filas
POR QUÊ: Desacopla tarefas, garante entrega
USA PARA: Enviar emails, gerar PDFs, alertas
```

#### 6. **Celery** (Processamento Assíncrono)
```
O QUE É: Sistema de tarefas em background
POR QUÊ: Não trava a aplicação em tarefas lentas
USA PARA: Gerar PDF, enviar email, alertas segunda-feira
```

---

## 🎯 PARTE 2: Conceitos Fundamentais

### 2.1 - O que é DDD (Domain-Driven Design)?

**Problema**: Código vira bagunça quando cresce

**Solução DDD**: Organizar por "domínios de negócio"

#### Exemplo Prático:

```
❌ SEM DDD (Bagunça):
models.py (1000 linhas)
views.py (800 linhas)
utils.py (500 linhas)

✅ COM DDD (Organizado):
contexts/
├── cadastros/          ← Tudo sobre clientes/vendedores
│   ├── domain/         ← Regras de negócio
│   ├── application/    ← Casos de uso
│   └── infrastructure/ ← Banco, APIs
│
├── catalogo/           ← Tudo sobre produtos
│   ├── domain/
│   ├── application/
│   └── infrastructure/
│
└── orcamentos/         ← Tudo sobre orçamentos
    ├── domain/
    ├── application/
    └── infrastructure/
```

#### Camadas do DDD:

```
┌─────────────────────────────────────────┐
│ 1. DOMAIN (Regras de Negócio)          │
│    - Entities (Cliente, Produto)        │
│    - Value Objects (CPF, Email)         │
│    - Domain Services (Cálculos)         │
└─────────────────────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│ 2. APPLICATION (Casos de Uso)          │
│    - CriarCliente                       │
│    - AtualizarProduto                   │
│    - GerarOrcamento                     │
└─────────────────────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│ 3. INFRASTRUCTURE (Detalhes Técnicos)  │
│    - PostgreSQL                         │
│    - APIs REST                          │
│    - Cache                              │
└─────────────────────────────────────────┘
```

**Regra de Ouro**: Domain NUNCA depende de Infrastructure!

---

### 2.2 - O que é SOLID?

**5 Princípios para código limpo**

#### S - Single Responsibility (Uma Responsabilidade)

```python
# ❌ ERRADO: Classe faz tudo
class Cliente:
    def salvar_no_banco(self):
        pass
    
    def enviar_email(self):
        pass
    
    def calcular_desconto(self):
        pass

# ✅ CERTO: Cada classe uma coisa
class Cliente:
    """Só representa um cliente"""
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

class ClienteRepository:
    """Só salva no banco"""
    def salvar(self, cliente):
        pass

class EmailService:
    """Só envia email"""
    def enviar(self, email):
        pass
```

#### O - Open/Closed (Aberto para Extensão)

```python
# ❌ ERRADO: Precisa modificar classe para adicionar
class Calculadora:
    def calcular(self, tipo):
        if tipo == "simples":
            return self.calculo_simples()
        elif tipo == "avancado":
            return self.calculo_avancado()
        # Adicionar novo tipo = modificar aqui!

# ✅ CERTO: Adiciona sem modificar
class Calculadora(ABC):
    @abstractmethod
    def calcular(self):
        pass

class CalculadoraSimples(Calculadora):
    def calcular(self):
        return "simples"

class CalculadoraAvancada(Calculadora):
    def calcular(self):
        return "avancado"

# Adicionar nova? Só criar classe nova!
class CalculadoraIA(Calculadora):
    def calcular(self):
        return "com IA"
```

#### L - Liskov Substitution (Substituível)

```python
# ✅ CERTO: Subclasse pode substituir classe pai
class Produto:
    def calcular_preco(self) -> float:
        return 100.0

class Painel(Produto):
    def calcular_preco(self) -> float:
        return 850.0  # Mesmo tipo de retorno

class Inversor(Produto):
    def calcular_preco(self) -> float:
        return 3500.0  # Mesmo tipo de retorno

# Funciona com qualquer produto!
def mostrar_preco(produto: Produto):
    print(produto.calcular_preco())
```

#### I - Interface Segregation (Interfaces Específicas)

```python
# ❌ ERRADO: Interface gigante
class Repository:
    def create(self): pass
    def read(self): pass
    def update(self): pass
    def delete(self): pass
    def export_pdf(self): pass  # Nem todos precisam!
    def send_email(self): pass  # Nem todos precisam!

# ✅ CERTO: Interfaces pequenas
class ReadRepository:
    def read(self): pass

class WriteRepository:
    def create(self): pass
    def update(self): pass
    def delete(self): pass

class ExportRepository:
    def export_pdf(self): pass
```

#### D - Dependency Inversion (Dependa de Abstrações)

```python
# ❌ ERRADO: Depende de implementação concreta
class CriarCliente:
    def __init__(self):
        self.repo = PostgreSQLRepository()  # Acoplado!
    
    def executar(self, dados):
        cliente = Cliente(dados)
        self.repo.salvar(cliente)

# ✅ CERTO: Depende de abstração
class CriarCliente:
    def __init__(self, repository: ClienteRepository):  # Interface!
        self.repository = repository
    
    def executar(self, dados):
        cliente = Cliente(dados)
        self.repository.salvar(cliente)

# Pode usar qualquer implementação:
repo_postgres = PostgreSQLRepository()
repo_mongo = MongoDBRepository()
repo_memoria = InMemoryRepository()  # Para testes!

use_case = CriarCliente(repo_postgres)  # Injeta dependência
```

---

### 2.3 - O que é Complexidade Ciclomática?

**Definição**: Número de caminhos diferentes no código

#### Exemplo:

```python
# Complexidade = 1 (sem if/for/while)
def somar(a, b):
    return a + b

# Complexidade = 2 (1 if)
def eh_maior_idade(idade):
    if idade >= 18:  # +1
        return True
    return False

# Complexidade = 5 (4 ifs)
def validar_cliente(cliente):
    if not cliente.nome:  # +1
        raise Error()
    if not cliente.email:  # +1
        raise Error()
    if not cliente.cpf:  # +1
        raise Error()
    if cliente.idade < 18:  # +1
        raise Error()
    return True
```

#### Como Reduzir:

```python
# ❌ Complexidade = 5
def validar_cliente(cliente):
    if not cliente.nome:
        raise Error("Nome inválido")
    if not cliente.email:
        raise Error("Email inválido")
    if not cliente.cpf:
        raise Error("CPF inválido")
    if cliente.idade < 18:
        raise Error("Menor de idade")
    return True

# ✅ Complexidade = 2 (por função)
class ClienteValidator:
    def validar(self, cliente):
        self._validar_nome(cliente)
        self._validar_email(cliente)
        self._validar_cpf(cliente)
        self._validar_idade(cliente)
    
    def _validar_nome(self, cliente):
        if not cliente.nome:  # Complexidade = 2
            raise Error("Nome inválido")
    
    def _validar_email(self, cliente):
        if not cliente.email:  # Complexidade = 2
            raise Error("Email inválido")
```

**Meta**: Manter complexidade < 10 por função

---

## 🛠️ PARTE 3: Estrutura do Projeto Explicada

### 3.1 - Por que Docker?

**Problema**: "Na minha máquina funciona!"

**Solução**: Docker = Empacotar tudo (código + dependências)

```
SEM DOCKER:
- Instalar Python 3.11
- Instalar PostgreSQL
- Instalar Redis
- Instalar RabbitMQ
- Configurar tudo
- Rezar para funcionar

COM DOCKER:
- docker-compose up
- Pronto! ✅
```

### 3.2 - O que é docker-compose.yml?

**Arquivo que define todos os serviços**

```yaml
# Cada "service" é um container (mini-servidor)

services:
  postgres:           # Container do banco
    image: postgres   # Imagem pronta do Docker Hub
    ports:
      - "5432:5432"   # Porta: host:container
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Persistir dados
  
  django:             # Container do Django
    build: ./backend  # Constrói da pasta backend
    ports:
      - "8000:8000"
    depends_on:       # Só inicia depois do postgres
      - postgres
```

**Comandos Importantes**:
```bash
docker-compose up -d      # Sobe tudo em background
docker-compose ps         # Ver status
docker-compose logs -f    # Ver logs em tempo real
docker-compose down       # Desliga tudo
docker-compose restart    # Reinicia
```

---

## 📂 PARTE 4: Estrutura de Pastas Explicada

```
OPS - CRM/
│
├── backend/                    # Todo código Python
│   │
│   ├── shared/                 # Código compartilhado
│   │   ├── domain/             # Regras de negócio comuns
│   │   │   ├── value_objects/  # CPF, Email, Money
│   │   │   ├── events/         # Eventos de domínio
│   │   │   └── exceptions/     # Erros customizados
│   │   │
│   │   ├── infrastructure/     # Infraestrutura comum
│   │   │   ├── tenant/         # Resolver qual tenant
│   │   │   ├── database/       # Conexão com banco
│   │   │   ├── cache/          # Redis
│   │   │   └── messaging/      # RabbitMQ
│   │   │
│   │   └── application/        # Interfaces comuns
│   │       └── interfaces/     # Contratos (Ports)
│   │
│   ├── contexts/               # Bounded Contexts (DDD)
│   │   │
│   │   ├── cadastros/          # Contexto de Cadastros
│   │   │   ├── domain/         # Regras de negócio
│   │   │   │   ├── entities/   # Cliente, Vendedor
│   │   │   │   ├── value_objects/  # Endereco, Telefone
│   │   │   │   ├── repositories/   # Interfaces
│   │   │   │   └── services/   # Serviços de domínio
│   │   │   │
│   │   │   ├── application/    # Casos de uso
│   │   │   │   ├── use_cases/  # CriarCliente
│   │   │   │   ├── dtos/       # Data Transfer Objects
│   │   │   │   └── validators/ # Validações
│   │   │   │
│   │   │   └── infrastructure/ # Implementações
│   │   │       ├── repositories/   # PostgreSQL
│   │   │       ├── django_models/  # Models Django
│   │   │       └── api/        # Rotas FastAPI
│   │   │
│   │   ├── catalogo/           # Contexto de Catálogo
│   │   │   └── (mesma estrutura)
│   │   │
│   │   └── orcamentos/         # Contexto de Orçamentos
│   │       └── (mesma estrutura)
│   │
│   ├── django_admin/           # Aplicação Django
│   │   ├── settings.py         # Configurações
│   │   ├── urls.py             # Rotas
│   │   └── wsgi.py             # Servidor
│   │
│   ├── fastapi_app/            # Aplicação FastAPI
│   │   ├── main.py             # Entrada
│   │   ├── middleware/         # Middlewares
│   │   └── routers/            # Rotas da API
│   │
│   └── celery_app/             # Aplicação Celery
│       ├── tasks/              # Tarefas assíncronas
│       └── celeryconfig.py     # Configurações
│
├── docs/                       # Documentação
│   ├── 01-BOUNDED-CONTEXTS.md
│   ├── 02-ROADMAP-FASES.md
│   └── ...
│
├── scripts/                    # Scripts utilitários
│   ├── init-db.sql             # Inicializar banco
│   └── backup.sh               # Backup
│
├── docker-compose.yml          # Orquestração Docker
├── .env.example                # Variáveis de ambiente
├── .gitignore                  # Arquivos ignorados
└── README.md                   # Documentação principal
```

---

## 🎓 PARTE 5: Próximos Passos de Aprendizado

### Ordem Recomendada:

```
1. ✅ Entender arquitetura (você está aqui!)
2. 📝 Criar Value Objects (CPF, Email)
3. 🏗️ Criar primeira Entity (Cliente)
4. 💾 Criar Repository (salvar Cliente)
5. 🎯 Criar Use Case (CriarCliente)
6. 🌐 Criar API (POST /clientes)
7. 🧪 Criar Testes
8. 🔄 Repetir para outras entidades
```

---

## 📚 Glossário de Termos

```
Entity: Objeto com identidade única (Cliente, Produto)
Value Object: Objeto sem identidade (CPF, Email)
Repository: Salva/busca dados no banco
Use Case: Ação que o usuário faz (CriarCliente)
DTO: Objeto para transferir dados entre camadas
Port: Interface (contrato)
Adapter: Implementação de um Port
Domain Service: Lógica de negócio complexa
Infrastructure: Detalhes técnicos (banco, API)
```

---

## ❓ Perguntas Frequentes

**P: Por que separar em tantas camadas?**
R: Para isolar mudanças. Se trocar PostgreSQL por MongoDB, só muda Infrastructure.

**P: Por que usar interfaces (Ports)?**
R: Para testar sem banco real. Usa InMemoryRepository nos testes.

**P: Complexidade ciclomática importa mesmo?**
R: Sim! Código com complexidade alta = bugs e difícil de manter.

**P: Preciso seguir DDD à risca?**
R: Não! Use o que faz sentido. Pragmatismo > Purismo.

---

Pronto para começar a implementar? Vou te guiar passo a passo! 🚀

Qual parte quer implementar primeiro?
1. Value Objects (CPF, Email)
2. Entity Cliente
3. Repository
4. Use Case
