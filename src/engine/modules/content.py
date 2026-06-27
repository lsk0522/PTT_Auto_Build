import os
import requests
from google import genai
from dataclasses import dataclass
from typing import List

@dataclass
class SlideModel:
    kind: str
    meta: dict
    content: str

def get_system_prompt(language: str = "Korean") -> str:
    return f"""
    You are an expert presentation designer. Convert the following raw text into a structured presentation using our Slide DSL.
    IMPORTANT: You must write the output slides (titles, bullet points, and subtitles) in {language}.
    
    Rules:
    1. Separate slides with `---`
    2. Start each slide with `@slide: <type>` (types: `title`, `bullets`)
    3. Use standard Markdown for the content (`#` for slide title, `-` for bullets).
    
    Example Output:
    @slide: title
    # My Presentation
    Subtitle goes here
    ---
    @slide: bullets
    ## Key Points
    - First point
    - Second point
    """

from google import genai
from google.genai import types

def generate_with_gemini(api_key: str, raw_text: str, language: str) -> str:
    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        system_instruction=get_system_prompt(language)
    )
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Raw Text:\n{raw_text}",
        config=config
    )
    return response.text

def generate_with_perplexity(api_key: str, raw_text: str, language: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": get_system_prompt(language)},
            {"role": "user", "content": f"Convert this to slides:\n{raw_text}"}
        ]
    }
    response = requests.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def generate_with_openai(api_key: str, raw_text: str, language: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": get_system_prompt(language)},
            {"role": "user", "content": f"Convert this to slides:\n{raw_text}"}
        ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def generate_slide_dsl_with_llm(raw_text: str, provider: str, api_key: str, language: str = "Korean") -> str:
    if not api_key:
        api_key = os.environ.get(f"{provider.upper()}_API_KEY", "")
        if not api_key:
            raise ValueError(f"API key for {provider} is not provided or set in environment variables.")
            
    provider = provider.lower()
    if provider == "gemini":
        return generate_with_gemini(api_key, raw_text, language)
    elif provider == "perplexity":
        return generate_with_perplexity(api_key, raw_text, language)
    elif provider == "openai":
        return generate_with_openai(api_key, raw_text, language)
    else:
        raise ValueError(f"Unsupported AI provider: {provider}")

def parse_slide_dsl(markdown_text: str) -> List[SlideModel]:
    slides = []
    blocks = markdown_text.split("---")
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        lines = block.split('\n')
        kind = "bullets"
        meta = {}
        content_lines = []
        
        for line in lines:
            if line.startswith("@slide:"):
                kind = line.split(":")[1].strip()
            elif line.startswith("@"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    meta[parts[0].strip('@')] = parts[1].strip()
            else:
                content_lines.append(line)
                
        slides.append(SlideModel(kind=kind, meta=meta, content='\n'.join(content_lines).strip()))
        
    return slides

def process_input(input_text: str, is_raw_data: bool = True, provider: str = "gemini", api_key: str = "", language: str = "Korean") -> List[SlideModel]:
    if is_raw_data:
        dsl_text = generate_slide_dsl_with_llm(input_text, provider, api_key, language)
    else:
        dsl_text = input_text
        
    return parse_slide_dsl(dsl_text)
