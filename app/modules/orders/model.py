"""
Modelele de baza de date pentru gestionarea comenzilor si a cosului de cumparaturi.
Defineste tabelele 'comenzi' si 'comenzi_lumanari' utilizÃ¢nd SQLAlchemy.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# Corectie import: Sursa centrala definita in prima faza
from app.db.session import Base


class Comanda(Base):
    """
    Stocheaza informatiile generale ale unei comenzi plasate in magazin.
    """

    __tablename__ = "comenzi"

    id_comanda = Column(Integer, primary_key=True, index=True)

    # Legatura cu utilizatorul (clientul) care a plasat comanda
    id_client = Column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    # Statusul comenzii: 'in_asteptare', 'platita', 'expediata', 'anulata'
    status = Column(String, default="in_asteptare", nullable=False)

    # Valoarea totala a comenzii in RON
    total = Column(Float, default=0.0, nullable=False)

    # Corectie: timezone=True asigura maparea nativa ca TIMESTAMPTZ in Neon Cloud
    data_comanda = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Optimizare ORM: Relatie directa pentru incarcarea rapida a produselor asociate
    produse = relationship(
        "ComandaLumanare", back_populates="comanda", cascade="all, delete-orphan"
    )


class ComandaLumanare(Base):
    """
    Tabel de legatura care stocheaza produsele (lumÃ¢narile) din cadrul fiecarei comenzi.
    """

    __tablename__ = "comenzi_lumanari"

    id = Column(Integer, primary_key=True, index=True)
    id_comanda = Column(
        Integer, ForeignKey("comenzi.id_comanda", ondelete="CASCADE"), nullable=False
    )
    id_lumanare = Column(Integer, nullable=False)

    # Cantitatea din acest produs cumparata de client
    cantitate = Column(Integer, nullable=False)

    # Pretul istoric de la momentul cumpararii
    pret_salvat = Column(Float, nullable=False)

    # Optimizare ORM: Permite accesarea obiectului parinte direct din linia de comanda
    comanda = relationship("Comanda", back_populates="produse")

