# Hermes PDF + DOCX + Voice + Telegram Skills

Complete skill pack for your Hermes Agent.

## Available Skills

### 1. Document Skills
- `pdf_skill.py` — Extract text/tables, OCR, create reports, merge/split PDFs
- `docx_skill.py` — Create professional Word documents, read templates, convert to PDF

### 2. Telegram Delivery
- `telegram_delivery_skill.py` — Send generated files directly back to you in Telegram

### 3. Voice Skill (NEW)
- `voice_skill.py` — High-quality Speech-to-Text + Text-to-Speech

## Voice Capabilities

**Recommended stack:**
- **STT (listening)**: faster-whisper (large-v3-turbo)
- **TTS (speaking)**: Piper TTS (fast + good Spanish voices) or XTTS-v2 (higher quality + voice cloning)

### Quick Start for Voice

```bash
pip install faster-whisper piper-tts
```

For better quality + voice cloning:
```bash
pip install faster-whisper TTS
```

**Good Spanish voices for Piper:**
- `es_ES-davefx-medium` (recommended)
- `es_ES-carlfm-x_low`
- `es_MX-ald-medium`

Download voices: https://rhasspy.github.io/piper-samples/

## Full Installation (Recommended)

```bash
git clone https://github.com/legiovi/hermes-pdf-docx-skills.git
cd hermes-pdf-docx-skills
pip install -r requirements.txt
```

Then copy the `.py` files into your Hermes `skills/` folder and register them.

## Main Link to Share with Hermes

```
https://github.com/legiovi/hermes-pdf-docx-skills
```

Hermes can autonomously clone the repo and install the skills.

## Next Steps
Want me to improve anything? Examples:
- Better real-time voice conversation flow
- Voice cloning setup
- Integration with Telegram voice messages
- Add Kokoro TTS as option
