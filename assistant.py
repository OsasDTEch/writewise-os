from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Any
from query import app  # This is your LangChain app

class AskRequest(BaseModel):
    query: str
    chat_history: List[Any]

api = FastAPI()

@api.post("/ask")
async def ask(request: AskRequest):
    state = {
        "query": request.query,
        "chat_history": request.chat_history,
        "question": request.query,
        "docs": [],
        "answer": ""
    }
    result = app.invoke(state)
    return result
