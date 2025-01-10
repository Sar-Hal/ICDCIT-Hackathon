import fitz
import requests
import json
import os
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def extract_pdf_content(pdf_path):
    """Extract text from PDF."""
    pdf = fitz.open(pdf_path)
    text_content = ""
    
    for page_number in range(len(pdf)):
        page = pdf[page_number]
        text_content += page.get_text() + "\n"
        print(f"Processed page {page_number + 1}/{len(pdf)}")
    
    return text_content

def clean_text(text):
    """Clean the text by removing empty lines."""
    return "\n".join([line for line in text.splitlines() if line.strip() != ""])

def split_text(text, max_tokens=1500):
    """Split text into smaller chunks."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        word_length = len(word) // 4
        if current_length + word_length > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def query_groq_llm(prompt, context, max_tokens=500):
    """Query Groq LLM API."""
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [
                {"role": "system", "content": "You are an assistant helping summarize educational content."},
                {"role": "user", "content": f"{prompt}\n\nContext:\n{context}"}
            ],
            "model": "llama-3.3-70b-versatile",
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")
        else:
            print(f"Groq API Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def process_pdf_to_summary(pdf_path, output_path):
    """Main function to process PDF and generate summary."""
    print(f"Processing PDF: {pdf_path}")
    
    # Extract text from PDF
    text_content = extract_pdf_content(pdf_path)
    
    # Clean text
    cleaned_text = clean_text(text_content)
    
    # Split into chunks
    chunks = split_text(cleaned_text)
    print(f"Split text into {len(chunks)} chunks")
    
    # Process each chunk
    summarized_text = ""
    user_query = "Extract and summarize the main educational concepts and key points from this text. Focus on core ideas, definitions, and important relationships."
    
    for i, chunk in enumerate(chunks, 1):
        print(f"\nProcessing chunk {i}/{len(chunks)}...")
        
        # Try up to 3 times
        for attempt in range(3):
            response = query_groq_llm(user_query, chunk)
            if response:
                summarized_text += f"\n=== Section {i} ===\n" + response + "\n"
                break
            print(f"Attempt {attempt + 1} failed, retrying...")
            
    # Save final summary
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summarized_text)
    
    print(f"\nSummary saved to: {output_path}")

if __name__ == "__main__":
    input_pdf = "Minimization_Final_Version\BIOSENSOR.pdf"
    output_file = "final_summary.txt"
    process_pdf_to_summary(input_pdf, output_file)