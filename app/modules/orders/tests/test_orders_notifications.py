import os
import asyncio
from app.shared.invoice_generator import generate_invoice_pdf, calculate_delivery_date


def test_invoice_and_shipping_logic():
    """Valideaza calculul asincron al datei de livrare si scrierea fizica a facturii."""
    # 1. Validare format data de livrare (DD-MM-YYYY)
    delivery_date = calculate_delivery_date()
    assert len(delivery_date) == 10
    assert delivery_date[2] == "-" and delivery_date[5] == "-"

    # 2. Corectie asincrona: Executam coroutine-ul in mod controlat prin asyncio.run
    pdf_path = asyncio.run(
        generate_invoice_pdf(
            order_id=999, customer_email="client_test@infinity.ai", total_amount=135.50
        )
    )

    # 3. Validare existenta fisier fizic generat
    assert isinstance(pdf_path, str), "Calea returnata trebuie sa fie un string valid!"
    assert os.path.exists(pdf_path) is True, (
        f"Fisierul PDF lipseste de pe disc la calea: {pdf_path}"
    )
    assert os.path.getsize(pdf_path) > 0, "Fisierul PDF generat este gol!"

