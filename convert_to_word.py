"""
Script untuk convert HTML BAB IV & V ke Word Document
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from bs4 import BeautifulSoup
import re

def html_to_word(html_file, output_file):
    """Convert HTML to Word document"""
    
    # Read HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Create Word document
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # Process body content
    body = soup.find('body')
    if body:
        process_element(doc, body)
    
    # Save document
    doc.save(output_file)
    print(f"✅ Document saved to: {output_file}")

def process_element(doc, element):
    """Process HTML element and add to Word document"""
    
    for child in element.children:
        if child.name == 'h1':
            # Title (BAB IV / BAB V)
            text = child.get_text().strip()
            p = doc.add_paragraph(text)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.runs[0]
            run.font.size = Pt(14)
            run.font.bold = True
            p.paragraph_format.space_after = Pt(18)
            
        elif child.name == 'h2':
            # Section heading
            text = child.get_text().strip()
            p = doc.add_paragraph(text)
            run = p.runs[0]
            run.font.size = Pt(12)
            run.font.bold = True
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            
        elif child.name == 'h3':
            # Subsection heading
            text = child.get_text().strip()
            p = doc.add_paragraph(text)
            run = p.runs[0]
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.italic = True
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            
        elif child.name == 'h4':
            # Sub-subsection heading
            text = child.get_text().strip()
            p = doc.add_paragraph(text)
            run = p.runs[0]
            run.font.size = Pt(12)
            run.font.bold = True
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            
        elif child.name == 'p':
            # Paragraph
            text = child.get_text().strip()
            if text:
                # Check if paragraph has no-indent class
                no_indent = 'no-indent' in child.get('class', [])
                p = doc.add_paragraph(text)
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                if not no_indent:
                    p.paragraph_format.first_line_indent = Inches(0.39)  # 1cm
                p.paragraph_format.line_spacing = 1.8
                
                # Process strong/em tags
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(12)
                
        elif child.name == 'ul' or child.name == 'ol':
            # Lists
            process_list(doc, child)
            
        elif child.name == 'table':
            # Tables
            process_table(doc, child)
            
        elif child.name == 'div' and 'figure' in child.get('class', []):
            # Figures/Images
            process_figure(doc, child)
        
        elif hasattr(child, 'children'):
            # Recursively process children
            process_element(doc, child)

def process_list(doc, list_element):
    """Process ul/ol lists"""
    is_ordered = list_element.name == 'ol'
    
    for idx, li in enumerate(list_element.find_all('li', recursive=False), 1):
        text = li.get_text().strip()
        if is_ordered:
            p = doc.add_paragraph(f"{idx}. {text}")
        else:
            p = doc.add_paragraph(text, style='List Bullet')
        
        p.paragraph_format.left_indent = Inches(0.79)  # 2cm
        p.paragraph_format.line_spacing = 1.8

def process_table(doc, table_element):
    """Process HTML table"""
    # Count rows and columns
    rows = table_element.find_all('tr')
    if not rows:
        return
    
    # Get max columns
    max_cols = max(len(row.find_all(['th', 'td'])) for row in rows)
    
    # Create Word table
    word_table = doc.add_table(rows=len(rows), cols=max_cols)
    word_table.style = 'Table Grid'
    
    for row_idx, row in enumerate(rows):
        cells = row.find_all(['th', 'td'])
        for col_idx, cell in enumerate(cells):
            word_cell = word_table.rows[row_idx].cells[col_idx]
            word_cell.text = cell.get_text().strip()
            
            # Format header cells
            if cell.name == 'th':
                for paragraph in word_cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.bold = True
                        run.font.size = Pt(11)
    
    # Add space after table
    doc.add_paragraph()

def process_figure(doc, figure_div):
    """Process figure with image and caption"""
    # Find image
    img = figure_div.find('img')
    if img:
        img_src = img.get('src', '')
        # Convert file:/// path to local path
        if img_src.startswith('file:///'):
            img_path = img_src.replace('file:///', '').replace('/', '\\')
            
            try:
                # Add image
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run()
                run.add_picture(img_path, width=Inches(5.5))
            except Exception as e:
                print(f"⚠️  Could not add image: {img_path} - {e}")
                # Add placeholder text
                p = doc.add_paragraph(f"[Gambar: {img_path}]")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Find caption
    caption = figure_div.find('div', class_='figure-caption')
    if caption:
        caption_text = caption.get_text().strip()
        p = doc.add_paragraph(caption_text)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.font.size = Pt(11)
        run.font.italic = True

if __name__ == '__main__':
    input_file = r'd:\devnolife\research-system\testing_results\BAB_IV_Hasil_dan_Pembahasan.html'
    output_file = r'd:\devnolife\research-system\testing_results\BAB_IV_V_Hasil_dan_Pembahasan.docx'
    
    print("🔄 Converting HTML to Word...")
    html_to_word(input_file, output_file)
    print("✅ Conversion complete!")
