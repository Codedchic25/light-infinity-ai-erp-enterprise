from sqlalchemy import Column, Integer, String
from app.db.session import Base


class Customer(Base):
    __tablename__ = "customers"
    id_client = Column(Integer, primary_key=True, index=True)
    nume = Column(String, nullable=False)
    telefon = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)

