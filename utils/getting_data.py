import requests
import json
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()   

# Step 1: API Call
url = os.getenv('Api')  # Replace with your API URL
if not url:
    raise ValueError("API_URL not set in .env file")
username = os.getenv('Login')  # Replace with your API username
if not username:
    raise ValueError("API_USERNAME not set in .env file")
password = os.getenv('Pass')  # Replace with your API password
if not password:
    raise ValueError("API_PASSWORD not set in .env file")

response = requests.get(url, auth=HTTPBasicAuth(username, password))

if response.status_code == 200:
    # Step 2: Save Full JSON
    full_data = response.json()
    with open('docs/history_data.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)

    # Step 3: Extract Necessary Fields and Clean HTML
    simplified_data = []
    for item in full_data.get('result', []):
        raw_html = item.get('text', '')
        clean_text = BeautifulSoup(raw_html, 'html.parser').get_text(separator=' ', strip=True)

        simplified_data.append({
            'id': item.get('sys_id'),
            'title': item.get('short_description'),
            'content': clean_text,  # Cleaned text without HTML tags
            'author': item.get('sys_created_by'),
            'created_on': item.get('sys_created_on'),
            'updated_on': item.get('sys_updated_on')
        })

    # Step 4: Save Clean JSON for RAG
    with open('docs/rag_index.json', 'w', encoding='utf-8') as f:
        json.dump(simplified_data, f, ensure_ascii=False, indent=4)

    print("✅ Files saved successfully and HTML cleaned!")
else:
    print(f"❌ Failed to fetch data: {response.status_code} - {response.text}")
