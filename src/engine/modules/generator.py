from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from .theme import Theme
from .content import SlideModel
from typing import List

def hex_to_rgb(hex_str: str) -> RGBColor:
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

def set_slide_background(slide, bg_color_hex: str):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = hex_to_rgb(bg_color_hex)

def generate_pptx(theme: Theme, slides: List[SlideModel], output_path: str):
    """
    Module 3: Generates a highly customized and beautiful .pptx file.
    Uses blank slides to programmatically draw modern UI layouts.
    """
    prs = Presentation()
    
    # Set standard widescreen 16:9 dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Slide layout 6 is a completely blank slide
    blank_layout = prs.slide_layouts[6]
    
    for index, slide_model in enumerate(slides):
        slide = prs.slides.add_slide(blank_layout)
        set_slide_background(slide, theme.bg_color)
        
        if slide_model.kind == 'title':
            # 1. Left Accent Decorative Bar
            accent_bar = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, 
                Inches(0), Inches(0), Inches(0.4), Inches(7.5)
            )
            accent_bar.fill.solid()
            accent_bar.fill.fore_color.rgb = hex_to_rgb(theme.primary_color)
            accent_bar.line.fill.background()
            
            # 2. Main Title & Subtitle Text Box
            # Combine into a single text frame to prevent overlap
            txBox = slide.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.5), Inches(4.0))
            tf = txBox.text_frame
            tf.word_wrap = True
            
            lines = slide_model.content.split('\n')
            title_text = lines[0].strip('# ') if len(lines) > 0 else "Title"
            subtitle_text = lines[1].strip() if len(lines) > 1 else ""
            
            # Add Title Paragraph
            p_title = tf.paragraphs[0]
            p_title.text = title_text
            p_title.font.name = theme.title_font
            p_title.font.size = Pt(54)
            p_title.font.bold = True
            p_title.font.color.rgb = hex_to_rgb(theme.primary_color)
            p_title.space_after = Pt(20)
            
            # Add Subtitle Paragraph
            if subtitle_text:
                p_sub = tf.add_paragraph()
                p_sub.text = subtitle_text
                p_sub.font.name = theme.body_font
                p_sub.font.size = Pt(22)
                p_sub.font.color.rgb = hex_to_rgb(theme.text_color)
                
        elif slide_model.kind == 'bullets':
            # 1. Top Decorative Separator Line
            sep_line = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.04)
            )
            sep_line.fill.solid()
            sep_line.fill.fore_color.rgb = hex_to_rgb(theme.primary_color)
            sep_line.line.fill.background()
            
            # 2. Title Text Box
            title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.8))
            tf_title = title_box.text_frame
            tf_title.word_wrap = True
            p_title = tf_title.paragraphs[0]
            
            # 3. Content Text Box
            content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
            tf_content = content_box.text_frame
            tf_content.word_wrap = True
            
            lines = slide_model.content.split('\n')
            title_text = "Untitled Slide"
            bullets = []
            
            for line in lines:
                if line.startswith('#'):
                    title_text = line.strip('# ')
                elif line.startswith('-'):
                    bullets.append(line.strip('- '))
                    
            # Set slide title
            p_title.text = title_text
            p_title.font.name = theme.title_font
            p_title.font.size = Pt(36)
            p_title.font.bold = True
            p_title.font.color.rgb = hex_to_rgb(theme.primary_color)
            
            # Add bullet points
            for i, bullet in enumerate(bullets):
                p_bullet = tf_content.paragraphs[0] if i == 0 else tf_content.add_paragraph()
                p_bullet.text = bullet
                p_bullet.level = 0
                p_bullet.font.name = theme.body_font
                p_bullet.font.size = Pt(20)
                p_bullet.font.color.rgb = hex_to_rgb(theme.text_color)
                p_bullet.space_after = Pt(16)
                
            # 4. Tiny Slide Number (Footer)
            footer_box = slide.shapes.add_textbox(Inches(11.5), Inches(6.8), Inches(1.0), Inches(0.4))
            tf_footer = footer_box.text_frame
            p_footer = tf_footer.paragraphs[0]
            p_footer.text = str(index + 1)
            p_footer.alignment = PP_ALIGN.RIGHT
            p_footer.font.name = theme.body_font
            p_footer.font.size = Pt(12)
            p_footer.font.color.rgb = hex_to_rgb(theme.text_color)
            
    prs.save(output_path)
