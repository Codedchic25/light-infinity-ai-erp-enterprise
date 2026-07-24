from agno.agent import Agent
from agno.models.groq import Groq
from app.modules.ai.schema import ChatRequest, ChatResponse


class AIService:
    def __init__(self):
        # Definim agentul eliminÃ¢nd parametrul problematic show_tool_calls
        self.agent = Agent(
            model=Groq(id="llama-3.1-8b-instant"),
            markdown=True,
            description="Asistent Cognitiv Enterprise pentru platforma Light Infinity AI.",
        )

    async def process_chat(self, payload: ChatRequest) -> ChatResponse:
        try:
            # Rulam agentul Agno si preluam raspunsul sub forma de text
            run_response = self.agent.run(payload.message)
            return ChatResponse(status="success", response=run_response.content)
        except Exception as e:
            return ChatResponse(
                status="error", response=f"Eroare procesare AI backend: {str(e)}"
            )


ai_service = AIService()

