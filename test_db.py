"""
Script de fortare structura tranzactionala in Neon Cloud (PostgreSQL).
Creeaza chirurgical tabela 'comenzi_lumanari' si listeaza nomenclatorul final.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("PROD_DATABASE_URL") or os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("postgresql+asyncpg"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("\nâš¡ --- EXECUTARE SCRIPT CHIRURGICAL SQL ---")

        # Trimitem direct comanda nativa de creare a tabelei lipsa in Neon Cloud
        create_table_query = text("""
            CREATE TABLE IF NOT EXISTS comenzi_lumanari (
                id SERIAL PRIMARY KEY,
                id_comanda INTEGER NOT NULL,
                id_lumanare INTEGER NOT NULL,
                cantitate INTEGER NOT NULL,
                pret_salvat FLOAT NOT NULL,
                CONSTRAINT fk_comenzi_lumanari_id_comanda
                    FOREIGN KEY (id_comanda)
                    REFERENCES comenzi(id_comanda)
                    ON DELETE CASCADE
            );
        """)
        connection.execute(create_table_query)

        # Generam si indexul pe care il cauta sistemul
        create_index_query = text("""
            CREATE INDEX IF NOT EXISTS ix_comenzi_lumanari_id
            ON comenzi_lumanari (id);
        """)
        connection.execute(create_index_query)

        # Salvam definitiv modificarea in AWS Neon Cloud
        connection.commit()
        print("âœ… Tabela 'comenzi_lumanari' a fost creata direct pe serverul Cloud!")

        print("\nðŸ—‚ï¸ --- LISTA ACTUALIZATÄ‚ A TABELEROR ACTIVE ---")
        query_list = text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tabele = connection.execute(query_list).scalars().all()

        print("âœ… Structura curenta din Neon DB:")
        for t in tabele:
            print(f"   â–ªï¸ {t}")

except Exception as e:
    print(f"âŒ Eroare in timpul executiei: {str(e)}")

