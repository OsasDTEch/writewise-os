from dotenv import load_dotenv
import asyncio
import os

# 🛠 Fix: Ensure there's a running event loop
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from scrapping import scrape_appwrite_docs

load_dotenv()

# 🔧 Create the embedding object after event loop is ensured
embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# 🧠 Scrape content
documents = scrape_appwrite_docs()

# ✂️ Split into manageable chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)
print(f"Splitted into {len(chunks)} chunks")

# 🧲 Build and save FAISS vector store
vectorstore = FAISS.from_documents(chunks, embedding)
vectorstore.save_local("data/faiss_index")
print("✅ FAISS index saved to 'data/faiss_index'")
