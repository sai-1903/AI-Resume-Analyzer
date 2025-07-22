import requests

API_KEY = input("🔐 Enter your OpenRouter API key (org-...): ")

response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://github.com/sai-1903/sai-1903",
    }
)

if response.status_code == 200:
    data = response.json()
    print("✅ Available Models:")
    for model in data.get("models", []):
        print(" •", model)
else:
    print("❌ Error listing models:", response.status_code, response.text)
