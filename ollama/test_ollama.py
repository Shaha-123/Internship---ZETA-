import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "mistral",
        "prompt": "Say OK",
        "stream": False
    }
)

print(response.json()["response"])
