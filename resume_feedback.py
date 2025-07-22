import requests

def get_resume_feedback(resume_text, api_key):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [
            {
                "role": "user",
                "content": f"You're a resume expert. Give improvements for:\n\n{resume_text[:3000]}"
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        st.write("📦 API Status:", response.status_code)
        st.write("📝 Response Preview:", response.text[:300])
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"❌ API error: {e}")
        return "No response."
