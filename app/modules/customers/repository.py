from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.modules.customers.model import Client
from app.modules.customers.schema import ClientCreate, ClientUpdate


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_client: int) -> Optional[Client]:
        """Preia un client pe baza ID-ului unic."""
        return self.db.get(Client, id_client)

    def get_by_email(self, email: str) -> Optional[Client]:
        """Preia un client pe baza adresei de email."""
        statement = select(Client).where(Client.email == email)
        return self.db.execute(statement).scalar_one_or_none()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Client]:
        """Preia o lista paginata de clienti pentru CRM."""
        statement = select(Client).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, obj_in: ClientCreate) -> Client:
        """ÃŽnregistreaza un client nou in baza de date."""
        db_obj = Client(nume=obj_in.nume, telefon=obj_in.telefon, email=obj_in.email)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: Client, obj_in: ClientUpdate) -> Client:
        """Actualizeaza atributele unui client existent."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id_client: int) -> Optional[Client]:
        """È˜terge un client din sistem."""
        db_obj = self.get_by_id(id_client)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
        return db_obj

