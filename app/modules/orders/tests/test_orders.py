from main import app
from app.modules.auth.dependencies import get_current_user


# Structura mock pentru a simula un utilizator activ autentificat
class MockUser:
    id = 8
    email = "test_pytest@infinity.ai"
    role = "customer"
    is_active = True


def mock_get_current_user():
    """Returneaza un utilizator valid pentru a trece de bariera de securitate JWT."""
    return MockUser()


def test_checkout_tranzactional_succes(client):
    """Valideaza plasarea unei comenzi prin ruta oficiala unificata de checkout cu user autentificat."""
    # ÃŽnregistram suprascrierea dependentei pentru acest test
    app.dependency_overrides[get_current_user] = mock_get_current_user

    payload = {
        "nume_client": "Client Test",
        "email_client": "test_pytest@infinity.ai",
        "adresa_livrare": "Strada Fabricii Nr. 10, Cluj-Napoca",
        "produse": [{"id_lumanare": 2, "cantitate": 1, "pret_salvat": 45.0}],
    }

    try:
        response = client.post("/orders/checkout", json=payload)
        assert response.status_code == 201, (
            f"Checkout-ul a esuat cu status {response.status_code}: {response.text}"
        )
        assert response.json().get("status") == "succes"
    finally:
        # Curatam obligatoriu overrides dupa executie pentru a nu afecta alte teste
        app.dependency_overrides.clear()


def test_checkout_stoc_insuficient(client):
    """Garanteaza ca sistemul refuza tranzactiile daca cosul este gol, chiar si pentru utilizatori logati."""
    app.dependency_overrides[get_current_user] = mock_get_current_user

    payload = {
        "nume_client": "Client Test",
        "email_client": "test_pytest@infinity.ai",
        "adresa_livrare": "Strada Fabricii",
        "produse": [],  # Cos gol
    }

    try:
        response = client.post("/orders/checkout", json=payload)
        assert response.status_code == 400, (
            f"Asteptat status 400 pentru cos gol, primit: {response.status_code}"
        )
    finally:
        app.dependency_overrides.clear()

