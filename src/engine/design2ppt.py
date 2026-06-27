import argparse
import sys
from modules.theme import parse_design_md
from modules.content import process_input
from modules.generator import generate_pptx

def main():
    parser = argparse.ArgumentParser(description="Generate PPTX from DESIGN.md and raw text/materials.")
    parser.add_argument("--design", required=True, help="Path to DESIGN.md file")
    parser.add_argument("--input", required=True, help="Path to raw text/materials or slide DSL")
    parser.add_argument("--out", required=True, help="Output path for the generated .pptx")
    parser.add_argument("--raw", action="store_true", help="Flag to indicate input is raw text requiring LLM processing")
    parser.add_argument("--provider", default="gemini", help="AI provider (gemini, perplexity, openai)")
    parser.add_argument("--api-key", default="", help="API key for the chosen provider")
    
    args = parser.parse_args()
    
    print(f"Parsing design file: {args.design}")
    theme = parse_design_md(args.design)
    
    print(f"Processing input file: {args.input}")
    with open(args.input, 'r', encoding='utf-8') as f:
        input_text = f.read()
        
    slides = process_input(input_text, is_raw_data=args.raw, provider=args.provider, api_key=args.api_key)
    print(f"Generated {len(slides)} slides.")
    
    print(f"Generating PPTX: {args.out}")
    generate_pptx(theme, slides, args.out)
    print("Done!")

if __name__ == "__main__":
    main()
