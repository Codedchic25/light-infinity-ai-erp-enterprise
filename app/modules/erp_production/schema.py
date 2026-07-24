"""
Schemele Pydantic v2 pentru modulul ERP de productie.
Asigura validarea datelor de intrare pentru loturi si structura raspunsului de consum conform METHOD.md.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List


class ProductionLotInput(BaseModel):
    """Schema utilizata de administrator pentru a raporta fabricarea unui lot nou de lumÃ¢nari."""

    id_lumanare: int = Field(
        ..., description="ID-ul lumÃ¢narii din catalog pentru care se porneste productia"
    )
    cantitate_de_fabricat: int = Field(
        ...,
        gt=0,
        description="Numarul de bucati finite ce urmeaza a fi fabricate (minim 1)",
    )


class MaterialConsumDetail(BaseModel):
    """Structura detaliata pentru raportarea ingredientelor consumate."""

    material: str = Field(..., description="Numele materiei prime consumate")
    cantitate_scazuta: float = Field(
        ..., description="Cantitatea totala scazuta din stocul depozitului"
    )
    unitate_masura: str = Field(..., description="Unitatea de masura (g, ml, buc)")


class ProductionLotResponse(BaseModel):
    """Schema de raspuns enterprise care garanteaza output-ul conform contractului din METHOD.md."""

    id_lot: int = Field(..., description="ID-ul simbolic sau de log al operatiunii")
    sku_produs: str = Field(..., description="Codul SKU al lumÃ¢narii fabricate")
    cantitate_fabricata: int = Field(..., description="Bucatile finite intrate in stoc")
    status: str = Field(default="succes_procesat", description="Statusul tranzactiei")
    consum_detaliat: List[MaterialConsumDetail] = Field(
        ..., description="Lista ingredientelor descarcate automat din reteta"
    )

    model_config = ConfigDict(from_attributes=True)

