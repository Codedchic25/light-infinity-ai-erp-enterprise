import os
from collections.abc import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

load_dotenv()

RUN_ENV = os.getenv("RUN_ENV", "dev").lower()

if RUN_ENV == "prod":
    DATABASE_URL = os.getenv("PROD_DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("PROD_DATABASE_URL nu este configurata in mediu!")

    # Optimizari stricte pentru pooling-ul Serverless din Neon Cloud
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Elimina erorile de conexiuni inchise de Neon
        pool_recycle=300,  # Recicleaza conexiunile vechi la 5 minute
    )
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./light_infinity_dev.db")
    connect_args = (
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    )
    engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency Injection FastAPI cu inchidere garantata a conexiunii.
    Tipizarea explicita [Session, None, None] asigura autocompletion in rute.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Asigura returnarea conexiunii in pool indiferent de erori

