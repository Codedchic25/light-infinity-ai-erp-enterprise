from typing import List
from pydantic import BaseModel


class KPISummary(BaseModel):
    venit_total: float
    numar_comenzi: int
    valoare_medie_comanda: float
    total_lumanari_vandute: int


class ProductSalesPerformance(BaseModel):
    id_lumanare: int
    nume_lumanare: str
    sku: str
    cantitate_vanduta: int
    venit_generat: float


class MaterialConsumptionReport(BaseModel):
    id_material: int
    nume_material: str
    unitate: str
    total_consumat: float
    stoc_ramas_actual: float


class DashboardAnalyticsResponse(BaseModel):
    kpis: KPISummary
    top_produse: List[ProductSalesPerformance]
    consum_materiale: List[MaterialConsumptionReport]

