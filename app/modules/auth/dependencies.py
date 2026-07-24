"""
Dependente de Securitate si Autentificare pentru Light Infinity AI.
Valideaza si decodeaza asamblarile JWT trimise de frontend-uri catre FastAPI.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.modules.auth.model import User

# Schema OAuth2 indica endpoint-ul de login pentru generarea token-urilor Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    Decodifica si valideaza token-ul JWT primit in header-ul cererii HTTP.
    Extrage utilizatorul live din DB sau arunca exceptii controlate 401.
    """
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentiale invalide sau token de acces expirat.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # COREKT SECURITY REBUILD: Extragem valoarea string curata din obiectul SecretStr
        # Acest pas elimina eroarea JWKError aruncata de libraria python-jose.
        secret_key = settings.JWT_SECRET_KEY.get_secret_value()

        payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise cred_exception

    except JWTError:
        raise cred_exception

    # Cautam utilizatorul in baza de date activa
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise cred_exception

    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependenta suplimentara (Gatekeeper RBAC): Verifica daca utilizatorul
    autentificat detine rolul de administrator pentru accesul la BI / RAG.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acces interzis! Aceasta actiune necesita privilegii de administrator.",
        )
    return current_user

