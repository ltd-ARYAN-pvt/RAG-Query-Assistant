import google.genai as genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"Error initializing Google Generative AI client: {e}")
    client = None

def generate_response(prompt: str, model: str = "gemini-2.0-flash-001") -> str:
    if client is None:
        raise RuntimeError("Google Generative AI client is not initialized.")

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=4000, # Set your desired maximum output tokens here
                temperature=0.2,        # You can also include other parameters like temperature
                top_p=0.9,              # and top_p for generation control
                top_k=40
            )
        )
        # print(f"Response from model {model}: {response.text}")
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "An error occurred while generating the response."
    
if __name__ == "__main__":
    # Example usage
    prompt = "What is the difference between gemini-2.0-flash vs 2.5-flash? in point form"
    response = generate_response(prompt)
    print(f"Response: {response}")