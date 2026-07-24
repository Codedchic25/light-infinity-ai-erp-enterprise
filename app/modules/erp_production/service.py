"""
Serviciul de orchestra pentru modulul ERP Productie.
Face legatura intre endpoint-urile API / Agentul AI si instrumentele tranzactionale.
"""

from sqlalchemy.orm import Session
from app.modules.erp_production.tools import ProductionTools
from app.modules.erp_production.schema import ProductionLotInput, ProductionLotResponse


class ProductionService:
    """
    Serviciu enterprise ce expune logica de business pentru managementul fabricii.
    """

    def __init__(self, db: Session):
        self.db = db
        # Instantiem utilitarele tranzactionale din tools.py
        self.tools = ProductionTools(self.db)

    def creeaza_lot_nou(
        self, lot_in: ProductionLotInput, detalii_operator: str = "Sistem Central ERP"
    ) -> ProductionLotResponse:
        """
        Orchestreaza lansarea unui nou lot in productie.
        Verifica reteta, stocurile din Neon Cloud si actualizeaza inventarul atomic.
        """
        # Delegam executia completa catre functia securizata din tools.py
        return self.tools.executa_lot_productie(
            lot_in=lot_in, detalii_operator=detalii_operator
        )

