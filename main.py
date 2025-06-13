from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from RAG.rag_vector_store import load_vector_store, create_vector_store
from RAG.rag_retriever import retrieve_and_generate
from RAG.rag_loader import load_docs, chunk_documents
import os

app = FastAPI()

# Enable CORS for all origins (for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = None  # Global store

@app.on_event("startup")
def load_vector_db():
    global vector_store
    try:
        print("🔄 Checking for existing Chroma DB...")
        if os.path.exists("./chroma_db") and len(os.listdir("./chroma_db")) > 0:
            print("📂 Found existing Chroma DB, loading it...")
            vector_store = load_vector_store()
        else:
            print("🆕 No existing DB found. Creating new vector store...")
            docs = load_docs("docs/rag_index.json")
            chunks = chunk_documents(docs)
            vector_store = create_vector_store(chunks)
        print("✅ Vector store ready!")
    except Exception as e:
        print(f"❌ Error loading vector store: {e}")

class QueryRequest(BaseModel):
    question: str

@app.post("/rag/query")
async def rag_query(request: QueryRequest):
    try:
        answer = retrieve_and_generate(request.question, vector_store)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
