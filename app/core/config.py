"""
Modul de configurare centralizat pentru platforma Light Infinity AI.
ÃŽncarca si valideaza variabilele de mediu necesare functionarii backend-ului.
"""

import os
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# ÃŽncarcam corect si curat fisierul .env aflat in radacina proiectului
load_dotenv()


class Settings(BaseSettings):
    """
    Clasa de configurare bazata pe Pydantic v2 pentru validarea datelor de intrare.
    Protejeaza cheile secrete impotriva scurgerilor accidentale in loguri.
    """

    PROJECT_NAME: str = "Light Infinity AI - Enterprise"
    RUN_ENV: str = Field(default="dev")

    # Prefixul global pentru rutele API cerut de suitele de testare automate
    API_V1_STR: str = "/api/v1"

    # Configuratii Baze de Date (Local vs Productie Cloud)
    DATABASE_URL: str = Field(default="sqlite:///./light_infinity_dev.db")
    PROD_DATABASE_URL: str = Field(default="")

    # Securitate Nucleu JWT (Fortam lipsa unui fallback hardcodat in productie)
    # Folosim SecretStr pentru ca valoarea sa nu apara niciodata textual in loguri sau print-uri
    JWT_SECRET_KEY: SecretStr = Field(
        default=os.getenv("JWT_SECRET_KEY") or "PRODUCE_CRASH_IF_PROD_AND_MISSING"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def get_db_url(self) -> str:
        """Returneaza URL-ul corect al bazei de date in functie de mediu."""
        if self.RUN_ENV.lower() == "prod":
            if not self.PROD_DATABASE_URL or self.PROD_DATABASE_URL == "":
                raise ValueError(
                    "PROD_DATABASE_URL nu este configurata in mediu de productie!"
                )
            return self.PROD_DATABASE_URL
        return self.DATABASE_URL

    # Corectie Pydantic v2: Trecerea de la clasa Config la modelul modern de configurare
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore",  # Ignora alte variabile din .env care nu sunt mapate in clasa
    )


# Instantiere si validare imediata la pornirea aplicatiei
settings = Settings()

# Verificare de siguranta la nivel de productie
if (
    settings.RUN_ENV.lower() == "prod"
    and settings.JWT_SECRET_KEY.get_secret_value()
    == "PRODUCE_CRASH_IF_PROD_AND_MISSING"
):
    raise ValueError(
        "CRITICAL SECURITY ERROR: JWT_SECRET_KEY trebuie definita in fisierul .env in mediul de productie!"
    )

