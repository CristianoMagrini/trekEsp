import json
import requests

OLLAMA_SERVER_URL="https://api-chat.sitai.duckdns.org/api/generate"
MODEL_NAME="llama3.1"
PROMPT_TEXT="Dammi le coordinate di bergamo. Rispondi sempre e solo con le coordinate in formato: 12.34, 56.235"

payload={
    "model": MODEL_NAME,
    "prompt": PROMPT_TEXT,
    "stream": False
}

response = requests.post(OLLAMA_SERVER_URL, json=payload)

if response.status_code == 200:
    data = response.json()
    print(data["response"])
else:
    print("Errore: ", response.status_code, response.text)

