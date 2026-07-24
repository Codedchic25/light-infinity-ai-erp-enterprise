from datetime import datetime, timedelta
import random


def genereaza_awb_curier(comanda_data: dict) -> dict:
    """Simuleaza generarea unui AWB prin API-ul unui curier.

    Primeste datele comenzii (id, customer_name, shipping_address)
    si returneaza detaliile de expediere generate oficial.
    """
    order_id = comanda_data.get("id", 0)
    customer_name = comanda_data.get("customer_name", "Client")

    # Generam un numar unic de AWB (Prefix de companie + ID comanda + cifre aleatorii)
    cifre_aleatorii = "".join([str(random.randint(0, 9)) for _ in range(6)])
    numar_awb = f"INF{order_id:04d}{cifre_aleatorii}"

    # Calculam data estimata de livrare (in mod normal 24-48 de ore lucratoare)
    data_curenta = datetime.now()
    data_estimata_livrare = data_curenta + timedelta(days=2)

    # Structura de raspuns standard pe care o ofera un API de curierat
    detalii_livrare = {
        "status_api": "SUCCESS",
        "awb": numar_awb,
        "curier": "Infinity Express (Simulat)",
        "customer_name": customer_name,
        "shipping_address": comanda_data.get("shipping_address", "Nespecificata"),
        "data_generare": data_curenta.strftime("%Y-%m-%d %H:%M:%S"),
        "data_estimata_livrare": data_estimata_livrare.strftime("%Y-%m-%d"),
        "cost_transport_ron": 19.00,
    }

    print(
        f"ðŸšš AWB {numar_awb} generat cu succes pentru {customer_name}! Livrare estimata: {detalii_livrare['data_estimata_livrare']}"
    )
    return detalii_livrare

