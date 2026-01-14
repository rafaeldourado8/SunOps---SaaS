# 🚀 Plano de Entrega Rápida - Fase 1 MVP

## 🎯 Objetivo

Entregar sistema funcionando em **2 semanas** com:
- ✅ CRUD Clientes, Vendedores, Fornecedores
- ✅ CRUD Produtos (Painéis, Inversores, etc)
- ✅ Sistema de Cotação com validade
- ✅ Montador de Kits
- ✅ Cálculos (Geração, Payback)
- ✅ Geração de PDF
- ✅ Multi-tenant funcionando
- ✅ Autenticação

## 📦 Stack Simplificada (MVP Rápido)

```
Django Admin (tudo em um)
├── Models (ORM)
├── Admin Interface (CRUD pronto)
├── Views (APIs simples)
└── Templates (se precisar)

PostgreSQL (multi-tenant)
Redis (cache)
Celery (tarefas assíncronas)
```

**Decisão**: Usar só Django no MVP (FastAPI depois)
- Django Admin = CRUD grátis
- Menos código para escrever
- Entrega mais rápida

## 📁 Estrutura Simplificada

```
backend/
├── manage.py
├── config/                 # Settings Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/
│   ├── tenants/           # Multi-tenancy
│   ├── cadastros/         # Clientes, Vendedores, Fornecedores
│   ├── catalogo/          # Produtos, Marcas, Cotações
│   └── orcamentos/        # Kits, Orçamentos, PDFs
│
└── requirements.txt
```

## 🗓️ Cronograma de Entrega

### Semana 1: Base + Cadastros

**Dia 1**: Setup Django + Multi-tenant
- Criar projeto Django
- Configurar multi-tenant (django-tenants)
- Migrations do banco master

**Dia 2**: App Cadastros
- Models: Cliente, Vendedor, Fornecedor
- Django Admin configurado
- CRUD funcionando

**Dia 3**: App Catálogo (Parte 1)
- Models: Marca, Produto (abstrato)
- Models: Painel, Inversor, Estrutura
- Django Admin

**Dia 4**: App Catálogo (Parte 2)
- Model: Cotacao (com validade)
- Celery Task: Alerta segunda-feira
- Admin com filtros

**Dia 5**: Testes + Ajustes
- Testar CRUD completo
- Ajustar validações
- Documentar

### Semana 2: Orçamentos + Cálculos

**Dia 1**: App Orçamentos (Parte 1)
- Models: Kit, ItemKit, Orcamento
- Relacionamentos

**Dia 2**: App Orçamentos (Parte 2)
- Cálculos: Potência, Geração, Payback
- Methods nos models

**Dia 3**: Geração de PDF
- WeasyPrint ou ReportLab
- Template HTML do orçamento
- Celery Task para gerar PDF

**Dia 4**: Interface Admin Avançada
- Inline editing (Kit dentro de Orçamento)
- Actions customizadas
- Filtros e buscas

**Dia 5**: Deploy + Testes Finais
- Docker Compose completo
- Subir em EC2 (opcional)
- Testes end-to-end

## 📦 Dependências (requirements.txt)

```txt
# Django
Django==4.2
django-environ==0.11.2

# Multi-tenant
django-tenants==3.5.0

# Database
psycopg2-binary==2.9.9

# Cache
redis==5.0.1
django-redis==5.4.0

# Tasks
celery==5.3.4

# PDF
weasyprint==60.1

# API (futuro)
djangorestframework==3.14.0

# Dev
pytest==7.4.3
pytest-django==4.7.0
```

## 🎯 Entregas por Funcionalidade

### F1.01-F1.03: CRUD Cadastros ✅
```python
# apps/cadastros/models.py
class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf_cnpj = models.CharField(max_length=18)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    # ... campos completos

class Vendedor(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    # ...

class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    # ...
```

### F1.04-F1.05: CRUD Produtos ✅
```python
# apps/catalogo/models.py
class Marca(models.Model):
    nome = models.CharField(max_length=100)

class Produto(models.Model):
    # Classe abstrata
    nome = models.CharField(max_length=255)
    marca = models.ForeignKey(Marca)
    preco = models.DecimalField()
    
    class Meta:
        abstract = True

class Painel(Produto):
    potencia = models.IntegerField()  # Watts
    tipo = models.CharField()  # Monocristalino, Policristalino

class Inversor(Produto):
    potencia = models.IntegerField()  # kW
    tipo = models.CharField()  # String, Microinversor
```

### F1.06-F1.07: Cotação + Alerta ✅
```python
# apps/catalogo/models.py
class Cotacao(models.Model):
    produto = models.ForeignKey(Produto)
    preco = models.DecimalField()
    data_cotacao = models.DateField(auto_now_add=True)
    validade = models.DateField()  # +3 dias úteis
    
    def save(self, *args, **kwargs):
        if not self.validade:
            self.validade = self.calcular_validade()
        super().save(*args, **kwargs)
    
    def calcular_validade(self):
        # +3 dias úteis
        pass

# apps/catalogo/tasks.py
@celery.task
def alerta_cotacao_segunda():
    # Envia email se cotação expirada
    pass
```

### F1.08-F1.09: Monte Seu Kit ✅
```python
# apps/orcamentos/models.py
class Kit(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    is_template = models.BooleanField(default=False)

class ItemKit(models.Model):
    kit = models.ForeignKey(Kit)
    produto = models.ForeignKey(Produto)
    quantidade = models.IntegerField()
```

### F1.10-F1.11: Cálculos ✅
```python
# apps/orcamentos/models.py
class Kit(models.Model):
    # ...
    
    def calcular_potencia(self):
        """Retorna potência total em kWp"""
        paineis = self.itemkit_set.filter(
            produto__tipo='painel'
        )
        total = sum(
            item.produto.potencia * item.quantidade 
            for item in paineis
        )
        return total / 1000  # Converter W para kW
    
    def calcular_geracao(self, hsp=5.0):
        """Retorna geração mensal em kWh"""
        potencia = self.calcular_potencia()
        return potencia * hsp * 30 * 0.8
    
    def calcular_payback(self, investimento, economia_mensal):
        """Retorna payback em meses"""
        return investimento / economia_mensal
```

### F1.12-F1.13: Orçamento + PDF ✅
```python
# apps/orcamentos/models.py
class Orcamento(models.Model):
    cliente = models.ForeignKey(Cliente)
    vendedor = models.ForeignKey(Vendedor)
    kit = models.ForeignKey(Kit)
    valor_total = models.DecimalField()
    pdf = models.FileField(upload_to='orcamentos/')
    
    def gerar_pdf(self):
        # WeasyPrint
        html = render_to_string('orcamento.html', {
            'orcamento': self
        })
        pdf = HTML(string=html).write_pdf()
        self.pdf.save(f'orcamento_{self.id}.pdf', ContentFile(pdf))
```

## 🔧 Comandos de Setup

```bash
# 1. Criar estrutura
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Criar projeto Django
django-admin startproject config .
python manage.py startapp tenants
python manage.py startapp cadastros
python manage.py startapp catalogo
python manage.py startapp orcamentos

# 3. Configurar multi-tenant
# Editar settings.py

# 4. Migrations
python manage.py makemigrations
python manage.py migrate

# 5. Criar superuser
python manage.py createsuperuser

# 6. Rodar
python manage.py runserver
```

## ✅ Critérios de Aceite (Checklist)

- [ ] Cadastrar cliente com todos os dados
- [ ] Cadastrar produto com preço e fornecedor
- [ ] Sistema calcula validade de 3 dias úteis
- [ ] Alerta de cotação segunda-feira
- [ ] Montar kit com mínimo 2 categorias
- [ ] Calcular potência (kWp) e geração (kWh)
- [ ] Calcular payback
- [ ] Gerar PDF do orçamento
- [ ] Multi-tenant funcionando (2 empresas)
- [ ] Deploy em Docker

## 🚀 Próximos Passos

Vou criar todos os arquivos necessários na ordem:
1. Setup Django + Multi-tenant
2. Models de todos os apps
3. Admin configurado
4. Celery tasks
5. Geração de PDF
6. Docker completo

**Confirma que quer que eu crie tudo agora?**
