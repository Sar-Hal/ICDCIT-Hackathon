import requests

# Set your Groq API key
groq_api_key = "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"

def generate_question_and_distractors(text):
    # Define the API endpoint
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Define the headers for the request
    headers = {
        'Authorization': f'Bearer {groq_api_key}',
        'Content-Type': 'application/json'
    }

    # Define the payload for the request
    payload = {
        "messages": [
            {"role": "system", "content": "You are an educational content summarizer."},
            {"role": "user", "content": f"Generate a multiple-choice question based on the following text:\n\n{text}"}
        ],
        "model": "llama-3.3-70b-versatile",
        "max_tokens": 500,
        "temperature": 0.7
    }

    # Make the POST request to the API
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        completion_data = response.json()
        question = completion_data.get('choices', [{}])[0].get('text', '').strip()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Groq API: {e}")
        return None, None, None  # Return gracefully in case of an error

    # Step 2: Generate distractors (for demonstration purposes, just a basic example)
    words = text.split()
    correct_answer = words[0]  # Assume the first word is the correct answer (simplified)
    distractors = words[1:4]  # Take the next three words as distractors (replace with better logic)

    # Ensure we have enough distractors
    while len(distractors) < 3:
        distractors.append("Random Answer")

    distractors = distractors[:3]

    # Combine options
    options = distractors + [correct_answer]
    random.shuffle(options)

    return question, options, correct_answer

# Example usage
text = "Albert Einstein was born in Ulm, Germany, in 1879. He was a theoretical physicist who developed the theory of relativity."
question, options, correct_answer = generate_question_and_distractors(text)

if question:
    print(f"Question: {question}")
    print(f"Options: {options}")
    print(f"Correct Answer: {correct_answer}")
else:
    print("Failed to generate question due to connection issues.")