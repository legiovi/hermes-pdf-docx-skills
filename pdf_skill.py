"""
PDF Skill for Hermes Agent
High-value document processing functions.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional, Union
import pdfplumber
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from pdf2image import convert_from_path
import pytesseract
from PIL import Image


def extract_text(pdf_path: str, layout: bool = True) -> str:
    """Extract text from PDF. layout=True preserves structure better."""
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if layout:
                page_text = page.extract_text(layout=True) or ""
            else:
                page_text = page.extract_text() or ""
            text_parts.append(f"--- Page {page.page_number} ---\n{page_text}")
    return "\n\n".join(text_parts)


def extract_tables(pdf_path: str) -> List[Dict]:
    """Extract all tables from PDF as list of dicts (ready for analysis)."""
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            for table in tables:
                if table:
                    headers = table[0]
                    for row in table[1:]:
                        if any(cell for cell in row):  # skip empty rows
                            row_dict = {headers[i]: row[i] for i in range(len(headers)) if i < len(row)}
                            row_dict["_page"] = page_num
                            all_tables.append(row_dict)
    return all_tables


def pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 150) -> List[str]:
    """Convert PDF pages to images for vision analysis. Returns list of image paths."""
    os.makedirs(output_dir, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=dpi)
    saved_paths = []
    for i, img in enumerate(images):
        path = os.path.join(output_dir, f"page_{i+1:03d}.png")
        img.save(path, "PNG")
        saved_paths.append(path)
    return saved_paths


def ocr_pdf(pdf_path: str, lang: str = "eng") -> str:
    """OCR for scanned PDFs. lang can be 'eng+spa+ara' etc."""
    text_parts = []
    images = convert_from_path(pdf_path, dpi=300)
    for i, img in enumerate(images):
        page_text = pytesseract.image_to_string(img, lang=lang)
        text_parts.append(f"--- Page {i+1} ---\n{page_text}")
    return "\n\n".join(text_parts)


def merge_pdfs(input_pdfs: List[str], output_path: str) -> str:
    """Merge multiple PDFs into one."""
    writer = PdfWriter()
    for pdf_file in input_pdfs:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path


def create_pdf_report(title: str, content: str, output_path: str, 
                       author: str = "Hermes Agent") -> str:
    """Create a clean professional PDF report from text content."""
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        textColor=colors.HexColor('#1a365d')
    )
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))
    
    # Content
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=8
    )
    for paragraph in content.split('\n\n'):
        if paragraph.strip():
            story.append(Paragraph(paragraph.strip().replace('\n', ' '), body_style))
    
    doc.build(story)
    return output_path
