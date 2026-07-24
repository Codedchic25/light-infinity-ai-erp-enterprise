import os
import sys
from dotenv import load_dotenv

# Fortam Python sa vada radacina proiectului pentru a evita ModuleNotFoundError
sys.path.append(os.getcwd())

# Incarcam variabilele de mediu inainte de orice import intern
load_dotenv()

# Ignoram ordinea standard de import pentru Ruff deoarece avem nevoie de sys.path si load_dotenv inainte
from app.security.password import get_password_hash  # noqa: E402
from app.db.session import Base, SessionLocal, engine  # noqa: E402
from app.modules.auth.model import User  # noqa: E402
from app.modules.catalog.model import (  # noqa: E402
    Ceara,
    Culoare,
    Forma,
    Lumanare,
    Parfum,
    Sezon,
)
from app.modules.erp_production.model import Material  # noqa: E402
from sqlalchemy import text  # noqa: E402


def seed_database():
    print("⚙️ [SEED] Sincronizare structura tabele SQL...")
    Base.metadata.create_all(bind=engine)

    # Citim credentialele in siguranta din fisierul .env local
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin_bi@infinity.ai")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "schimba_ma_in_productie")

    db = SessionLocal()
    try:
        # ==============================================================================
        # 1. POPULARE UTILIZATOR ADMINISTRATOR (SQL BRUT)
        # ==============================================================================
        print("🔄 [SEED] Reimprospatare utilizator administrator...")
        db.query(User).filter(User.email == ADMIN_EMAIL).delete()
        db.commit()

        # Generam hash-ul folosind parola citita corect din VARIABILA DE MEDIU (.env)
        parola_criptata_str = get_password_hash(ADMIN_PASSWORD)

        # Inseram datele direct prin SQL Brut securizat
        sql_query = text(
            "INSERT INTO users (email, hashed_password, full_name, fullname, role, is_active) "
            "VALUES (:email, :hashed_password, :full_name, :fullname, :role, :is_active)"
        )
        db.execute(
            sql_query,
            {
                "email": ADMIN_EMAIL,
                "hashed_password": parola_criptata_str,
                "full_name": "Administrator Executiv BI",
                "fullname": "Administrator Executiv BI",
                "role": "admin",
                "is_active": True,
            },
        )
        db.commit()
        print("✅ [SEED] Utilizator Administrator salvat cu succes via Direct SQL.")

        # ==============================================================================
        # 2. POPULARE NOMENCLATOARE CATALOG (ELIMINARE CONFLICTE FOREIGN KEY)
        # ==============================================================================
        print("📦 [SEED] Populare nomenclatoare pentru atribute lumanari...")
        db.query(Lumanare).delete()
        db.query(Ceara).delete()
        db.query(Sezon).delete()
        db.query(Forma).delete()
        db.query(Parfum).delete()
        db.query(Culoare).delete()
        db.commit()

        ceara_soia = Ceara(id_ceara=1, tip="Soia")
        sezon_general = Sezon(id_sezon=1, nume="Toate Sezoanele")
        forma_pahar = Forma(id_forma=1, nume="Pahar")
        parfum_relax = Parfum(id_parfum=1, nume="Menta")
        parfum_lavanda = Parfum(id_parfum=2, nume="Lavanda")
        culoare_verde = Culoare(id_culoare=1, nume="Verde")
        culoare_albastru = Culoare(id_culoare=2, nume="Albastru")

        db.add_all(
            [
                ceara_soia,
                sezon_general,
                forma_pahar,
                parfum_relax,
                parfum_lavanda,
                culoare_verde,
                culoare_albastru,
            ]
        )
        db.commit()

        # ==============================================================================
        # 3. POPULARE CATALOG LUMANARI
        # ==============================================================================
        print("🕯️ [SEED] Populare catalog central de lumanari...")

        lumanare_1 = Lumanare(
            id_lumanare=1,
            sku="LUM-SOIA-RELAX-01",
            nume="Lumanare Relaxare",
            pret=45.90,
            stoc=25,
            id_ceara=1,
            id_sezon=1,
            id_forma=1,
            id_parfum=1,
            id_culoare=1,
        )

        lumanare_2 = Lumanare(
            id_lumanare=2,
            sku="LUM-SOIA-LAV-02",
            nume="Lumanare Parfumata Lavanda",
            pret=45.00,
            stoc=18,
            id_ceara=1,
            id_sezon=1,
            id_forma=1,
            id_parfum=2,
            id_culoare=2,
        )

        db.add_all([lumanare_1, lumanare_2])
        db.commit()
        print("✅ [SEED] Catalogul de lumanari a fost sincronizat cu succes.")

        # ==============================================================================
        # 4. POPULARE NOMENCLATOR MATERII PRIME ERP
        # ==============================================================================
        if not db.query(Material).first():
            ceara_mat = Material(
                nume="Ceara de Soia Flocoane",
                stoc_curent=500.0,
                unitate_masura="kg",
            )
            db.add(ceara_mat)
            db.commit()
            print("✅ [SEED] Materie prima Lumanare de Soia adaugata in inventar.")

        print("🚀 [SEED] Seeding complet finalizat cu succes 100% verde si sincronizat!")

    except Exception as e:
        db.rollback()
        print(f"❌ [SEED ERROR] Generarea datelor a esuat critic: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

