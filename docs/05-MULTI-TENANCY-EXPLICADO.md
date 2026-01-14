# 05 - Multi-Tenancy: Database-per-Tenant Explicado

## 🎯 O que é um Tenant?

**Tenant = Empresa Cliente do seu SaaS**

No seu caso:
- **Tenant 1**: Solar ABC Ltda (empresa de energia solar)
- **Tenant 2**: Solar XYZ Energia (outra empresa de energia solar)
- **Tenant 3**: Fotovoltaica 123 (mais uma empresa)

Cada empresa que **paga R$ 300/mês** é um tenant diferente.

---

## 🏢 Arquitetura Database-per-Tenant

### Conceito Visual

```
┌─────────────────────────────────────────────────────────────┐
│                    SEU SAAS (seucrm.com)                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Tenant 1     │   │  Tenant 2     │   │  Tenant 3     │
│  Solar ABC    │   │  Solar XYZ    │   │  Fotov. 123   │
├───────────────┤   ├───────────────┤   ├───────────────┤
│ Banco Próprio │   │ Banco Próprio │   │ Banco Próprio │
│ solar_abc_db  │   │ solar_xyz_db  │   │ fotov_123_db  │
└───────────────┘   └───────────────┘   └───────────────┘
```

### Cada Tenant tem:
- ✅ Seu próprio banco de dados PostgreSQL
- ✅ Seus próprios clientes, produtos, orçamentos
- ✅ Seus próprios usuários (vendedores)
- ✅ Dados 100% isolados

---

## 🔍 Como Funciona na Prática

### Exemplo Real

#### Tenant 1: Solar ABC
```
Subdomínio: solar-abc.seucrm.com
Banco: solar_abc_db

Dados no banco:
├── Clientes: João Silva, Maria Santos
├── Vendedores: Carlos (vendedor da Solar ABC)
├── Produtos: 50 painéis, 10 inversores
└── Orçamentos: 15 orçamentos criados
```

#### Tenant 2: Solar XYZ
```
Subdomínio: solar-xyz.seucrm.com
Banco: solar_xyz_db

Dados no banco:
├── Clientes: Pedro Costa, Ana Lima
├── Vendedores: Roberto (vendedor da Solar XYZ)
├── Produtos: 80 painéis, 15 inversores
└── Orçamentos: 30 orçamentos criados
```

**IMPORTANTE**: João Silva (cliente da Solar ABC) **NUNCA** aparece no banco da Solar XYZ!

---

## 🔐 Isolamento Total

### Por que Database-per-Tenant?

```
❌ COMPARTILHADO (Single Database):
┌─────────────────────────────┐
│      um_unico_banco_db      │
├─────────────────────────────┤
│ clientes                    │
│ ├── id=1, nome=João, tenant_id=1  │
│ ├── id=2, nome=Pedro, tenant_id=2 │
│ └── id=3, nome=Ana, tenant_id=2   │
└─────────────────────────────┘
Risco: Bug no código pode vazar dados!


✅ SEPARADO (Database-per-Tenant):
┌──────────────┐  ┌──────────────┐
│ solar_abc_db │  │ solar_xyz_db │
├──────────────┤  ├──────────────┤
│ clientes     │  │ clientes     │
│ ├── id=1, João│  │ ├── id=1, Pedro│
│              │  │ └── id=2, Ana  │
└──────────────┘  └──────────────┘
Seguro: Impossível vazar dados!
```

---

## 🗄️ Estrutura de Bancos

### Banco MASTER (Central)

```
┌─────────────────────────────────────────┐
│         master_db (PostgreSQL)          │
│  (Gerencia TODOS os tenants)            │
├─────────────────────────────────────────┤
│                                         │
│  Tabela: tenants                        │
│  ┌────┬──────────┬─────────────────┐   │
│  │ id │ slug     │ db_name         │   │
│  ├────┼──────────┼─────────────────┤   │
│  │ 1  │solar-abc │solar_abc_db     │   │
│  │ 2  │solar-xyz │solar_xyz_db     │   │
│  │ 3  │fotov-123 │fotov_123_db     │   │
│  └────┴──────────┴─────────────────┘   │
│                                         │
│  Tabela: subscriptions                  │
│  ┌────┬───────────┬────────┬────────┐  │
│  │ id │ tenant_id │ plano  │ status │  │
│  ├────┼───────────┼────────┼────────┤  │
│  │ 1  │ 1         │ basico │ ativo  │  │
│  │ 2  │ 2         │ basico │ ativo  │  │
│  │ 3  │ 3         │ basico │ trial  │  │
│  └────┴───────────┴────────┴────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

### Bancos dos Tenants

```
┌─────────────────────────────────────────┐
│      solar_abc_db (PostgreSQL)          │
│  (Dados da empresa Solar ABC)           │
├─────────────────────────────────────────┤
│                                         │
│  Tabela: clientes                       │
│  ┌────┬──────────────┬──────────────┐  │
│  │ id │ nome         │ cpf          │  │
│  ├────┼──────────────┼──────────────┤  │
│  │ 1  │ João Silva   │ 111.111.111  │  │
│  │ 2  │ Maria Santos │ 222.222.222  │  │
│  └────┴──────────────┴──────────────┘  │
│                                         │
│  Tabela: produtos                       │
│  ┌────┬─────────────┬────────┬───────┐ │
│  │ id │ nome        │ preco  │ tipo  │ │
│  ├────┼─────────────┼────────┼───────┤ │
│  │ 1  │ Painel 550W │ 850.00 │painel │ │
│  │ 2  │ Inversor 5k │3500.00 │inver. │ │
│  └────┴─────────────┴────────┴───────┘ │
│                                         │
│  Tabela: orcamentos                     │
│  ┌────┬────────────┬──────────┬───────┐│
│  │ id │ cliente_id │ valor    │ data  ││
│  ├────┼────────────┼──────────┼───────┤│
│  │ 1  │ 1          │ 25000.00 │01/01  ││
│  │ 2  │ 2          │ 30000.00 │05/01  ││
│  └────┴────────────┴──────────┴───────┘│
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│      solar_xyz_db (PostgreSQL)          │
│  (Dados da empresa Solar XYZ)           │
├─────────────────────────────────────────┤
│                                         │
│  Tabela: clientes                       │
│  ┌────┬──────────────┬──────────────┐  │
│  │ id │ nome         │ cpf          │  │
│  ├────┼──────────────┼──────────────┤  │
│  │ 1  │ Pedro Costa  │ 333.333.333  │  │
│  │ 2  │ Ana Lima     │ 444.444.444  │  │
│  └────┴──────────────┴──────────────┘  │
│                                         │
│  (mesmas tabelas, dados diferentes)     │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Request Completo

### Passo a Passo

```
1. Usuário acessa: solar-abc.seucrm.com/clientes

2. Request chega no servidor Django/FastAPI

3. Middleware extrai tenant do subdomínio:
   URL: solar-abc.seucrm.com
   Tenant slug: "solar-abc"

4. Consulta banco MASTER:
   SELECT * FROM tenants WHERE slug = 'solar-abc'
   
   Resultado:
   {
     id: 1,
     slug: "solar-abc",
     db_name: "solar_abc_db",
     db_host: "localhost",
     db_user: "tenant_user",
     db_password: "***"
   }

5. Conecta no banco do tenant:
   Connection String: postgresql://tenant_user:***@localhost/solar_abc_db

6. Executa query:
   SELECT * FROM clientes
   
   Resultado: João Silva, Maria Santos

7. Retorna resposta para o usuário
```

### Código Simplificado

```python
# middleware/tenant_resolver.py

def resolve_tenant(request):
    # 1. Extrai subdomínio
    host = request.get_host()  # solar-abc.seucrm.com
    slug = host.split('.')[0]  # solar-abc
    
    # 2. Busca tenant no banco MASTER
    tenant = MasterDB.query(
        "SELECT * FROM tenants WHERE slug = %s", 
        [slug]
    )
    
    if not tenant:
        raise TenantNotFound()
    
    # 3. Conecta no banco do tenant
    connection = connect_to_tenant_db(
        host=tenant['db_host'],
        database=tenant['db_name'],
        user=tenant['db_user'],
        password=tenant['db_password']
    )
    
    # 4. Armazena conexão no contexto da request
    request.tenant = tenant
    request.db_connection = connection
    
    return request


# views/clientes.py

def listar_clientes(request):
    # A conexão já está no contexto!
    # Automaticamente usa o banco correto
    clientes = request.db_connection.query(
        "SELECT * FROM clientes"
    )
    
    return JsonResponse(clientes)
```

---

## 📊 Exemplo com 3 Tenants

### Cenário Real

```
Você tem 3 empresas clientes:

┌─────────────────────────────────────────────────────────┐
│ TENANT 1: Solar ABC                                     │
├─────────────────────────────────────────────────────────┤
│ URL: solar-abc.seucrm.com                               │
│ Banco: solar_abc_db                                     │
│ Usuários: 2 (Carlos, Ana)                               │
│ Clientes cadastrados: 50                                │
│ Orçamentos: 120                                         │
│ Plano: R$ 300/mês                                       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ TENANT 2: Solar XYZ                                     │
├─────────────────────────────────────────────────────────┤
│ URL: solar-xyz.seucrm.com                               │
│ Banco: solar_xyz_db                                     │
│ Usuários: 2 (Roberto, Paula)                            │
│ Clientes cadastrados: 80                                │
│ Orçamentos: 200                                         │
│ Plano: R$ 300/mês                                       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ TENANT 3: Fotovoltaica 123                              │
├─────────────────────────────────────────────────────────┤
│ URL: fotov-123.seucrm.com                               │
│ Banco: fotov_123_db                                     │
│ Usuários: 2 (João, Maria)                               │
│ Clientes cadastrados: 30                                │
│ Orçamentos: 80                                          │
│ Plano: R$ 300/mês (trial 7 dias)                        │
└─────────────────────────────────────────────────────────┘

TOTAL: 3 tenants × R$ 300 = R$ 900/mês de receita
```

---

## 💾 Storage por Tenant

### Cálculo Real

```
Cada tenant tem seu próprio banco com:

┌─────────────────────────────────────────┐
│ Tabelas (schema igual para todos)      │
├─────────────────────────────────────────┤
│ clientes                                │
│ vendedores                              │
│ fornecedores                            │
│ marcas                                  │
│ produtos                                │
│ cotacoes                                │
│ orcamentos                              │
│ kits                                    │
│ itens_kit                               │
└─────────────────────────────────────────┘

Storage por tenant (ano 1):
├── Clientes: 50 × 2 KB = 100 KB
├── Produtos: 200 × 5 KB = 1 MB
├── Orçamentos: 360 × 10 KB = 3.6 MB
├── PDFs: 360 × 500 KB = 180 MB
├── Logs: 45 MB
└── Outros: 10 MB
─────────────────────────────────
TOTAL: ~240 MB por tenant
```

### Com 10 Tenants

```
10 bancos separados:
├── solar_abc_db: 240 MB
├── solar_xyz_db: 240 MB
├── fotov_123_db: 240 MB
├── ... (mais 7 tenants)
└── Total: 2.4 GB

Mais overhead (índices, etc): +30%
Total real: 3.1 GB

Mais backups (2x): 6.2 GB
```

---

## 🖥️ Infraestrutura Física

### Opção 1: Todos no Mesmo Servidor (MVP)

```
┌─────────────────────────────────────────────────────┐
│  AWS RDS PostgreSQL (db.t3.small)                   │
│  RAM: 2 GB | Storage: 50 GB                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐  ┌──────────────┐               │
│  │ master_db    │  │ solar_abc_db │               │
│  │ (100 MB)     │  │ (240 MB)     │               │
│  └──────────────┘  └──────────────┘               │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐               │
│  │ solar_xyz_db │  │ fotov_123_db │               │
│  │ (240 MB)     │  │ (240 MB)     │               │
│  └──────────────┘  └──────────────┘               │
│                                                     │
│  ... (mais 7 bancos de tenants)                    │
│                                                     │
│  Total usado: ~3 GB de 50 GB disponíveis           │
│                                                     │
└─────────────────────────────────────────────────────┘

Custo: $35/mês (1 servidor RDS)
```

### Opção 2: Servidores Separados (Escala)

```
┌──────────────────────┐  ┌──────────────────────┐
│ RDS Master           │  │ RDS Tenants 1-50     │
│ db.t3.micro          │  │ db.t3.medium         │
│ master_db            │  │ 50 bancos            │
│ $15/mês              │  │ $50/mês              │
└──────────────────────┘  └──────────────────────┘

                          ┌──────────────────────┐
                          │ RDS Tenants 51-100   │
                          │ db.t3.medium         │
                          │ 50 bancos            │
                          │ $50/mês              │
                          └──────────────────────┘

Custo: $115/mês (3 servidores RDS)
```

---

## 🔢 Recalculando Custos Corretos

### Premissa Correta

```
1 Tenant = 1 Empresa Cliente = 1 Banco de Dados

10 Tenants = 10 Empresas = 10 Bancos = R$ 3.000/mês receita
```

### Storage Real (10 Tenants)

```
Master DB:
└── 1 banco × 100 MB = 100 MB

Tenants DBs:
└── 10 bancos × 240 MB = 2.4 GB

Total: 2.5 GB
Com overhead (30%): 3.25 GB
Com backup (2x): 6.5 GB

Arredondando: 10 GB de storage necessário
```

### Compute Real (10 Tenants)

```
Usuários totais: 10 tenants × 2 usuários = 20 usuários
Usuários simultâneos: 20 × 60% = 12 usuários
Usuários no pico: 12 × 1.3 = 16 usuários

Requests/segundo: 0.52 req/s (pico)

CPU necessária: 1 core (t3.small)
RAM necessária: 2 GB
```

### Database Real (10 Tenants)

```
Conexões:
├── Pool por tenant: 5 conexões
├── Total: 10 × 5 = 50 conexões
└── Max connections: 50 × 1.5 = 75

IOPS: ~100 (baixo para 10 tenants)

Storage: 20 GB (com margem)

Instância: db.t3.small (2 GB RAM, 2 vCPU)
```

### Custo Correto (10 Tenants)

```
┌─────────────────────────────────────────┐
│ INFRAESTRUTURA AWS (10 Tenants)         │
├─────────────────────────────────────────┤
│                                         │
│ EC2 App (t3.small)         $15.18      │
│ EC2 RabbitMQ (t3.micro)    $7.59       │
│ RDS Master (db.t3.micro)   $16.61      │
│ RDS Tenants (db.t3.small)  $35.32      │
│ ElastiCache (t3.micro)     $12.41      │
│ S3 Storage                 $0.01       │
│ Data Transfer              $2.43       │
│ Route53 + Monitoring       $18.40      │
│                                         │
├─────────────────────────────────────────┤
│ TOTAL                      $107.95     │
│ Margem 20%                 $21.59      │
├─────────────────────────────────────────┤
│ TOTAL FINAL                $129.54     │
└─────────────────────────────────────────┘

Conversão (1 USD = R$ 5.00):
Custo: R$ 647.70/mês

Receita: 10 × R$ 300 = R$ 3.000/mês
Lucro: R$ 3.000 - R$ 647.70 = R$ 2.352,30/mês
Margem: 78.4%
```

---

## 📈 Projeção Correta de Crescimento

| Tenants | Empresas | Receita/Mês | Custo AWS | Lucro | Margem |
|---------|----------|-------------|-----------|-------|--------|
| 1       | 1        | R$ 300      | R$ 200    | R$ 100| 33%    |
| 5       | 5        | R$ 1.500    | R$ 400    | R$ 1.100| 73%  |
| 10      | 10       | R$ 3.000    | R$ 650    | R$ 2.350| 78%  |
| 20      | 20       | R$ 6.000    | R$ 900    | R$ 5.100| 85%  |
| 50      | 50       | R$ 15.000   | R$ 2.000  | R$ 13.000| 87% |
| 100     | 100      | R$ 30.000   | R$ 4.000  | R$ 26.000| 87% |

---

## 🎯 Vantagens vs Desvantagens

### ✅ Vantagens Database-per-Tenant

1. **Segurança Máxima**
   - Impossível vazar dados entre empresas
   - Bug no código não afeta outros tenants

2. **Performance Isolada**
   - Tenant grande não afeta tenant pequeno
   - Queries não competem

3. **Backup/Restore Individual**
   - Restaurar só uma empresa
   - Não afeta outras

4. **Customização**
   - Pode ter schema diferente por tenant
   - Migrações independentes

5. **Compliance**
   - LGPD facilitada
   - Dados geograficamente separados

### ❌ Desvantagens

1. **Complexidade**
   - Precisa gerenciar múltiplas conexões
   - Migrations em todos os bancos

2. **Custo Inicial Maior**
   - Overhead por banco
   - Mais storage

3. **Relatórios Cross-Tenant**
   - Difícil agregar dados de todos
   - Precisa de banco de analytics separado

---

## 🔧 Provisionamento de Novo Tenant

### Fluxo Completo

```
1. Empresa se cadastra no site
   └── Preenche: Nome, Email, Subdomínio desejado

2. Sistema valida
   ├── Subdomínio disponível?
   ├── Email único?
   └── Dados válidos?

3. Cria registro no banco MASTER
   INSERT INTO tenants (slug, nome, db_name, status)
   VALUES ('solar-abc', 'Solar ABC', 'solar_abc_db', 'provisioning')

4. Cria novo banco PostgreSQL
   CREATE DATABASE solar_abc_db;

5. Roda migrations no novo banco
   ├── CREATE TABLE clientes...
   ├── CREATE TABLE produtos...
   └── ... (todas as tabelas)

6. Insere dados iniciais (seed)
   ├── Usuário admin
   ├── Produtos padrão (opcional)
   └── Configurações

7. Atualiza status no MASTER
   UPDATE tenants SET status = 'active' WHERE slug = 'solar-abc'

8. Configura DNS (subdomínio)
   solar-abc.seucrm.com → seu servidor

9. Envia email de boas-vindas
   "Seu CRM está pronto! Acesse: solar-abc.seucrm.com"

Tempo total: 30-60 segundos (automatizado)
```

---

## 🧪 Testando Isolamento

### Teste Prático

```python
# Conecta no tenant 1
connection1 = connect('solar_abc_db')
connection1.execute("INSERT INTO clientes (nome) VALUES ('João')")

# Conecta no tenant 2
connection2 = connect('solar_xyz_db')
result = connection2.execute("SELECT * FROM clientes")

# Resultado: VAZIO (João não aparece!)
# Porque está em outro banco!
```

---

## 📚 Resumo Final

### O que você precisa entender:

1. **1 Tenant = 1 Empresa Cliente = 1 Banco de Dados**

2. **10 Tenants = 10 Empresas pagando R$ 300/mês cada**

3. **Cada banco tem as mesmas tabelas, mas dados diferentes**

4. **Sistema identifica tenant pelo subdomínio**

5. **Middleware conecta no banco correto automaticamente**

6. **Dados 100% isolados entre tenants**

7. **Custo AWS: ~R$ 650/mês para 10 tenants**

8. **Receita: R$ 3.000/mês (10 × R$ 300)**

9. **Lucro: R$ 2.350/mês (78% de margem)**

10. **Escala bem: quanto mais tenants, maior a margem**

---

Agora ficou claro? Quer que eu explique alguma parte específica com mais detalhes?
