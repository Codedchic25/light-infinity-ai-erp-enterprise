"""
Schemele Pydantic v2 pentru modulul de Comenzi.
Asigura validarea stricta a datelor trimise din cosul de cumparaturi la checkout.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class ComandaProdusCreate(BaseModel):
    """Schema pentru un singur produs adaugat in cos."""

    id_lumanare: int = Field(..., description="ID-ul lumÃ¢narii din catalog")
    cantitate: int = Field(
        ..., gt=0, description="Cantitatea trebuie sa fie cel putin 1"
    )


class CheckoutInput(BaseModel):
    """Schema primita de backend in momentul in care clientul apasa pe 'Plaseaza Comanda'."""

    # ÃŽn Python 3.9+, folosim direct 'list' nativ fara a mai importa nimic din typing
    produse: list[ComandaProdusCreate] = Field(
        ..., min_length=1, description="Cosul nu poate fi gol"
    )


class ComandaProdusResponse(BaseModel):
    """Schema pentru afisarea produselor din interiorul unei comenzi finalizate."""

    id_lumanare: int
    cantitate: int
    pret_salvat: float

    model_config = ConfigDict(from_attributes=True)


class ComandaResponse(BaseModel):
    """Schema completa de raspuns returnata dupa generarea cu succes a comenzii."""

    id_comanda: int
    id_user: int
    status: str
    total: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

