#!/bin/bash
# One-command installer for Hermes PDF + DOCX Skills

set -e

echo "Cloning hermes-pdf-docx-skills..."
git clone https://github.com/legiovi/hermes-pdf-docx-skills.git /tmp/hermes-document-skills

cd /tmp/hermes-document-skills

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Copy pdf_skill.py and docx_skill.py to your Hermes skills/ directory"
echo "2. Register the functions in your Hermes tool registry"
echo "3. Restart Hermes or reload skills"
echo ""
echo "Repo location: /tmp/hermes-document-skills"