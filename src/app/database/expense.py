# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# import os

# load_dotenv()


# def validate_postgres_config():
#     required_vars = [
#         "POSTGRES_USER",
#         "POSTGRES_PASSWORD",
#         "POSTGRES_HOST",
#         "POSTGRES_PORT",
#         "POSTGRES_DB",
#     ]
#     missing_vars = []

#     for var in required_vars:
#         if os.getenv(var) is None:
#             missing_vars.append(var)

#     if missing_vars:
#         raise ValueError(
#             f"Missing required environment variables: {', '.join(missing_vars)}"
#         )


# validate_postgres_config()

# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT")
# POSTGRES_DB = os.getenv("POSTGRES_DB")

# POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# engine = create_engine(POSTGRES_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import os

load_dotenv()

def _ensure_sslmode(url: str) -> str:
    """
    Append sslmode=require to the Postgres URL if it's missing.
    Works with URLs that may already have query params.
    """
    if not url:
        return url
    if "postgresql" not in url:
        return url  # not a postgres URL
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query))
    if "sslmode" not in query:
        query["sslmode"] = "require"
        parts = parts._replace(query=urlencode(query))
        return urlunsplit(parts)
    return url

def _build_url_from_components() -> str:
    required_vars = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB"]
    missing = [v for v in required_vars if os.getenv(v) is None]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD", "")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT", "5432")
    db   = os.getenv("POSTGRES_DB")

    return f"postgresql://{user}:{password}@{host}:{port}/{db}"

def _should_force_ssl() -> bool:
    """
    Render requires SSL; allow local overrides via FORCE_DB_SSL env.
    """
    if os.getenv("RENDER") == "true":
        return True
    override = os.getenv("FORCE_DB_SSL")
    if override is not None:
        return override == "1"
    return False

# 1) Prefer DATABASE_URL (Render). Fallback to individual vars (local dev).
DATABASE_URL = os.getenv("DATABASE_URL") or _build_url_from_components()

# 2) On Render (or generally in prod), ensure SSL unless explicitly set.
# Render sets RENDER="true" in env; also allow explicit override.
if _should_force_ssl():
    DATABASE_URL = _ensure_sslmode(DATABASE_URL)

# Optional: simple guard to avoid using localhost on Render
if os.getenv("RENDER") == "true" and ("@localhost:" in DATABASE_URL or "@127.0.0.1:" in DATABASE_URL):
    raise RuntimeError(
        "DATABASE_URL points to localhost on Render. Use the Postgres service URL from the Render dashboard."
    )

# 3) Create engine + session factory
SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "0") == "1"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=SQLALCHEMY_ECHO,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
