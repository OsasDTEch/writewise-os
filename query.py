import os

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Any

from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_anthropic import ChatAnthropic
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
model = ChatAnthropic(model='claude-3-opus-20240229', anthropic_api_key=os.getenv('CLAUDE_APIKEY'))
embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

class GraphState(TypedDict):
    query: str
    chat_history: List[Any]
    question: str
    docs: List[Any]
    answer: str

def retrieve(state: GraphState) -> GraphState:
    # Safe deserialization enabled – make sure you trust the source
    db = FAISS.load_local('./data/faiss_index', embedding, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()
    docs = retriever.invoke(state['query'])
    return {
        **state,
        'docs': [doc.page_content for doc in docs]
    }



def generate_answer(state: GraphState) -> GraphState:
    context = "\n".join(state['docs'])

    # Add chat history to prompt for context
    chat_context = ""
    if state.get('chat_history'):
        recent_chat = state['chat_history'][-4:]  # Last 2 exchanges
        chat_context = "\n".join([f"{speaker}: {msg}" for speaker, msg in recent_chat])
        chat_context = f"\nPrevious conversation:\n{chat_context}\n"

    prompt = f"Context from Appwrite docs:\n{context}\n{chat_context}\nCurrent question: {state['query']}\n\nProvide a helpful answer:"

    response = llm.invoke(prompt)

    chat_log = state.get("chat_history", [])
    chat_log.append(("You", state['query']))
    chat_log.append(("WriteWise", response.content))  # Changed to WriteWise!

    return {
        **state,
        "answer": response.content,
        "chat_history": chat_log
    }

builder = StateGraph(GraphState)
builder.add_node('retriever', retrieve)
builder.add_node('answer_generator', generate_answer)
builder.set_entry_point('retriever')
builder.add_edge('retriever', 'answer_generator')
builder.add_edge('answer_generator', END)

app = builder.compile()
