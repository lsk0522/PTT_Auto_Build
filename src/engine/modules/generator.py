from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from .theme import Theme
from .content import SlideModel
from typing import List

def hex_to_rgb(hex_str: str) -> RGBColor:
    hex_str = hex_str.lstrip('#')
    return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

def generate_pptx(theme: Theme, slides: List[SlideModel], output_path: str):
    """
    Module 3: Generates the .pptx file using python-pptx based on the Theme and SlideModels.
    """
    prs = Presentation()
    
    # Very basic layouts: 0 is usually Title, 1 is Title and Content
    title_layout = prs.slide_layouts[0]
    bullet_layout = prs.slide_layouts[1]
    
    for slide_model in slides:
        if slide_model.kind == 'title':
            slide = prs.slides.add_slide(title_layout)
            title = slide.shapes.title
            subtitle = slide.placeholders[1]
            
            # Very basic markdown parsing for title
            lines = slide_model.content.split('\n')
            if len(lines) > 0:
                title.text = lines[0].strip('# ')
            if len(lines) > 1:
                subtitle.text = lines[1]
                
            # Apply theme colors
            if title.text_frame.paragraphs:
                title.text_frame.paragraphs[0].font.color.rgb = hex_to_rgb(theme.primary_color)
                
        elif slide_model.kind == 'bullets':
            slide = prs.slides.add_slide(bullet_layout)
            title = slide.shapes.title
            body = slide.placeholders[1]
            
            lines = slide_model.content.split('\n')
            body_text = []
            for line in lines:
                if line.startswith('#'):
                    title.text = line.strip('# ')
                elif line.startswith('-'):
                    body_text.append(line.strip('- '))
            
            body.text = '\n'.join(body_text)
            
            # Apply theme colors
            if title.text_frame.paragraphs:
                title.text_frame.paragraphs[0].font.color.rgb = hex_to_rgb(theme.primary_color)
                
    prs.save(output_path)
