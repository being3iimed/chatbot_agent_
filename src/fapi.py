import sys
package = __import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from setup import CrewaiConversationalChatbotCrew

app = FastAPI(title="ISIKlub Chatbot API")

# Optional: allow frontend calls from any domain (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crew = CrewaiConversationalChatbotCrew().crew()


class ChatRequest(BaseModel):
    user_message: str


class ChatResponse(BaseModel):
    assistant_message: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = crew.kickoff(inputs={"user_message": request.user_message})
        return ChatResponse(assistant_message=result.raw.strip('"'))
    except Exception as e:
        return ChatResponse(assistant_message=f"Une erreur est survenue : {str(e)}")
