from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.connection import Base  # Conectare directa la instanta centrala inspectata


class StockAuditLog(Base):
    __tablename__ = "stock_audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_lumanare = Column(Integer, index=True, nullable=False)
    actiune = Column(String(100), default="SCADERE_STOC_COMANDA", nullable=False)
    cantitate_veche = Column(Integer, nullable=False)
    cantitate_noua = Column(Integer, nullable=False)
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

