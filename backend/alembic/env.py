from logging.config import fileConfig

# Imports Adicionados
import os
import sys
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- Imports da Aplicação ---
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from app import config as app_config  # Importa sua configuração (config.py)
from app.db import Base               # Importa seu Base metadata (db.py)

# --- IMPORTAR TODOS OS SEUS MODELOS AQUI ---
from app.core.users.models import User
from app.core.clientes.models import Cliente
from app.core.sales.propostas.models import Proposta
from app.core.sales.projetos.models import Projeto
from app.core.financeiro.models import ConfiguracaoFinanceira, Transacao
# --- Fim dos Imports de Modelos ---


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Alteração 1: Definir o target_metadata ---
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    
    # --- Alteração 2: Construir a URL offline ---
    DB_URL = f"postgresql+psycopg2://{app_config.DATABASE_USERNAME}:{app_config.DATABASE_PASSWORD}@{app_config.DATABASE_HOST}/{app_config.DATABASE_NAME}"
    
    context.configure(
        url=DB_URL, # Usar a URL construída
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    
    # --- Alteração 3: Construir a URL online e o config ---
    DB_URL = f"postgresql+psycopg2://{app_config.DATABASE_USERNAME}:{app_config.DATABASE_PASSWORD}@{app_config.DATABASE_HOST}/{app_config.DATABASE_NAME}"

    db_config = config.get_section(config.config_ini_section, {})
    db_config["sqlalchemy.url"] = DB_URL

    connectable = engine_from_config(
        db_config, # Passa o dicionário modificado
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()