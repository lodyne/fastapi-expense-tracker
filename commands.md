# Essential commands

## Environment setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Database (Alembic)

```bash
alembic upgrade head                # apply latest migrations
alembic revision --autogenerate -m "short message"
```

## Application (local dev)

```bash
PYTHONPATH=src python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
# alternatively export the path once, then run:
# export PYTHONPATH=src && python -m uvicorn src.main:app --reload --port 8000
# or run via Docker:
docker compose up app --build
```

## Dockerfile (single container)

```bash
docker build -t expense-tracker-api .      # build image from Dockerfile
docker run --rm -p 8000:8000 --env-file .env expense-tracker-api
```

## Docker Compose workflow

```bash
docker compose up --build           # start API + Postgres
docker compose logs -f app          # follow API logs
docker compose down -v              # stop and delete volumes
```

## Testing

```bash
pytest                              # run entire suite
pytest src/app/tests/test_postgres_routes.py -k "budget"
```
