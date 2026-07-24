import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.db.session import Base, get_db
from app.core.config import settings
from app.modules.auth.service import AuthService as UserService
from app.modules.auth.schema import UserCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(name="client")
def client_fixture(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(name="user_token")
def user_token_fixture(session):
    """Genereaza un token de utilizator obsnuit (customer)."""
    user_service = UserService(session)
    user = user_service.register_user(
        UserCreate(
            email="user_crm@infinity.ai",
            password="userpassword",
            full_name="Regular User",
            role="customer",
        )
    )
    token = user_service.create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    return f"Bearer {token}"


# --- TESTE INTEGRARE CRM ---


def test_create_customer_success(client, user_token):
    """Verifica adaugarea unui client nou in baza de date CRM."""
    headers = {"Authorization": user_token}
    customer_data = {
        "nume": "Ion Popescu",
        "telefon": "0722123456",
        "email": "ion.popescu@gmail.com",
    }

    response = client.post(
        f"{settings.API_V1_STR}/customers/", json=customer_data, headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nume"] == "Ion Popescu"
    assert "id_client" in data


def test_create_duplicate_email_fails(client, user_token):
    """Verifica daca sistemul blocheaza duplicarea adresei de email in CRM."""
    headers = {"Authorization": user_token}
    customer_data = {
        "nume": "Vasile Georgescu",
        "telefon": "0733123456",
        "email": "vasile@gmail.com",
    }

    # Prima inserare
    client.post(
        f"{settings.API_V1_STR}/customers/", json=customer_data, headers=headers
    )
    # A doua inserare cu acelasi email
    response = client.post(
        f"{settings.API_V1_STR}/customers/", json=customer_data, headers=headers
    )

    assert response.status_code == 400
    assert "este deja utilizata" in response.json()["detail"]


def test_delete_customer_unauthorized_fails(client, user_token):
    """Verifica daca un utilizator simplu (non-admin) este blocat la stergerea unui client (RBAC)."""
    headers = {"Authorization": user_token}

    # ÃŽncercare stergere (ID fictiv)
    response = client.delete(f"{settings.API_V1_STR}/customers/1", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "The user does not have enough privileges"

