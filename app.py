import gradio as gr
import requests

# FastAPI backend URL
API_URL = "http://localhost:8000/rag/query"  # Update if deploying

def ask_question(user_question):
    try:
        response = requests.post(API_URL, json={"question": user_question})
        if response.status_code == 200:
            return response.json().get("answer")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"

# Gradio interface with Markdown output
iface = gr.Interface(
    fn=ask_question,
    inputs=gr.Textbox(lines=2, placeholder="Ask a question based on historical data..."),
    outputs=gr.Markdown(),  # Render as Markdown
    title="📚 RAG-Based Historical Q&A",
    description="Ask any question. The system will answer only if the answer exists in the historical data. Responses are displayed in rich Markdown format."
)

if __name__ == "__main__":
    iface.launch()
