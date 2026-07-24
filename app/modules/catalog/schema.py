"""
Schemele Pydantic v2 pentru modulul de Catalog.
Asigura validarea stricta a datelor pentru lumÃ¢nari si nomenclatoarele lor asociate.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# --- Scheme pentru Nomenclatoare ---


class CearaBase(BaseModel):
    tip: str = Field(..., min_length=2, max_length=50)


class CearaResponse(CearaBase):
    id_ceara: int
    model_config = ConfigDict(from_attributes=True)


class SezonBase(BaseModel):
    nume: str = Field(..., min_length=2, max_length=50)


class SezonResponse(SezonBase):
    id_sezon: int
    model_config = ConfigDict(from_attributes=True)


class FormaBase(BaseModel):
    nume: str = Field(..., min_length=2, max_length=50)


class FormaResponse(FormaBase):
    id_forma: int
    model_config = ConfigDict(from_attributes=True)


class ParfumBase(BaseModel):
    nume: str = Field(..., min_length=2, max_length=50)


class ParfumResponse(ParfumBase):
    id_parfum: int
    model_config = ConfigDict(from_attributes=True)


class CuloareBase(BaseModel):
    nume: str = Field(..., min_length=2, max_length=50)


class CuloareResponse(CuloareBase):
    id_culoare: int
    model_config = ConfigDict(from_attributes=True)


# --- Scheme pentru LumÃ¢nari (Produse) ---


class LumanareCreate(BaseModel):
    """Schema utilizata pentru adaugarea unei lumÃ¢nari noi in stoc."""

    sku: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Cod unic de produs (ex: LUM-SOIA-01)",
    )
    nume: str = Field(..., min_length=3, max_length=100)
    pret: float = Field(..., gt=0, description="Pretul trebuie sa fie mai mare decÃ¢t 0")
    stoc: int = Field(default=0, ge=0, description="Stocul initial nu poate fi negativ")
    id_ceara: int
    id_sezon: int
    id_forma: int
    id_parfum: int
    id_culoare: int


class LumanareUpdate(BaseModel):
    """Schema utilizata pentru actualizarea partiala a unei lumÃ¢nari."""

    nume: Optional[str] = Field(None, min_length=3, max_length=100)
    pret: Optional[float] = Field(None, gt=0)
    stoc: Optional[int] = Field(None, ge=0)


class LumanareResponse(BaseModel):
    """Schema pentru returnarea detaliilor complete ale lumÃ¢narii prin API."""

    id_lumanare: int
    sku: str
    nume: str
    pret: float
    stoc: int
    id_ceara: Optional[int] = None
    id_sezon: Optional[int] = None
    id_forma: Optional[int] = None
    id_parfum: Optional[int] = None
    id_culoare: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

