import os
from google import genai
from dataclasses import dataclass
from typing import List

@dataclass
class SlideModel:
    kind: str  # e.g., 'title', 'bullets'
    meta: dict
    content: str  # The raw markdown content for this slide

def generate_slide_dsl_with_llm(raw_text: str) -> str:
    """
    Uses Gemini API to convert raw text into our @slide DSL markdown.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert presentation designer. Convert the following raw text into a structured presentation using our Slide DSL.
    
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
    
    Raw Text:
    {raw_text}
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

def parse_slide_dsl(markdown_text: str) -> List[SlideModel]:
    """
    Parses the @slide DSL markdown into SlideModel objects.
    """
    slides = []
    blocks = markdown_text.split("---")
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        lines = block.split('\n')
        kind = "bullets" # default
        meta = {}
        content_lines = []
        
        for line in lines:
            if line.startswith("@slide:"):
                kind = line.split(":")[1].strip()
            elif line.startswith("@"):
                # parse other meta tags like @layout: 2col
                parts = line.split(":", 1)
                if len(parts) == 2:
                    meta[parts[0].strip('@')] = parts[1].strip()
            else:
                content_lines.append(line)
                
        slides.append(SlideModel(kind=kind, meta=meta, content='\n'.join(content_lines).strip()))
        
    return slides

def process_input(input_text: str, is_raw_data: bool = True) -> List[SlideModel]:
    """
    Main entry point for Module 2.
    If is_raw_data is True, it first runs through the LLM.
    Then parses the DSL into SlideModels.
    """
    if is_raw_data:
        dsl_text = generate_slide_dsl_with_llm(input_text)
    else:
        dsl_text = input_text
        
    return parse_slide_dsl(dsl_text)
