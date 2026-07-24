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
from app.modules.analytics.service import AnalyticsService

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


@pytest.fixture(name="admin_token")
def admin_token_fixture(session):
    user_service = UserService(session)
    admin_user = user_service.register_user(
        UserCreate(
            email="admin_bi@infinity.ai",
            password="adminpassword",
            full_name="Admin BI",
            role="admin",
        )
    )
    token = user_service.create_access_token(
        data={"sub": admin_user.email, "role": admin_user.role}
    )
    return f"Bearer {token}"


# --- TESTE PRECIZIE MATEMATICÄ‚ BI ---


def test_empty_analytics_returns_zero_structures(session):
    """Verifica comportamentul algoritmilor cÃ¢nd baza de date ERP nu contine date comerciale."""
    service = AnalyticsService(session)
    report = service.calculeaza_statistici_dashboard()

    assert report.kpis.venit_total == 0.0
    assert report.kpis.numar_comenzi == 0
    assert report.kpis.valoare_medie_comanda == 0.0
    assert report.kpis.total_lumanari_vandute == 0
    assert len(report.top_produse) == 0


def test_analytics_calculations_precision(client, admin_token, session):
    """
    Insereaza un set fix de tranzactii in sistem si verifica daca agregarile
    Pandas/NumPy returneaza indicatorii KPI exacti in endpoint-ul REST protect.
    """
    headers = {"Authorization": admin_token}

    # 1. Creare client si nomenclatoare
    c_res = client.post(
        f"{settings.API_V1_STR}/customers/",
        json={"nume": "BI Client", "email": "bi@test.ai"},
        headers=headers,
    ).json()
    id_client = c_res["id_client"]

    c_id = client.post(
        f"{settings.API_V1_STR}/products/attributes/ceara?name=Soia", headers=headers
    ).json()["id"]
    s_id = client.post(
        f"{settings.API_V1_STR}/products/attributes/sezon?name=Vara", headers=headers
    ).json()["id"]
    f_id = client.post(
        f"{settings.API_V1_STR}/products/attributes/forma?name=Pahar", headers=headers
    ).json()["id"]
    p_id = client.post(
        f"{settings.API_V1_STR}/products/attributes/parfum?name=Menta", headers=headers
    ).json()["id"]
    cul_id = client.post(
        f"{settings.API_V1_STR}/products/attributes/culoare?name=Verde", headers=headers
    ).json()["id"]

    # 2. Creare doua tipuri de lumÃ¢nari diferite
    prod1 = client.post(
        f"{settings.API_V1_STR}/products/",
        json={
            "nume": "LumÃ¢nare Mint",
            "sku": "LUM-MNT-01",
            "pret": 40.00,
            "stoc": 50,
            "id_ceara": c_id,
            "id_sezon": s_id,
            "id_forma": f_id,
            "id_parfum": p_id,
            "id_culoare": cul_id,
        },
        headers=headers,
    ).json()

    prod2 = client.post(
        f"{settings.API_V1_STR}/products/",
        json={
            "nume": "LumÃ¢nare Green",
            "sku": "LUM-GRN-02",
            "pret": 60.00,
            "stoc": 50,
            "id_ceara": c_id,
            "id_sezon": s_id,
            "id_forma": f_id,
            "id_parfum": p_id,
            "id_culoare": cul_id,
        },
        headers=headers,
    ).json()

    # 3. Plasare comenzi cu valori cunoscute
    # Comanda 1: 2x Prod1 = 80.00 RON
    client.post(
        f"{settings.API_V1_STR}/orders/",
        json={
            "id_client": id_client,
            "produse": [{"id_lumanare": prod1["id_lumanare"], "cantitate": 2}],
        },
        headers=headers,
    )

    # Comanda 2: 1x Prod2 = 60.00 RON
    client.post(
        f"{settings.API_V1_STR}/orders/",
        json={
            "id_client": id_client,
            "produse": [{"id_lumanare": prod2["id_lumanare"], "cantitate": 1}],
        },
        headers=headers,
    )

    # 4. Interogare endpoint Analytics Dashboard si validare matematica
    response = client.get(f"{settings.API_V1_STR}/analytics/dashboard", headers=headers)
    assert response.status_code == 200
    data = response.json()

    # Total Venituri: 80 + 60 = 140.00 RON
    assert data["kpis"]["venit_total"] == 140.00
    assert data["kpis"]["numar_comenzi"] == 2
    # Valoare Medie: 140 / 2 = 70.00 RON
    assert data["kpis"]["valoare_medie_comanda"] == 70.00
    # Total vÃ¢ndute: 2 + 1 = 3 bucati
    assert data["kpis"]["total_lumanari_vandute"] == 3

