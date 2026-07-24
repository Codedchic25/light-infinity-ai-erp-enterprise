import os
import pandas as pd
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.groq import Groq
from sqlalchemy.orm import Session
import chromadb
from app.db.session import SessionLocal
from app.modules.catalog.model import Lumanare


class RaportStocIn(BaseModel):
    fara_filtru: bool = Field(
        True, description="Folosit doar pentru structura JSON interna."
    )


class AnalizaBIIn(BaseModel):
    rulare_statistici: bool = Field(
        True, description="Folosit doar pentru structura JSON interna."
    )


class InterogareRAGIn(BaseModel):
    intrebare: str = Field(..., description="Textul intrebarii tehnice din manuale.")


def interogheaza_stocuri_reale(parametri: RaportStocIn) -> str:
    db: Session = SessionLocal()
    try:
        produse = db.query(Lumanare).all()
        if not produse:
            return "Nu s-au gasit lumanari in baza de date."
        rap = "=== RAPORT STOCURI ===\n"
        for p in produse:
            rap += f"- SKU: {p.sku} | Nume: {p.nume} | Stoc: {p.stoc} buc\n"
        return rap
    finally:
        db.close()


def detecteaza_anomalii_si_statistici(parametri: AnalizaBIIn) -> str:
    db: Session = SessionLocal()
    try:
        produse = db.query(Lumanare).all()
        if not produse:
            return "Date insuficiente."
        df = pd.DataFrame(
            [
                {"sku": p.sku, "nume": p.nume, "stoc": p.stoc, "pret": p.pret}
                for p in produse
            ]
        )
        stoc_mediu = df["stoc"].mean()
        val_inv = (df["stoc"] * df["pret"]).sum()
        stoc_critic_df = df[df["stoc"] < 10]

        if not stoc_critic_df.empty:
            alerte = "\nâš ï¸ ANOMALII DETECTATE:\n"
            for _, r in stoc_critic_df.iterrows():
                alerte += f"- {r['nume']} are doar {r['stoc']} unitati!\n"
        else:
            alerte = "\nâœ… Stocuri in parametri normali.\n"

        return f"=== ANALIZA BI ===\n- Total SKU: {len(df)}\n- Stoc mediu: {stoc_mediu:.1f}\n- Valoare: {val_inv:,.2f} RON{alerte}"
    finally:
        db.close()


def interogheaza_retete_vectoriale(parametri: InterogareRAGIn) -> str:
    try:
        if not os.path.exists("./data/chromadb"):
            return "ChromaDB neinitializat."
        cc = chromadb.PersistentClient(path="./data/chromadb")
        col = cc.get_collection(name="retete_fabrica")
        rez = col.query(query_texts=[parametri.intrebare], n_results=1)
        if rez.get("documents"):
            return f"Informatii din manuale: {rez.get('documents')}"
        return "Nu s-au gasit date relevante in manualele fabricii."
    except Exception as e:
        return f"Eroare RAG: {str(e)}"


agent_cognitiv = Agent(
    model=Groq(id="llama-3.1-8b-instant"),
    instructions=[
        "Esti creierul cognitiv al platformei Light Infinity AI.",
        "Raspunde intotdeauna profesional, direct, in limba romana.",
        "Misiunea ta principala este sa analizezi situatiile complexe din fabrica.",
        "Daca detectezi un produs cu stoc critic folosind uneltele analitice, coreleaza automat situatia cu reteta sa tehnica din `interogheaza_retete_vectoriale` pentru a explica managerilor ce materii prime trebuie comandate urgent de la furnizori.",
        "Nu povesti ce unelte folosesti. Afiseaza direct raportul rafinat final in format Markdown.",
    ],
    tools=[
        interogheaza_stocuri_reale,
        detecteaza_anomalii_si_statistici,
        interogheaza_retete_vectoriale,
    ],
    markdown=True,
)

if __name__ == "__main__":
    agent_cognitiv.print_response(
        "Verifica daca avem anomalii de stoc si spune-mi ce instructiuni de calitate sau reteta are acel produs afectat."
    )

