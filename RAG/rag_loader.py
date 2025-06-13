import json
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_docs(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    documents = []
    for item in data:
        content = item['content']
        metadata = {
            "id": item["id"],
            "title": item["title"],
            "date": item["updated_on"],
        }
        documents.append(Document(page_content=content, metadata=metadata))

    return documents

def chunk_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)
    return chunks