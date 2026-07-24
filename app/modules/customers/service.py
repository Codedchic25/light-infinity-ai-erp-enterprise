from sqlalchemy.orm import Session
from app.modules.customers.model import Customer
from app.modules.customers.schema import ClientCreate


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def register_customer(self, data: ClientCreate) -> Customer:
        obj = Customer(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

