import os
import time
from fastapi.testclient import TestClient
from sqlalchemy import func

from main import app
from app.db.session import get_db, engine, Base
from app.modules.catalog.model import Lumanare
from app.modules.erp_production.model import Material, StockAuditLog, Reteta

client = TestClient(app)


def test_stripe_webhook_flow():
    """
    Test de Integrare E2E Curat: Valideaza decrementarea atomica BOM,
    jurnalul de audit industrial si generarea facturii PDF in mod asincron.
    """
    # Ne asiguram ca baza locala SQLite are structura creata corect din metadatele unificate
    Base.metadata.create_all(bind=engine)

    db = next(get_db())

    cale_factura = os.path.join(".", "storage", "invoices", "factura_comanda_8.pdf")
    if os.path.exists(cale_factura):
        os.remove(cale_factura)

    try:
        # ---------------------------------------------------------
        # FAZA A: SETUP DATE DE SIMULARE (CONFORM CONSTRÃ‚NGERILOR)
        # ---------------------------------------------------------
        lumanare_test = db.query(Lumanare).filter(Lumanare.id_lumanare == 2).first()
        if not lumanare_test:
            lumanare_test = Lumanare(
                id_lumanare=2,
                nume="LumÃ¢nare Parfumata Lavanda",
                sku="LUM-LAV-02",
                pret=45.0,
                stoc=100,
            )
            db.add(lumanare_test)
            db.flush()

        material_ceara = (
            db.query(Material).filter(func.lower(Material.nume).like("%cear%")).first()
        )
        if not material_ceara:
            material_ceara = Material(
                nume="Ceara de albine naturala", stoc_curent=500.0, unitate_masura="kg"
            )
            db.add(material_ceara)
            db.flush()
        else:
            material_ceara.stoc_curent = 500.0

        reteta_test = (
            db.query(Reteta)
            .filter(
                Reteta.id_lumanare == 2,
                Reteta.id_material == material_ceara.id_material,
            )
            .first()
        )
        if not reteta_test:
            reteta_test = Reteta(
                id_lumanare=2,
                id_material=material_ceara.id_material,
                cantitate_necesara=4.0,
            )
            db.add(reteta_test)

        db.commit()

        # ---------------------------------------------------------
        # FAZA B: EXECUÈšIE (Payload Stripe in aplicatia FastAPI)
        # ---------------------------------------------------------
        payload = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "metadata": {"order_id": "8"},
                    "payment_status": "paid",
                    "customer_details": {"email": "test_client@infinity.ai"},
                    "amount_total": 15000,
                }
            },
        }
        headers = {
            "Content-Type": "application/json",
            "Stripe-Signature": "simulat_local",
        }

        response = client.post("/webhook", json=payload, headers=headers)

        # ---------------------------------------------------------
        # FAZA C: VALIDARE COMPUSÄ‚ NATIVÄ‚
        # ---------------------------------------------------------
        assert response.status_code == 200, f"Eroare Webhook: {response.text}"

        # Verificam scaderea din DB
        db.refresh(material_ceara)
        assert material_ceara.stoc_curent == 496.0, (
            f"Eroare BOM! Stoc curent: {material_ceara.stoc_curent}"
        )

        # Polling pasiv pentru scrierea fizica a facturii asincrone pe disc
        timp_asteptat = 0
        while not os.path.exists(cale_factura) and timp_asteptat < 20:
            time.sleep(0.1)
            timp_asteptat += 1

        assert os.path.exists(cale_factura), (
            "Documentul PDF fiscal nu a fost generat pe disc!"
        )
        assert os.path.getsize(cale_factura) > 0, "Fisierul fiscal generat este gol!"

        ultimul_log = (
            db.query(StockAuditLog).order_by(StockAuditLog.id_log.desc()).first()
        )
        assert ultimul_log is not None
        assert ultimul_log.tip_actiune == "vanzare_comanda"

    finally:
        db.close()

