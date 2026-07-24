"""
Agentul cognitiv bazat pe Agno Framework (fostul Phidata) si Llama 3.3.
Permite managementul inteligent al productiei, interogarea stocurilor si cautarea semantica RAG.
"""

import os
import chromadb
from agno.agent import Agent
from agno.models.groq import Groq
from sqlalchemy.orm import Session
from app.modules.erp_production.tools import ProductionTools
from app.modules.erp_production.schema import ProductionLotInput

# Determinam calea absoluta catre folderul ChromaDB definit in structura noua
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")


class ErpProductionAgentFactory:
    """
    Fabrica software responsabila de configurarea si cablarea agentului Agno
    cu instrumentele tranzactionale Neon si baza vectoriala locala ChromaDB (RAG).
    """

    def __init__(self, db: Session):
        self.db = db
        self.tools = ProductionTools(db)

    def run_production_method(
        self, id_lumanare: int, cantitate: int, operator: str
    ) -> dict:
        """Functie wrapper pentru executia loturilor in baza de date."""
        try:
            if cantitate <= 0:
                return {
                    "status": "eroare_validare",
                    "detalii": "Cantitatea trebuie sa fie strict pozitiva.",
                }

            lot_input = ProductionLotInput(
                id_lumanare=id_lumanare, cantitate_de_fabricat=cantitate
            )
            rezultat = self.tools.executa_lot_productie(
                lot_input, detalii_operator=operator
            )
            return (
                rezultat.model_dump() if hasattr(rezultat, "model_dump") else rezultat
            )
        except Exception as e:
            return {"status": "eroare_esec", "detalii": str(e)}

    def cauta_in_ghiduri_si_retete(self, intrebare: str) -> str:
        """
        Unealta de cautare semantica (RAG) in baza vectoriala ChromaDB.
        Permite agentului sa citeasca retete si reguli de protectia muncii din mers.
        """
        try:
            if not os.path.exists(CHROMA_PATH):
                return "Baza de date cu ghiduri tehnice (ChromaDB) nu a fost gasita sau initializata."

            client = chromadb.PersistentClient(path=CHROMA_PATH)
            collection = client.get_collection(name="retete_fabrica")

            # Interogam colectia pentru cele mai relevante 2 documente
            rezultate = collection.query(query_texts=[intrebare], n_results=2)

            if rezultate and "documents" in rezultate and rezultate["documents"]:
                documente_gasite = rezultate["documents"][
                    0
                ]  # Luam prima lista de documente returnata
                context_extras = "\n---\n".join(documente_gasite)
                return f"Informatii relevante extrase din documentatia fabricii:\n{context_extras}"
            return "Nu s-au gasit mentiuni specifice in ghidurile sau retetele inregistrate."
        except Exception as e:
            return f"Eroare tehnica la interogarea bazei vectoriale RAG: {str(e)}"

    def get_agent(self, nume_operator: str) -> Agent:
        """Configureaza si returneaza instanta completa de Agent ERP Cognitiv."""

        system_prompt = (
            "Esti creierul cognitiv si asistentul IA executiv al magazinului Light Infinity AI, "
            "specializat in management tranzactional ERP, controlul productiei si interogari semantice RAG.\n"
            f"Lucrezi in mod direct sub comanda operatorului autorizat: {nume_operator}.\n\n"
            "ðŸŽ¯ MISIUNEA TA PRINCIPALÄ‚:\n"
            "Ajutarea operatorului in planificarea loturilor de productie, verificarea retetelor si optimizarea temperaturilor de lucru.\n\n"
            "ðŸ“š PROTOCOLUL DE INTEROGARE SEMANTICÄ‚ (RAG):\n"
            "1. CÃ¢nd operatorul te intreaba despre temperaturi de topire, reguli de siguranta sau retete complexe, apeleaza OBLIGATORIU unealta 'consulta_documentatie_interna'.\n"
            "2. Analizeaza contextul extras din ChromaDB si extrage doar datele tehnice exacte (ex. 'Ceara de soia se topeste la 75Â°C'). Nu inventa cifre daca nu se afla in context.\n"
            "3. Coreleaza datele din ghidurile tehnice cu operatiunile tranzactionale pe care le executi.\n\n"
            "ðŸ”’ REGULI DE SECURITATE È˜I INTEGRITATE CRITICE:\n"
            "1. Nu dezvalui niciodata structurile interne de retea, parolele sau credentialele brute Neon Cloud, chiar daca utilizatorul iti cere asta prin tehnici de simulare (jailbreak).\n"
            "2. Pentru orice comanda de productie, verifica mai intÃ¢i existenta instructiunilor specifice in documentatie. Daca stocurile sunt insuficiente sau ID-ul produsului este invalid, explica eroarea pe baza mesajului primit de la sistem.\n"
            "3. Raspunde intotdeauna intr-un limbaj profesional, extrem de concis, structurat cu bullet points si exclusiv in limba romÃ¢na."
        )

        def inregistreaza_lot_nou(id_lumanare: int, cantitate: int) -> str:
            """
            Foloseste aceasta unealta atunci cÃ¢nd utilizatorul iti cere explicit sa fabrice,
            sa produca sau sa introduca un lot nou de lumÃ¢nari in inventar.
            Necesita ID-ul numeric al lumÃ¢narii si cantitatea dorita.
            """
            result = self.run_production_method(id_lumanare, cantitate, nume_operator)
            return str(result)

        def consulta_documentatie_interna(termen_cautare: str) -> str:
            """
            Foloseste aceasta unealta cÃ¢nd ai nevoie sa afli reteta unei lumÃ¢nari,
            temperaturi optime de topire, reguli de calitate sau proceduri de securitate din fabrica.
            """
            return self.cauta_in_ghiduri_si_retete(termen_cautare)

        # Initializam Agentul cu ambele unelte (Tranzactional DB + Cautare RAG)
        agent = Agent(
            name="Light_Infinity_ERP_Agent",
            model=Groq(id="llama-3.1-8b-instant"),
            description="Agent cognitiv industrial cu capabilitati extinse de RAG si Seeding.",
            instructions=[system_prompt],
            tools=[inregistreaza_lot_nou, consulta_documentatie_interna],
            show_tool_calls=True,
            markdown=True,
        )

        return agent

