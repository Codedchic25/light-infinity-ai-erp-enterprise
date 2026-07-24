from sqlalchemy.orm import Session
from app.modules.inventory.model import StockAuditLog
from app.modules.inventory.schema import StockAuditCreate


class InventoryService:
    @staticmethod
    def create_audit_entry(db: Session, audit_data: StockAuditCreate) -> StockAuditLog:
        db_log = StockAuditLog(
            id_lumanare=audit_data.id_lumanare,
            actiune=audit_data.actiune,
            cantitate_veche=audit_data.cantitate_veche,
            cantitate_noua=audit_data.cantitate_noua,
        )
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log

    @staticmethod
    def get_audit_trail(db: Session, limit: int = 100) -> list[StockAuditLog]:
        return (
            db.query(StockAuditLog).order_by(StockAuditLog.id.desc()).limit(limit).all()
        )

