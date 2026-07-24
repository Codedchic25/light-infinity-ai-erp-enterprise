import os
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context

# Adaugam comentariul # noqa: F401 pentru a curata panoul de avertismente din VS Code
from app.db.connection import Base
from app.modules.catalog.model import Lumanare  # noqa: F401
from app.modules.products.model import Ceara, Parfum, Culoare, Forma  # noqa: F401
from app.modules.erp_production.model import Reteta, Material, StockAuditLog  # noqa: F401
from app.modules.orders.model import Comanda, ComandaLumanare  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url():
    return os.getenv("PROD_DATABASE_URL") or os.getenv("DATABASE_URL")


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = get_url()
    if url and url.startswith("postgresql+asyncpg"):
        url = url.replace("postgresql+asyncpg", "postgresql")

    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

