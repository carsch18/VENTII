import requests
import json

API_KEY = "csk-d45v9f85n3k98tf89m5e6rfrh5dtnk6r9pn3j5fkmhe2wy43"

# Test chat completion
url = "https://api.cerebras.ai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
data = {
    "model": "llama3.1-8b",
    "messages": [{"role": "user", "content": "Say 'API working!' in 3 words"}],
    "max_tokens": 10
}

print("Testing Cerebras API...")
response = requests.post(url, headers=headers, json=data)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"✓ API Working!")
    print(f"Response: {result['choices'][0]['message']['content']}")
else:
    print(f"✗ Error: {response.text}")
