import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.app.routes.postgres import get_db
from src.app.database.postgres import Base, engine, SessionLocal


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    """Ensure the relevant Postgres tables exist before tests run."""
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session):
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    test_client = TestClient(app)

    try:
        yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture()
def auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/postgres/auth/token",
        data={"username": "admin", "password": "admin"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_category(client, headers, name="Food"):
    response = client.post(
        "/api/v1/postgres/categories",
        json={"name": name},
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()


def create_budget(client, headers, name="Monthly Budget", amount=5000.0):
    response = client.post(
        "/api/v1/postgres/budgets",
        json={"name": name, "amount": amount},
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()


def test_create_and_list_categories(client, auth_headers):
    category = create_category(client, auth_headers)

    list_response = client.get(
        "/api/v1/postgres/categories",
        headers=auth_headers,
    )
    assert list_response.status_code == 200
    payload = list_response.json()
    assert any(item["id"] == category["id"] for item in payload)


def test_create_budget_and_get_single(client, auth_headers):
    budget = create_budget(client, auth_headers)

    response = client.get(
        f"/api/v1/postgres/budgets/{budget['id']}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == budget["name"]
    assert data["amount"] == budget["amount"]


def test_create_and_delete_expense(client, auth_headers):
    category = create_category(client, auth_headers, name="Travel")
    budget = create_budget(client, auth_headers, name="Travel Budget", amount=1000.0)

    expense_payload = {
        "name": "Flight",
        "amount": 250.5,
        "category_id": category["id"],
        "budget_id": budget["id"],
    }

    create_response = client.post(
        "/api/v1/postgres/expenses",
        json=expense_payload,
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    expense = create_response.json()
    assert expense["name"] == expense_payload["name"]
    assert expense["amount"] == expense_payload["amount"]

    delete_response = client.delete(
        f"/api/v1/postgres/expenses/{expense['id']}",
        headers=auth_headers,
    )
    assert delete_response.status_code == 204

    not_found_response = client.get(
        f"/api/v1/postgres/expenses/{expense['id']}",
        headers=auth_headers,
    )
    assert not_found_response.status_code == 404
