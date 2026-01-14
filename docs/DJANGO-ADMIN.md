# Django Admin - Gerenciamento Centralizado

## 🎯 Estrutura

### 1. Admin Padrão (http://localhost:8000/admin)
Gerenciamento de dados do tenant atual.

**Models Registrados:**
- ✅ **Clientes** - CRUD completo com filtros
- ✅ **Vendedores** - CRUD completo com comissão
- ✅ Users (Django padrão)
- ✅ Groups (Django padrão)

**Acesso:**
- Qualquer usuário autenticado (staff)
- Vê apenas dados do seu tenant

---

### 2. SuperAdmin (http://localhost:8000/superadmin)
Gerenciamento multi-tenant (apenas superusers).

**Models Registrados:**
- ✅ **Tenants** - Gerenciar empresas/clientes
  - Criar novo tenant
  - Configurar database
  - Ativar/desativar

**Acesso:**
- Apenas superusers
- Vê todos os tenants

---

## 📋 Funcionalidades por Model

### Clientes (Admin Padrão)
```
List Display: nome, documento, email, telefone, ativo, created_at
Filtros: ativo, created_at
Busca: nome, documento, email
Readonly: id, created_at, updated_at
```

**Fieldsets:**
- Informações Básicas (nome, documento, email, telefone)
- Endereço (endereco)
- Status (ativo)
- Metadados (id, created_at, updated_at) - colapsado

---

### Vendedores (Admin Padrão)
```
List Display: nome, email, telefone, comissao_percentual, ativo, created_at
Filtros: ativo, created_at
Busca: nome, email, telefone
Readonly: id, created_at, updated_at
```

**Fieldsets:**
- Informações Básicas (nome, email, telefone)
- Comissão (comissao_percentual)
- Status (ativo)
- Metadados (id, created_at, updated_at) - colapsado

---

### Tenants (SuperAdmin)
```
List Display: slug, nome, db_name, db_host, ativo, created_at
Filtros: ativo, created_at
Busca: slug, nome, db_name
Readonly: created_at
```

**Fieldsets:**
- Informações do Tenant (slug, nome, ativo)
- Configuração Database (db_name, db_host, db_port)
- Metadados (created_at) - colapsado

**Permissões:**
- Add: Apenas superuser
- Change: Apenas superuser
- Delete: Apenas superuser

---

## 🚀 Como Usar

### 1. Criar Superuser
```bash
docker-compose exec django python manage.py createsuperuser
# Username: admin
# Email: admin@ops-crm.com
# Password: admin123
```

### 2. Acessar Admin Padrão
```
URL: http://localhost:8000/admin
Login: admin / admin123
```

**Ações disponíveis:**
- Criar/editar/deletar Clientes
- Criar/editar/deletar Vendedores
- Gerenciar usuários e grupos

### 3. Acessar SuperAdmin
```
URL: http://localhost:8000/superadmin
Login: admin / admin123 (apenas superuser)
```

**Ações disponíveis:**
- Criar novo tenant
- Configurar database do tenant
- Ativar/desativar tenant

---

## 📝 Criar Novo Tenant via SuperAdmin

1. Acesse http://localhost:8000/superadmin
2. Clique em "Tenants" → "Add Tenant"
3. Preencha:
   - **Slug**: `solar-xyz` (identificador único)
   - **Nome**: `Solar XYZ Ltda`
   - **DB Name**: `tenant_solar_xyz_db`
   - **DB Host**: `postgres` (padrão)
   - **DB Port**: `5432` (padrão)
   - **Ativo**: ✅
4. Salvar

5. Criar database no PostgreSQL:
```bash
docker-compose exec postgres createdb -U postgres tenant_solar_xyz_db
```

6. Aplicar migrations no novo tenant:
```bash
# Conectar ao database
docker-compose exec postgres psql -U postgres -d tenant_solar_xyz_db

# Copiar schema do master_db ou rodar migrations
```

---

## 🔐 Controle de Acesso

### Admin Padrão
- **Staff users**: Acesso ao admin do seu tenant
- **Superusers**: Acesso total

### SuperAdmin
- **Apenas Superusers**: Acesso exclusivo
- Gerencia todos os tenants
- Cria novos tenants

---

## 🎨 Customizações

### Adicionar novo model ao Admin

1. Criar model em `contexts/*/infrastructure/django_models/`
2. Registrar no `admin.py`:

```python
from django.contrib import admin
from .models import MeuModel

@admin.register(MeuModel)
class MeuModelAdmin(admin.ModelAdmin):
    list_display = ('campo1', 'campo2', 'created_at')
    list_filter = ('ativo', 'created_at')
    search_fields = ('campo1', 'campo2')
```

### Adicionar ao SuperAdmin

```python
from config.admin import superadmin_site

@admin.register(MeuModel, site=superadmin_site)
class MeuModelSuperAdmin(admin.ModelAdmin):
    # configuração
    pass
```

---

## 📊 Próximos Models (Sprint 2)

Serão adicionados ao Admin:
- ✅ Fornecedor
- ✅ Marca
- ✅ Produto (Painel, Inversor, Estrutura, Cabo, Conector)
- ✅ Cotação

---

## ✅ Status Atual

| Model | Admin Padrão | SuperAdmin | Status |
|-------|--------------|------------|--------|
| Cliente | ✅ | ❌ | Completo |
| Vendedor | ✅ | ❌ | Completo |
| Tenant | ❌ | ✅ | Completo |
| User | ✅ | ❌ | Django padrão |
| Group | ✅ | ❌ | Django padrão |

---

## 🔗 Links Rápidos

- **Admin Padrão**: http://localhost:8000/admin
- **SuperAdmin**: http://localhost:8000/superadmin
- **API Docs**: http://localhost:8001/docs
