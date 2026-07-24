"""
Modelele de baza de date pentru catalogul de produse si nomenclatoare.
Defineste structura tabelelor 'lumanari', 'ceara', 'sezon', 'forma', 'parfum' si 'culoare'.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey

# Corectie Critica: Legam modelul de instanta centrala de metadate auditata in Faza 1
from app.db.session import Base


class Ceara(Base):
    """Nomenclator pentru tipurile de ceara folosite in productie."""

    __tablename__ = "ceara"
    id_ceara = Column(Integer, primary_key=True, index=True)
    tip = Column(String, nullable=False)


class Sezon(Base):
    """Nomenclator pentru colectiile sezoniere ale magazinului."""

    __tablename__ = "sezon"
    id_sezon = Column(Integer, primary_key=True, index=True)
    nume = Column(String, nullable=False)


class Forma(Base):
    """Nomenclator pentru recipientele sau formele lumÃ¢narilor."""

    __tablename__ = "forma"
    id_forma = Column(Integer, primary_key=True, index=True)
    nume = Column(String, nullable=False)


class Parfum(Base):
    """Nomenclator pentru aromele utilizate."""

    __tablename__ = "parfum"
    id_parfum = Column(Integer, primary_key=True, index=True)
    nume = Column(String, nullable=False)


class Culoare(Base):
    """Nomenclator pentru culorile disponibile."""

    __tablename__ = "culoare"
    id_culoare = Column(Integer, primary_key=True, index=True)
    nume = Column(String, nullable=False)


class Lumanare(Base):
    """Tabelul central al produselor din magazin (Catalogul de LumÃ¢nari)."""

    __tablename__ = "lumanari"
    id_lumanare = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    nume = Column(String, nullable=False)
    pret = Column(Float, nullable=False)
    stoc = Column(Integer, default=0)

    # Relatii si chei straine catre nomenclatoare
    id_ceara = Column(Integer, ForeignKey("ceara.id_ceara"))
    id_sezon = Column(Integer, ForeignKey("sezon.id_sezon"))
    id_forma = Column(Integer, ForeignKey("forma.id_forma"))
    id_parfum = Column(Integer, ForeignKey("parfum.id_parfum"))
    id_culoare = Column(Integer, ForeignKey("culoare.id_culoare"))

