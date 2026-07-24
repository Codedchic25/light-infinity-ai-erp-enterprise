"""
Serviciul de business pentru gestionarea catalogului de produse.
Include logica de manipulare a stocurilor, adaugare loturi si nomenclatoare.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.catalog.model import Ceara, Sezon, Forma, Parfum, Culoare, Lumanare
from app.modules.catalog.schema import LumanareCreate, LumanareUpdate


class CatalogService:
    """
    Clasa centralizata pentru gestionarea tranzactiilor SQL legate de catalog.
    """

    def __init__(self, db: Session):
        self.db = db

    # --- Metode Management Nomenclatoare ---

    def add_ceara(self, tip: str) -> Ceara:
        """Adauga un tip nou de ceara in nomenclator."""
        obj = Ceara(tip=tip)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def add_sezon(self, nume: str) -> Sezon:
        """Adauga un sezon nou in nomenclator."""
        obj = Sezon(nume=nume)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def add_forma(self, nume: str) -> Forma:
        """Adauga o forma noua in nomenclator."""
        obj = Forma(nume=nume)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def add_parfum(self, nume: str) -> Parfum:
        """Adauga un parfum nou in nomenclator."""
        obj = Parfum(nume=nume)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def add_culoare(self, nume: str) -> Culoare:
        """Adauga o culoare noua in nomenclator."""
        obj = Culoare(nume=nume)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    # --- Metode Management LumÃ¢nari (Produse) ---

    def create_lumanare(self, candle_in: LumanareCreate) -> Lumanare:
        """
        Creeaza o lumÃ¢nare noua in catalog, verificÃ¢nd unicitatea codului SKU.
        """
        # Securitate: Prevenim duplicarea codurilor SKU in inventar
        existing = self.db.query(Lumanare).filter(Lumanare.sku == candle_in.sku).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Produsul cu SKU-ul '{candle_in.sku}' exista deja in stoc.",
            )

        db_candle = Lumanare(
            sku=candle_in.sku,
            nume=candle_in.nume,
            pret=candle_in.pret,
            stoc=candle_in.stoc,
            id_ceara=candle_in.id_ceara,
            id_sezon=candle_in.id_sezon,
            id_forma=candle_in.id_forma,
            id_parfum=candle_in.id_parfum,
            id_culoare=candle_in.id_culoare,
        )

        self.db.add(db_candle)
        self.db.commit()
        self.db.refresh(db_candle)
        return db_candle

    def get_all_lumanari(self) -> list[Lumanare]:
        """Returneaza lista completa a lumÃ¢narilor din catalog."""
        return self.db.query(Lumanare).all()

    def get_lumanare_by_id(self, id_lumanare: int) -> Lumanare:
        """Cauta o lumÃ¢nare dupa ID-ul sau sau returneaza eroare 404."""
        candle = (
            self.db.query(Lumanare).filter(Lumanare.id_lumanare == id_lumanare).first()
        )
        if not candle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="LumÃ¢narea solicitata nu a fost gasita.",
            )
        return candle

    def update_lumanare(self, id_lumanare: int, candle_in: LumanareUpdate) -> Lumanare:
        """
        Actualizeaza partial atributele unei lumÃ¢nari (ex: pret sau stoc modificat).
        """
        db_candle = self.get_lumanare_by_id(id_lumanare)

        # Actualizam dinamic doar cÃ¢mpurile trimise in cerere
        update_data = candle_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_candle, key, value)

        self.db.commit()
        self.db.refresh(db_candle)
        return db_candle

