import yaml
from dataclasses import dataclass

@dataclass
class Theme:
    primary_color: str
    secondary_color: str
    bg_color: str
    text_color: str
    title_font: str
    body_font: str

def parse_design_md(filepath: str) -> Theme:
    """
    Parses a DESIGN.md file and extracts theme tokens.
    For MVP, we assume a simple YAML frontmatter or key-value format.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Very basic mock parser for now
    # We will expand this to support actual Notion/DESIGN.md rules
    theme_data = {
        "primary_color": "#00FF41",
        "secondary_color": "#2D2D2D",
        "bg_color": "#1A1A1A",
        "text_color": "#FFFFFF",
        "title_font": "Inter",
        "body_font": "Inter"
    }
    
    return Theme(**theme_data)
