import requests
import json

# API endpoint
url = "https://api.groq.com/openai/v1/chat/completions"

# Your Groq API key
api_key = "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"

# Headers for the request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# Payload for the request
payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    "max_tokens": 100,  # Limit the response length
    "temperature": 0.7,  # Adjust randomness
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Handle the response
if response.status_code == 200:
    response_data = response.json()
    print("Chat Completion Response:")
    print(response_data["choices"][0]["message"]["content"])
else:
    print(f"Error: {response.status_code} - {response.text}")
