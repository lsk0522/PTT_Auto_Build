import sys
import argparse
import os
import requests
from google import genai

def chat_gemini(api_key: str, message: str) -> str:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=message
    )
    return response.text

def chat_perplexity(api_key: str, message: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "user", "content": message}
        ]
    }
    response = requests.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def chat_openai(api_key: str, message: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": message}
        ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", required=True)
    parser.add_argument("--provider", default="gemini")
    parser.add_argument("--api-key", default="")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get(f"{args.provider.upper()}_API_KEY", "")
    if not api_key:
        print("Error: API Key is missing")
        sys.exit(1)

    provider = args.provider.lower()
    try:
        if provider == "gemini":
            print(chat_gemini(api_key, args.message))
        elif provider == "perplexity":
            print(chat_perplexity(api_key, args.message))
        elif provider == "openai":
            print(chat_openai(api_key, args.message))
        else:
            print(f"Error: Unknown provider {provider}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
