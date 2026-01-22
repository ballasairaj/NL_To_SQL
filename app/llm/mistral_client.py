import requests
from app.config import MISTRAL_API_KEY

URL = "https://api.mistral.ai/v1/chat/completions"

def call_mistral(prompt: str):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-large-2512",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    res = requests.post(URL, json=payload, headers=headers)
    return res.json()["choices"][0]["message"]["content"]
