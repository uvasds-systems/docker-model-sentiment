import os
import requests
import json

# The file to analyze - this should be mounted as a volume in a real scenario
FILE_PATH = "input_text.txt" 
LLM_URL = os.environ.get("LLM_URL", "http://docker.internal")
MODEL_NAME = os.environ.get("LLM_MODEL", "llm") # Using the alias from compose file

def get_sentiment(text):
    """Sends text to the model runner API for sentiment analysis."""
    headers = {
        "Content-Type": "application/json"
    }
    # Using an explicit prompt to guide the general-purpose LLM using standard OpenAI API format
    prompt = f"Analyze the following text for sentiment and provide a single word answer: 'Positive', 'Negative', or 'Neutral'. Text: {text}"
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 50,
        "temperature": 0.1
    }

    try:
        response = requests.post(f"{LLM_URL}/chat/completions", headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        sentiment = result['choices'][0]['message']['content'].strip()
        print(f"Sentiment: {sentiment}")
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the model API: {e}")

if __name__ == "__main__":
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as f:
            content = f.read()
        if content:
            get_sentiment(content)
        else:
            print("File is empty.")
    else:
        print(f"File not found: {FILE_PATH}")

