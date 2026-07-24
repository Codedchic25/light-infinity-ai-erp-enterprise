from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.security.jwt import JWTManager

# Indica ruta de unde se extrage token-ul securizat
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")


class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, token: str = Depends(oauth2_scheme)) -> dict:
        payload = JWTManager.verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalid sau expirat",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_role = payload.get("role")
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acces interzis. Aceasta actiune necesita unul din rolurile: {self.allowed_roles}",
            )
        return payload

