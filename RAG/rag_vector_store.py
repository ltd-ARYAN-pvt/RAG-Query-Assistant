from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

def create_vector_store(chunks, persist_directory="./chroma_db"):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    return vector_store

def load_vector_store(persist_directory="./chroma_db"):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)
