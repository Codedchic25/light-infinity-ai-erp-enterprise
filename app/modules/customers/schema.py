from pydantic import BaseModel


class ClientCreate(BaseModel):
    nume: str
    telefon: str
    email: str

