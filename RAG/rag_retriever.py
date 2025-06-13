from langchain.prompts import PromptTemplate
from RAG.rag_llm import generate_response

# --- Prompt Template ---
template = """
You are a knowledgeable assistant with access to historical query data from database.
Your task is to search ONLY within the provided historical context and answer the user's question as accurately and concisely as possible.

Instructions:
- If the answer is found in the provided context, answer the question directly.
- If the answer is NOT available in the provided context, explicitly reply: "Based on the provided historical data, I do not have an answer to this question."
- Try to mention metadata like the date or author if relevant to the answer.
- Try to provide points for non-technical users, and avoid technical jargon.

Historical Data:
{context}

User Question:
{question}

Answer:
"""


prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

def retrieve_and_generate(query, vector_store, k=3):
    retrieved_docs = vector_store.similarity_search(query, k=k)
    context = "\n\n".join([
        f"Title: {doc.metadata.get('title')}\nDate: {doc.metadata.get('date')}\nContent: {doc.page_content}"
        for doc in retrieved_docs
    ])
    if not context:
        return "Based on the provided historical data, I do not have an answer to this question."
    prompt = prompt_template.format(context=context, question=query)

    # print(prompt)
    # Generate response using the LLM
    response = generate_response(prompt)

    return response
