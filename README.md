# Hermes PDF + DOCX Skills

Professional document processing skills for your Hermes Agent.

## Why these skills?

These skills give your Hermes Agent powerful autonomous capabilities for:
- Reading contracts, invoices, financial reports
- Extracting tables for trading/analysis
- Converting PDFs to images for vision analysis
- Creating professional PDF reports and Word documents
- OCR for scanned documents
- Filling templates and forms

Perfect for business automation, hotel operations, contracts in Qatar, and personal use.

## Installation for Hermes Agent

### Recommended: One-command install

```bash
git clone https://github.com/legiovi/hermes-pdf-docx-skills.git
cd hermes-pdf-docx-skills
pip install -r requirements.txt
```

Then copy `pdf_skill.py` and `docx_skill.py` into your Hermes `skills/` folder and register them.

### Or let Hermes install it autonomously

Share this link with your Hermes Agent:

```
https://github.com/legiovi/hermes-pdf-docx-skills
```

Hermes can:
1. `git clone` the repo
2. Run the installation commands
3. Load the skills into its tool registry

## Available Skills

### pdf_skill.py

Core functions:
- `extract_text(pdf_path, layout=True)` → Clean text extraction
- `extract_tables(pdf_path)` → Tables as list of dicts / DataFrames
- `pdf_to_images(pdf_path, output_dir)` → Render pages as images for vision
- `ocr_pdf(pdf_path)` → OCR for scanned documents
- `merge_pdfs(input_pdfs, output_path)`
- `create_pdf_report(title, content, output_path)` → Generate professional reports

### docx_skill.py

Core functions:
- `create_professional_docx(title, sections, output_path)` → High-quality Word documents
- `read_docx_to_markdown(docx_path)` → Best quality reading
- `fill_docx_template(template_path, replacements, output_path)`
- `docx_to_pdf(docx_path, output_pdf)`

## Integration with Hermes

Register the functions as tools in your Hermes tool registry so the agent can call them autonomously.

Example tool schema (simplified):

```json
{
  "name": "extract_text",
  "description": "Extract clean text from a PDF file",
  "parameters": {
    "type": "object",
    "properties": {
      "pdf_path": {"type": "string"},
      "layout": {"type": "boolean", "default": true}
    }
  }
}
```

## Requirements

See `requirements.txt`. Some features (OCR, PDF rendering) require system packages like `poppler-utils` and `tesseract-ocr`.

## Next Steps

Want more advanced features? Tell me and I can add:
- PDF form filling
- Advanced template editing
- Arabic/Spanish language support
- Invoice generation
- Contract analysis workflows
