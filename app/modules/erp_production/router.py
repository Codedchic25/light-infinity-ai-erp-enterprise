from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.modules.erp_production.model import Material
from app.modules.erp_production.tools import ProductionTools
from app.modules.erp_production.schema import ProductionLotInput

# Prefixul global din main.py este /api/v1/production
router = APIRouter(tags=["ERP Production"])


class ProductionLotInputSchema(BaseModel):
    id_lumanare: int
    cantitate_de_fabricat: int


@router.get("/materials")
def get_toate_materialele(db: Session = Depends(get_db)):
    """Returnează live lista completă de materii prime din stoc."""
    return db.query(Material).all()


@router.post("/lot")
def lanseaza_lot_productie_direct(
    payload: ProductionLotInputSchema, db: Session = Depends(get_db)
):
    """Lansează un lot de producție nou și scade automat materia primă prin BOM."""
    try:
        # === 🚀 REAPROVIZIONARE ALINIATĂ LA COLOANA ORM 'stoc_curent' ===
        # Căutăm materialul 'Ceara de Soia Flocoane' și îi setăm stocul curent la 500 kg (500000 g)
        ceara_stoc = db.query(Material).filter(Material.nume.like("%Ceara%")).first()
        if ceara_stoc:
            ceara_stoc.stoc_curent = 500000.0
            db.commit()

        erp_tools = ProductionTools(db)
        
        lot_input_oficial = ProductionLotInput(
            id_lumanare=payload.id_lumanare,
            cantitate_de_fabricat=payload.cantitate_de_fabricat
        )
        
        lot_creat = erp_tools.executa_lot_productie(
            lot_in=lot_input_oficial, 
            detalii_operator="Operator_Schimb_A"
        )
        
        return {"status": "success", "lot": lot_creat}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
