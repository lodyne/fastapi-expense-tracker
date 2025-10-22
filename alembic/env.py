# from logging.config import fileConfig
# import os

# from sqlalchemy import engine_from_config
# from sqlalchemy import pool

# from alembic import context

# from dotenv import load_dotenv
# from src.app.database.postgres import Base, POSTGRES_URL
# from src.app.models import postgres as postgres_models  # noqa: F401

# # this is the Alembic Config object, which provides
# # access to the values within the .ini file in use.
# config = context.config

# # Interpret the config file for Python logging.
# # This line sets up loggers basically.
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# # Ensure environment variables from .env are available when Alembic runs.
# load_dotenv()

# # add your model's MetaData object here
# # for 'autogenerate' support
# target_metadata = Base.metadata

# # other values from the config, defined by the needs of env.py,
# # can be acquired:
# # my_important_option = config.get_main_option("my_important_option")
# # ... etc.


# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode.

#     This configures the context with just a URL
#     and not an Engine, though an Engine is acceptable
#     here as well.  By skipping the Engine creation
#     we don't even need a DBAPI to be available.

#     Calls to context.execute() here emit the given string to the
#     script output.

#     """
#     config.set_main_option("sqlalchemy.url", POSTGRES_URL)
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )

#     with context.begin_transaction():
#         context.run_migrations()


# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode.

#     In this scenario we need to create an Engine
#     and associate a connection with the context.

#     """
#     config.set_main_option("sqlalchemy.url", POSTGRES_URL)

#     connectable = engine_from_config(
#         config.get_section(config.config_ini_section, {}),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection, target_metadata=target_metadata
#         )

#         with context.begin_transaction():
#             context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()


# alembic/env.py
from logging.config import fileConfig
import os
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

from alembic import context
from sqlalchemy import engine_from_config, pool

from dotenv import load_dotenv

# Import models so Alembic sees them
from src.app.models import expense as postgres_models  # noqa: F401
from src.app.database.expense import Base  # only Base, not POSTGRES_URL

# ----- Setup logging -----
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ----- Load .env for local dev -----
load_dotenv()

target_metadata = Base.metadata


def _ensure_sslmode(url: str) -> str:
    """Append sslmode=require if missing."""
    if not url or "postgresql" not in url:
        return url
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query))
    if "sslmode" not in query:
        query["sslmode"] = "require"
        parts = parts._replace(query=urlencode(query))
        return urlunsplit(parts)
    return url


def _build_url_from_components() -> str:
    """Fallback if DATABASE_URL is not provided: use POSTGRES_* env vars."""
    required = ["POSTGRES_USER", "POSTGRES_HOST", "POSTGRES_DB"]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise RuntimeError(
            "DATABASE_URL not set and missing components: " + ", ".join(missing)
        )
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD", "")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def _get_database_url() -> str:
    # Prefer DATABASE_URL (Render). Fallback to components for local dev.
    db_url = os.getenv("DATABASE_URL") or _build_url_from_components()

    # Enforce SSL on Render or when FORCE_DB_SSL=1 (default)
    if os.getenv("RENDER") == "true" or os.getenv("FORCE_DB_SSL", "1") == "1":
        db_url = _ensure_sslmode(db_url)

    return db_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    db_url = _get_database_url()
    config.set_main_option("sqlalchemy.url", db_url)

    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    db_url = _get_database_url()
    config.set_main_option("sqlalchemy.url", db_url)

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