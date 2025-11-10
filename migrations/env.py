from logging.config import fileConfig

# 🟢 Adicionado: create_engine para transformar a string de URL em um objeto Engine
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import create_engine # NOVO

from alembic import context

# ----------------------------------------------------------------------
# SEÇÃO DE IMPORTAÇÃO E METADADOS
# ----------------------------------------------------------------------

# Ajuste no PATH: Garante que as importações abaixo funcionem
import os
import sys
# O diretório raiz do projeto (onde está o alembic.ini e migrations/)
sys.path.insert(0, os.path.realpath('.')) 

# Importe a instância do SQLAlchemy e todos os seus Modelos:
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

# Defina o target_metadata como o metadata do Flask-SQLAlchemy
target_metadata = db.metadata

# ----------------------------------------------------------------------
# FUNÇÕES DE MIGRAÇÃO
# ----------------------------------------------------------------------

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
    
    🟢 CORREÇÃO: Lê a DATABASE_URL do ambiente (Render) e cria o Engine.
    """
    
    # 1. Tenta usar a variável de ambiente DATABASE_URL (Produção/Render)
    connectable = os.environ.get("DATABASE_URL")

    if connectable is None:
        # 2. Se DATABASE_URL não estiver definida (Desenvolvimento Local),
        #    usa a configuração do alembic.ini (e connectable é um objeto Engine)
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    else:
        # 3. SE ESTIVER NO RENDER (connectable é uma string de URL), cria o Engine:
        #    Isso resolve o erro 'AttributeError: 'str' object has no attribute 'connect''
        connectable = create_engine(connectable)

    # 4. Agora, 'connectable' é garantidamente um objeto Engine e pode usar .connect()
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