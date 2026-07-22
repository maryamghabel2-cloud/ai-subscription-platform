from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Ensure app module is importable
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import Base
from app.config import settings
# Import all models to register metadata
from app.models.user import User
from app.models.wallet import Wallet
from app.models.ledger import LedgerTransaction
from app.models.persona import Persona
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.api_key import ApiKey
from app.models.auth_session import AuthSession
from app.models.password_reset_token import PasswordResetToken

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override sqlalchemy.url from settings if present
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
