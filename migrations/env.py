from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ----------------------------------------------------------------------
# AS ALTERAÇÕES COMEÇAM AQUI
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
# target_metadata = mymodel.Base.metadata # Linha Original
# 3. Defina o target_metadata como o metadata do Flask-SQLAlchemy
target_metadata = db.metadata

# ----------------------------------------------------------------------
# O RESTANTE DO CÓDIGO PERMANECE INALTERADO
# ----------------------------------------------------------------------

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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