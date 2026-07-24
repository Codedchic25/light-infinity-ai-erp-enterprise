import os
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    if os.getenv("ENVIRONMENT") == "production":
        raise ValueError(
            "CRITICAL: JWT_SECRET_KEY must be set in production environment!"
        )
    SECRET_KEY = "super_secret_key_change_me_in_production_1234567890"

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


class JWTManager:
    @staticmethod
    def create_access_token(data: dict) -> str:
        """Genereaza un token JWT semnat digital."""
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> dict | None:
        """Valideaza tokenul si extrage datele utilizatorului."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload if payload.get("sub") else None
        except JWTError:
            return None

