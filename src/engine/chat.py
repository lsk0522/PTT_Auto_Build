import sys
import argparse
import os
import requests
from google import genai
from google.genai import types

def get_chat_system_prompt(language: str) -> str:
    return f"""
    You are a Presentation Assistant AI. Your job is to help the user design slide presentations.
    You must always structure your slide proposals using our Slide DSL so the app can preview and generate them.
    
    DSL Rules:
    1. Separate slides with `---`
    2. Start each slide with `@slide: <type>` (types: `title`, `bullets`)
    3. Use standard Markdown for the content (`#` for slide title, `-` for bullets).
    
    Example Output:
    @slide: title
    # Slide Title
    Subtitle of the presentation
    ---
    @slide: bullets
    ## Slide Header
    - Key point 1
    - Key point 2
    
    IMPORTANT: You must write all slide contents, titles, bullets, and responses in {language}.
    """

def chat_gemini(api_key: str, message: str, language: str) -> str:
    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        system_instruction=get_chat_system_prompt(language)
    )
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=message,
        config=config
    )
    return response.text

def chat_perplexity(api_key: str, message: str, language: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": get_chat_system_prompt(language)},
            {"role": "user", "content": message}
        ]
    }
    response = requests.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def chat_openai(api_key: str, message: str, language: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": get_chat_system_prompt(language)},
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
    parser.add_argument("--language", default="Korean")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get(f"{args.provider.upper()}_API_KEY", "")
    if not api_key:
        print("Error: API Key is missing", file=sys.stderr)
        sys.exit(1)

    provider = args.provider.lower()
    try:
        if provider == "gemini":
            print(chat_gemini(api_key, args.message, args.language))
        elif provider == "perplexity":
            print(chat_perplexity(api_key, args.message, args.language))
        elif provider == "openai":
            print(chat_openai(api_key, args.message, args.language))
        else:
            print(f"Error: Unknown provider {provider}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
