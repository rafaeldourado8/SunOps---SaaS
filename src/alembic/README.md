# Migrações do Banco de Dados

## 🚀 Comandos Principais

### Executar migrações
```bash
# Local
python migrate.py
# ou
alembic upgrade head

# Docker
docker-compose exec api python migrate.py
docker-compose exec api alembic upgrade head
```

### Criar nova migração
```bash
# Auto-detectar mudanças nos models
alembic revision --autogenerate -m "descrição da mudança"

# Migração manual
alembic revision -m "descrição da mudança"
```

### Reverter migração
```bash
# Voltar 1 migração
alembic downgrade -1

# Voltar para versão específica
alembic downgrade 001

# Voltar tudo
alembic downgrade base
```

### Ver histórico
```bash
alembic history
alembic current
```

## 📋 Estrutura

```
src/
├── alembic/
│   ├── versions/          # Migrações
│   │   └── 001_initial_migration.py
│   ├── env.py            # Configuração
│   └── script.py.mako    # Template
├── alembic.ini           # Config Alembic
└── migrate.py            # Script helper
```

## 🔧 Configuração

O Alembic está configurado para:
- Ler DATABASE_URL do .env
- Auto-importar todos os models
- Criar índices automaticamente
- Suportar rollback completo

## 📦 Tabelas Criadas

- `usuarios` - Usuários do sistema
- `clientes` - Clientes/Prospects
- `propostas` - Propostas comerciais
- `itens_proposta` - Itens das propostas
- `contratos` - Contratos gerados
- `premissas_preco` - Premissas de preço
- `configuracoes` - Configurações globais

## ⚠️ Importante

- Sempre revisar migrações auto-geradas
- Testar rollback antes de aplicar em produção
- Fazer backup antes de migrações grandes
