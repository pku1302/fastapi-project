import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from app.main import app
from app.database.database import get_session

TEST_DATABASE_URL = "postgresql://postgres:rjsqod1399#@localhost:5432/testdb"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    yield engine

@pytest.fixture
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
def created_post(client, token):
    response = client.post(
        "/posts", 
        headers={
            "Authorization": f"Bearer {token}"
        }, 
        json={
            "title": "test",
            "content": "test content",
        })
    
    assert response.status_code ==200 
    return response.json()

@pytest.fixture
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)
    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def created_user(client):
    response = client.post("/signup", json={
        "id": "testuser",
        "password": "testpassword",
    })
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def token(client, created_user):
    response = client.post(
        "/token",
        data={
            "username": created_user["id"],
            "password": "testpassword"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }    
    )
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

