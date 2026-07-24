from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class StockAuditCreate(BaseModel):
    id_lumanare: int = Field(..., description="ID-ul unic al produsului din ERP")
    actiune: str = Field(default="SCADERE_STOC_COMANDA", description="Tipul actiunii")
    cantitate_veche: int = Field(..., ge=0)
    cantitate_noua: int = Field(..., ge=0)


class StockAuditResponse(BaseModel):
    id: int
    id_lumanare: int
    actiune: str
    cantitate_veche: int
    cantitate_noua: int
    timestamp: datetime

    class Config:
        from_attributes = True


# --- CONFIGURARE COMPATIBILITATE PENTRU SUITA DE TESTE AUTOMATE ---
class ConsumMaterialCreate(BaseModel):
    """Schema de test pentru maparea consumului de ingrediente in BOM."""

    id_material: int
    cantitate_consumata: float


class ProductieCreate(BaseModel):
    """Schema de test pentru lansarea ordinelor de productie din fabrica."""

    id_lumanare: int
    cantitate: int
    consumuri: List[ConsumMaterialCreate] = []

