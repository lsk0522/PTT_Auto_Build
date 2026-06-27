import os
import sys
import argparse
from datetime import datetime
from modules.theme import parse_design_md
from modules.content import process_input
from modules.generator import generate_pptx

def get_unique_filepath(filepath: str) -> str:
    if not os.path.exists(filepath):
        return filepath
        
    dir_name, file_name = os.path.split(filepath)
    name, ext = os.path.splitext(file_name)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filepath = os.path.join(dir_name, f"{name}_{timestamp}{ext}")
    
    counter = 1
    while os.path.exists(new_filepath):
        new_filepath = os.path.join(dir_name, f"{name}_{timestamp}_{counter}{ext}")
        counter += 1
        
    return new_filepath

def main():
    parser = argparse.ArgumentParser(description="Generate PPTX from DESIGN.md and raw text/materials.")
    parser.add_argument("--design", required=True, help="Path to DESIGN.md file")
    parser.add_argument("--input", help="Path to raw text/materials or slide DSL")
    parser.add_argument("--text", help="Raw text content passed directly")
    parser.add_argument("--out", required=True, help="Output path for the generated .pptx")
    parser.add_argument("--raw", action="store_true", help="Flag to indicate input is raw text requiring LLM processing")
    parser.add_argument("--provider", default="gemini", help="AI provider (gemini, perplexity, openai)")
    parser.add_argument("--api-key", default="", help="API key for the chosen provider")
    parser.add_argument("--language", default="Korean", help="Target output language")
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        
    unique_out_path = get_unique_filepath(args.out)
    
    print(f"Parsing design file: {args.design}")
    theme = parse_design_md(args.design)
    
    if args.text:
        input_text = args.text
    elif args.input:
        print(f"Processing input file: {args.input}")
        with open(args.input, 'r', encoding='utf-8') as f:
            input_text = f.read()
    else:
        print("Error: Must provide either --input or --text")
        sys.exit(1)
        
    slides = process_input(input_text, is_raw_data=args.raw, provider=args.provider, api_key=args.api_key, language=args.language)
    print(f"Generated {len(slides)} slides.")
    
    print(f"Generating PPTX: {unique_out_path}")
    generate_pptx(theme, slides, unique_out_path)
    print("Done!")

if __name__ == "__main__":
    main()
