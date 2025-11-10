from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ----------------------------------------------------------------------
# INÍCIO DAS ALTERAÇÕES
# ----------------------------------------------------------------------

# 1. Ajuste no PATH: Garante que as importações abaixo funcionem
import os
import sys
# O diretório raiz do projeto (onde está o alembic.ini e migrations/)
sys.path.insert(0, os.path.realpath('.')) 

# 2. Importe a instância do SQLAlchemy e todos os seus Modelos:
# Assumindo que:
# - A instância db está em src.config.data_base
# - Seus modelos estão em src.Infrastructure.Model
from src.config.data_base import db
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Model.user import User 
# Importe todos os seus modelos aqui, se houver mais!

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# 3. Defina o target_metadata como o metadata do Flask-SQLAlchemy
target_metadata = db.metadata

# ----------------------------------------------------------------------
# FIM DA SEÇÃO DE METADATA
# ----------------------------------------------------------------------

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    
    🟢 CORREÇÃO: Lê a DATABASE_URL do ambiente (Render) antes de ler o alembic.ini.
    """
    
    # Tenta usar a variável de ambiente DATABASE_URL (usada em produção/Render)
    connectable = os.environ.get("DATABASE_URL")

    if connectable is None:
        # Se DATABASE_URL não estiver definida (ambiente local),
        # Volta a usar a configuração do alembic.ini
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    # Nota: Se 'connectable' for uma string de URL (do os.environ), a conexão é feita aqui.
    # Se for um objeto Engine (do engine_from_config), a conexão também funciona.
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