"""
Suita de teste unitare pentru validarea algoritmului de livrare (Shipping)
si a mecanismelor de Background Tasks din FastAPI.
"""

from datetime import datetime
from unittest.mock import patch
import pytest
from fastapi import BackgroundTasks

from app.shared.invoice_generator import calculate_delivery_date
from app.shared.notifications import send_order_email, check_and_send_stock_sms


@pytest.fixture
def mock_now():
    """Fixture utilitar pentru a injecta o data fixa in teste."""
    return datetime(2026, 7, 20, 12, 0)  # Luni, 20 Iulie 2026


def test_calculate_delivery_date_standard_day():
    """
    Test 1: Verifica daca intr-o zi normala (Miercuri),
    adunarea a 2 zile returneaza corect ziua de Vineri.
    """
    miercuri_mock = datetime(2026, 7, 22, 12, 0)

    with patch("app.shared.invoice_generator.datetime") as mock_datetime:
        mock_datetime.now.return_value = miercuri_mock
        mock_datetime.strftime = datetime.strftime

        data_estimata = calculate_delivery_date()
        assert data_estimata == "24-07-2026"


def test_calculate_delivery_date_skips_sunday():
    """
    Test 2 (CRITIC): Verifica daca livrarea ar pica Duminica,
    algoritmul o muta automat pentru Luni.
    """
    vineri_mock = datetime(2026, 7, 24, 12, 0)

    with patch("app.shared.invoice_generator.datetime") as mock_datetime:
        mock_datetime.now.return_value = vineri_mock
        mock_datetime.strftime = datetime.strftime

        data_estimata = calculate_delivery_date()
        assert data_estimata == "27-07-2026"

        obiect_data = datetime.strptime(data_estimata, "%d-%m-%Y")
        assert obiect_data.weekday() != 6


def test_calculate_delivery_date_order_on_saturday():
    """
    Test 3: Verifica comportamentul daca o comanda se pune SÃ¢mbata,
    iar livrarea standard de 2 zile ar pica Luni.
    """
    sambata_mock = datetime(2026, 7, 25, 12, 0)

    with patch("app.shared.invoice_generator.datetime") as mock_datetime:
        mock_datetime.now.return_value = sambata_mock
        mock_datetime.strftime = datetime.strftime

        data_estimata = calculate_delivery_date()
        assert data_estimata == "27-07-2026"


def test_background_tasks_registration():
    """
    Test 4: Verifica daca sarcinile asincrone sunt adaugate
    corect in coada nativa FastAPI pentru email-uri si SMS-uri.
    """
    tasks = BackgroundTasks()

    # ÃŽnregistram sarcinile in worker-ul local
    tasks.add_task(send_order_email, "test@infinity.ai", 101, 45.90)
    tasks.add_task(check_and_send_stock_sms, "Ceara de Soia Flocoane", -5.0)

    # Validam structural coada de executie
    assert len(tasks.tasks) == 2
    assert tasks.tasks[0].func == send_order_email
    assert tasks.tasks[1].func == check_and_send_stock_sms

