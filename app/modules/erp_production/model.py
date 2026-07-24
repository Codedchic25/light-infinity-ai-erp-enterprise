"""
Modelele de baza de date pentru modulul ERP de productie.
Defineste tabelele 'materiale', 'retete' si 'stock_audit_logs' utilizÃ¢nd SQLAlchemy.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# Corectie import: Unificarea cu punctul central stabilit in Faza 1
from app.db.session import Base


class Material(Base):
    """
    Stocheaza materiile prime brute din inventar (ceara, parfum, fitiluri).
    """

    __tablename__ = "materiale"

    id_material = Column(Integer, primary_key=True, index=True)
    nume = Column(String, unique=True, index=True, nullable=False)

    # Cantitatea curenta in stoc (g, ml sau bucati)
    stoc_curent = Column(Float, default=0.0, nullable=False)
    unitate_masura = Column(String, nullable=False)  # 'g', 'ml', 'buc'

    # Relatie utila pentru a vedea in ce retete este inclus materialul
    retete_asociate = relationship(
        "Reteta", back_populates="material", cascade="all, delete-orphan"
    )


class Reteta(Base):
    """
    Defineste ingredientele necesare pentru fabricarea unei singure unitati de lumÃ¢nare.
    Relatie de legatura intre tabela 'lumanari' si tabela 'materiale'.
    """

    __tablename__ = "retete"

    id_reteta = Column(Integer, primary_key=True, index=True)
    id_lumanare = Column(
        Integer, ForeignKey("lumanari.id_lumanare", ondelete="CASCADE"), nullable=False
    )
    id_material = Column(
        Integer, ForeignKey("materiale.id_material", ondelete="CASCADE"), nullable=False
    )

    # Cantitatea necesara pentru O SINGURÄ‚ lumÃ¢nare (ex: 180.0 grame)
    cantitate_necesara = Column(Float, nullable=False)

    # Optimizare ORM relationships pentru interogari rapide in algoritmul BOM
    material = relationship("Material", back_populates="retete_asociate")


class StockAuditLog(Base):
    """
    Jurnal de audit industrial (Audit Trail) obligatoriu in aplicatiile enterprise.
    ÃŽnregistreaza orice adaugare sau scadere automata de stoc din sistem.
    """

    __tablename__ = "stock_audit_logs"

    id_log = Column(Integer, primary_key=True, index=True)

    # Tipul entitatii modificate: 'lumanare' sau 'material'
    tip_entitate = Column(String, nullable=False)
    entitate_id = Column(Integer, nullable=False)

    # Tipul actiunii: 'productie', 'vanzare_comanda', 'ajustare_manuala'
    tip_actiune = Column(String, nullable=False)

    # Valoarea modificarii (pozitiva pentru intrari, negativa pentru iesiri/consum)
    cantitate_modificata = Column(Float, nullable=False)

    # Utilizatorul sau procesul care a declansat modificarea
    detalii = Column(String, nullable=True)

    # Corectie: timezone=True garanteaza marcajul TIMESTAMPTZ nativ in Neon DB
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

