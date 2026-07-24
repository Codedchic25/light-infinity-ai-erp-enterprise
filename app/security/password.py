from typing import Optional
import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica daca o parola in format text simplu corespunde hash-ului din baza de date."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Genereaza o amprenta criptografica Bcrypt nativa pentru o parola."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

