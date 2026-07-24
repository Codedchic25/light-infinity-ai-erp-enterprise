"""
Script de populare (seeding) pentru baza de date vectoriala locala ChromaDB.
Asigura persistenta documentelor folosite de sistemul RAG (Cautare Semantica).
"""

import os
import chromadb
from dotenv import load_dotenv

# ÃŽncarcam variabilele globale
load_dotenv()

# Definim calea absoluta catre folderul global din radacina proiectului
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")


def run_rag_seeding():
    print(f"ðŸ“‚ Initializare baza vectoriala ChromaDB in locatia sigura: {CHROMA_PATH}")
    os.makedirs(CHROMA_PATH, exist_ok=True)

    # Conexiune persistenta securizata la nivel de radacina proiect
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        chroma_client.delete_collection(name="retete_fabrica")
        print("â™»ï¸ Colectia veche 'retete_fabrica' a fost curatata.")
    except Exception:
        pass

    collection = chroma_client.create_collection(name="retete_fabrica")

    print(
        "ðŸ“ Adaugare retete si ghiduri operationale industriale in pipeline-ul RAG..."
    )
    retete = [
        "Reteta LumÃ¢nare Relaxare: Necesita 85% Ceara de Soia premium, 10% Parfum de Lavanda natural, topire la 68 grade Celsius si turnare lenta in Pahar Sticla Mov.",
        "Procedura de Securitate Fabrica: Temperatura in depozitul de ceara nu trebuie sa depaseasca 25 de grade Celsius pentru a preveni degradarea structurala a materiei prime.",
        "Ghid Calitate: Fiecare lot de lumÃ¢nari turnate trebuie lasat la maturat timp de minimum 48 de ore inainte de ambalare si etichetare cod SKU.",
    ]

    ids = ["id_reteta_01", "id_reteta_02", "id_reteta_03"]
    metadate = [{"tip": "reteta"}, {"tip": "protectia_muncii"}, {"tip": "calitate"}]

    # Inserare sincronizata cu metadate pentru filtrare avansata ulterioara
    collection.add(documents=retete, metadatas=metadate, ids=ids)
    print(
        "âœ… Seed RAG & ChromaDB finalizat cu succes! Documentele sunt persistate global."
    )


if __name__ == "__main__":
    run_rag_seeding()

