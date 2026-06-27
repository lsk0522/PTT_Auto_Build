import re
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
    Parses a DESIGN.md file and extracts theme tokens from YAML frontmatter.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Default values
    theme_data = {
        "primary_color": "#0075de",
        "secondary_color": "#f5f5f5",
        "bg_color": "#ffffff",
        "text_color": "#1f1f1f",
        "title_font": "Inter",
        "body_font": "Inter"
    }
    
    # Try parsing YAML frontmatter
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        try:
            parsed = yaml.safe_load(yaml_content)
            if parsed:
                colors = parsed.get("colors", {})
                typography = parsed.get("typography", {})
                
                theme_data["primary_color"] = colors.get("primary", theme_data["primary_color"])
                theme_data["secondary_color"] = colors.get("secondary", theme_data["secondary_color"])
                theme_data["bg_color"] = colors.get("canvas-soft", colors.get("bg_color", theme_data["bg_color"]))
                theme_data["text_color"] = colors.get("ink", colors.get("text_color", theme_data["text_color"]))
                theme_data["title_font"] = typography.get("display-1", typography.get("title_font", theme_data["title_font"]))
                theme_data["body_font"] = typography.get("body-md", typography.get("body_font", theme_data["body_font"]))
        except Exception as e:
            print(f"Warning: Failed to parse YAML frontmatter: {e}")
            
    return Theme(**theme_data)
