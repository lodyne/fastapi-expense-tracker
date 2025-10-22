# Expense Tracker API

A FastAPI-based backend for tracking expenses and managing budgets, using PostgreSQL for data storage (SQLAlchemy + Alembic migrations).

## Features

- Create, retrieve, and manage expenses
- PostgreSQL backend using SQLAlchemy (async or sync) with Alembic for migrations
- Pydantic models for validation
- OpenAPI docs (`/docs`) and ReDoc (`/redoc`)
- Environment-based configuration

## Project Structure

```text
fastapi-expense-tracker/
├── alembic/            # DB migrations (Alembic)
├── src/
│   ├── app/
│   │   ├── database/   # DB connection & repository code
│   │   ├── models/     # SQLAlchemy models
│   │   ├── routes/     # FastAPI routes
│   │   └── schema/     # Pydantic schemas
│   └── main.py
├── .env
├── .gitignore
└── README.md
```

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/lodyne/fastapi-expense-tracker.git
   cd fastapi-expense-tracker
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

   Create a `.env` file in the project root. The project reads a DATABASE_URL-style variable. Example:

   ```env
   # Recommended format (SQLAlchemy/Databases/asyncpg compatible)
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/expenses_db

   # Or when using sync drivers (psycopg2)
   # DATABASE_URL=postgresql://user:password@localhost:5432/expenses_db
   ```

5. **Run PostgreSQL locally** (if not already running):

   Option A — using Docker (recommended for development):

   ```bash
   docker run --rm -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=expenses_db -p 5432:5432 postgres:15
   ```

   Option B — using a local Postgres service (Homebrew on macOS):

   ```bash
   brew services start postgresql
   createdb expenses_db
   ```

6. **Run database migrations (Alembic):**

   If you've changed models, run:

   ```bash
   alembic upgrade head
   ```

7. **Run the API:**

   ```bash
   # If main.py is in src/, use:
   PYTHONPATH=src uvicorn main:app --reload
   ```

   Or use your alias if set:

   ```bash
   uvrun
   ```

## API Documentation

- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## License

MIT License

---

**Author:** Lodger Mtui  
**Contact:** <lodgmtui@gmail.com>
