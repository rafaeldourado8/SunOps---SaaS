# 🎓 Sprint 1: Fundação (Semanas 1-2)

## 🎯 Objetivo da Sprint

Criar a base do sistema:
- ✅ Infraestrutura multi-tenant funcionando
- ✅ Autenticação (login/logout)
- ✅ CRUD de Clientes
- ✅ CRUD de Vendedores

---

## 📅 Cronograma Detalhado

### Semana 1: Infraestrutura + Shared Kernel

```
Dia 1-2: Setup Docker + Banco Master
Dia 3-4: Value Objects (CPF, Email, Money)
Dia 5:   Tenant Resolution (identificar empresa)
```

### Semana 2: Autenticação + Cadastros

```
Dia 1-2: Sistema de Auth (JWT)
Dia 3-4: Entity Cliente + Repository
Dia 5:   API REST para Clientes
```

---

## 📚 DIA 1-2: Setup Docker + Banco Master

### 🎓 O que você vai aprender:

1. Como funciona Docker Compose
2. Como criar banco PostgreSQL
3. Como conectar aplicação ao banco
4. Multi-tenancy na prática

### 📝 Exercício 1: Entender o docker-compose.yml

**Abra o arquivo**: `docker-compose.yml`

**Sua missão**: Responda estas perguntas (sem olhar a resposta!)

```yaml
services:
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
```

**Perguntas**:
1. O que significa `image: postgres:15-alpine`?
2. O que significa `ports: "5432:5432"`?
3. Por que precisamos de `volumes`?

<details>
<summary>📖 Ver Respostas</summary>

1. **image**: Baixa imagem pronta do PostgreSQL versão 15 (alpine = versão leve)
2. **ports**: Mapeia porta 5432 do container para porta 5432 do host (sua máquina)
3. **volumes**: Persiste dados mesmo se container for deletado

</details>

---

### 📝 Exercício 2: Subir a Infraestrutura

**Passo 1**: Abra o terminal na pasta do projeto

```bash
cd "d:\OPS - CRM"
```

**Passo 2**: Copie o arquivo de ambiente

```bash
copy .env.example .env
```

**Passo 3**: Suba APENAS o PostgreSQL primeiro

```bash
docker-compose up postgres -d
```

**Passo 4**: Verifique se está rodando

```bash
docker-compose ps
```

**Passo 5**: Veja os logs

```bash
docker-compose logs postgres
```

---

### 📝 Exercício 3: Conectar no Banco

**Conecte no banco**:

```bash
docker exec -it ops-crm-postgres psql -U postgres -d master_db
```

**Execute comandos SQL**:

```sql
-- Ver tabelas
\dt

-- Ver tabela tenants
SELECT * FROM tenants;

-- Sair
\q
```

**Perguntas**:
1. Quantos tenants existem?
2. Quais são os nomes (slug)?

---

### 📝 Exercício 4: Criar Banco dos Tenants

**Conecte no PostgreSQL**:

```bash
docker exec -it ops-crm-postgres psql -U postgres
```

**Execute**:

```sql
CREATE DATABASE tenant_solar_abc_db;
CREATE DATABASE tenant_solar_xyz_db;
\l
\q
```

---

## 📚 DIA 3-4: Value Objects

### 📝 Exercício 5: Criar Value Object CPF

**Crie o arquivo**: `backend/shared/domain/value_objects/cpf.py`

**Template para você completar**:

```python
class CPF:
    def __init__(self, valor: str):
        # TODO: Remover caracteres não numéricos
        # TODO: Validar se tem 11 dígitos
        # TODO: Validar dígitos verificadores
        self._valor = limpo
    
    @property
    def valor(self) -> str:
        return self._valor
    
    @property
    def formatado(self) -> str:
        # TODO: Formatar CPF (123.456.789-00)
        pass
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, CPF):
            return False
        return self._valor == other._valor
```

---

## ✅ Checklist do Dia 1-4

- [ ] Subiu PostgreSQL com Docker
- [ ] Conectou no banco
- [ ] Criou bancos dos tenants
- [ ] Implementou Value Object CPF
- [ ] Implementou Value Object Email
- [ ] Implementou Value Object Money

---

**Comece pelos exercícios e me avise quando terminar!** 🚀
