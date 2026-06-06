"""
Voice Skill for Hermes Agent

High-quality Speech-to-Text (STT) + Text-to-Speech (TTS)

Recommended stack:
- STT: faster-whisper (large-v3-turbo or distil)
- TTS: Piper (fast + good Spanish) or XTTS-v2 (higher quality + cloning)

This skill allows Hermes to:
- Transcribe voice messages
- Generate natural voice output
- Support Spanish well

Install:
    pip install faster-whisper piper-tts

For Piper voices: https://rhasspy.github.io/piper-samples/
For XTTS: pip install TTS
"""

import os
import subprocess
from typing import Optional

try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None

try:
    from piper import PiperVoice
except ImportError:
    PiperVoice = None


# ==================== STT (Speech to Text) ====================

def transcribe_audio(
    audio_path: str,
    model_size: str = "large-v3-turbo",
    language: str = "es",
    device: str = "auto"
) -> str:
    """
    Transcribe audio file to text using faster-whisper.
    
    Best models: large-v3-turbo, large-v3, distil-large-v3
    language: 'es' for Spanish, 'en' for English, or None for auto
    """
    if WhisperModel is None:
        raise ImportError("Install faster-whisper: pip install faster-whisper")
    
    print(f"Loading Whisper model: {model_size}...")
    model = WhisperModel(model_size, device=device, compute_type="int8")
    
    segments, info = model.transcribe(
        audio_path,
        language=language,
        beam_size=5,
        vad_filter=True
    )
    
    text = " ".join([segment.text for segment in segments])
    print(f"Detected language: {info.language} (prob: {info.language_probability:.2f})")
    return text.strip()


def transcribe_audio_simple(audio_path: str, language: str = "es") -> str:
    """Simpler version using whisper.cpp or subprocess if preferred."""
    # Fallback to whisper command if faster-whisper not installed
    cmd = ["whisper", audio_path, "--language", language, "--model", "large-v3-turbo", "--output_format", "txt"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return "Transcription failed"


# ==================== TTS (Text to Speech) ====================

def text_to_speech_piper(
    text: str,
    output_path: str,
    voice_model: str = "es_ES-davefx-medium",  # Good Spanish voice
    piper_path: str = "piper"
) -> str:
    """
    Convert text to speech using Piper TTS (fast and good quality).
    
    Popular Spanish voices:
    - es_ES-davefx-medium
    - es_ES-carlfm-x_low
    - es_MX-ald-medium
    
    Download voices from: https://rhasspy.github.io/piper-samples/
    """
    if PiperVoice is None:
        # Fallback to subprocess
        cmd = [piper_path, "--model", voice_model, "--output_file", output_path]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, text=True)
        process.communicate(input=text)
        return output_path
    
    voice = PiperVoice.load(voice_model)
    with open(output_path, "wb") as wav_file:
        voice.synthesize(text, wav_file)
    return output_path


def text_to_speech_xtts(
    text: str,
    output_path: str,
    speaker_wav: Optional[str] = None,
    language: str = "es"
) -> str:
    """
    Higher quality TTS using XTTS-v2 (supports voice cloning).
    Requires: pip install TTS
    
    speaker_wav: Path to a short audio sample for voice cloning (6-10 seconds)
    """
    try:
        from TTS.api import TTS
    except ImportError:
        raise ImportError("Install Coqui TTS: pip install TTS")
    
    print("Loading XTTS model...")
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)
    
    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language=language,
        file_path=output_path
    )
    return output_path


def speak(
    text: str,
    output_path: str = "/tmp/hermes_response.wav",
    method: str = "piper",
    voice: str = "es_ES-davefx-medium"
) -> str:
    """
    Main function Hermes should use.
    
    method: 'piper' (recommended for speed) or 'xtts' (higher quality + cloning)
    """
    if method == "piper":
        return text_to_speech_piper(text, output_path, voice_model=voice)
    elif method == "xtts":
        return text_to_speech_xtts(text, output_path)
    else:
        raise ValueError("Method must be 'piper' or 'xtts'")


# ==================== Full Voice Interaction ====================

def process_voice_input(
    audio_path: str,
    tts_method: str = "piper",
    output_audio_path: str = "/tmp/hermes_response.wav"
) -> dict:
    """
    Full pipeline: Transcribe voice -> Return text (Hermes will process it)
    Then use speak() to generate response audio.
    """
    transcribed_text = transcribe_audio(audio_path)
    
    return {
        "transcribed_text": transcribed_text,
        "original_audio": audio_path,
        "ready_for_llm": True
    }
