from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    fullname: Optional[str] = Field(None, alias="full_name")
    role: Optional[str] = "customer"

    model_config = {
        "populate_by_name": True  # Permite Pydantic sa accepte si full_name si fullname
    }


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    fullname: Optional[str]
    role: str
    is_active: bool

    class Config:
        from_attributes = True


# --- MODELELE SOLICITATE DE ROUTER PENTRU JWT ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

