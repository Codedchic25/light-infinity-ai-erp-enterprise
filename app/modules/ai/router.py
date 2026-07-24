import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from app.modules.ai.agent import agent_cognitiv

# Forțăm citirea securizată a cheii Groq înainte de execuția agentului Agno
load_dotenv()

# Eliminăm prefixul "/ai" din router pentru a se alinia corect cu maparea globală din main.py
router = APIRouter(tags=["AI Cognitive"])


# Aliniem denumirea cheii primite cu cea trimisă de dashboard.py
class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str
    status: str


@router.post("/ai/chat", response_model=ChatResponse)
async def chat_with_agent(payload: ChatRequest):
    """
    Ruta oficială cognitivă.
    Sincronizează interfața Streamlit cu instanța oficială Agno Framework.
    """
    cheie_api = os.getenv("GROQ_API_KEY")
    if not cheie_api or cheie_api.startswith("gsk_pune"):
        raise HTTPException(
            status_code=401,
            detail="EROARE CRITICĂ: GROQ_API_KEY nu este configurată sau este invalidă în .env.",
        )

    try:
        # Apelăm instanța oficială din Agno Framework folosind promptul aliniat
        response_agent = agent_cognitiv.run(payload.prompt)

        # Extragere inteligentă a textului indiferent de structura internă a obiectului Agno
        text_raspuns = (
            response_agent.content
            if hasattr(response_agent, "content")
            else str(response_agent)
        )

        return ChatResponse(response=text_raspuns, status="success")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Eroare procesare Agent AI (Agno): {str(e)}"
        )

