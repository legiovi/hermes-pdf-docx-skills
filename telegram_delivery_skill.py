"""
Telegram File Delivery Skill for Hermes Agent

Allows Hermes to send generated documents (PDF, DOCX, images, etc.) 
back to the user via Telegram.

Requirements:
    pip install python-telegram-bot --upgrade

Setup:
    - Store your bot token securely (env variable or Hermes config)
    - The skill needs access to the user's chat_id
"""

import os
import asyncio
from typing import Optional
from telegram import Bot
from telegram.error import TelegramError


async def send_document(
    file_path: str,
    chat_id: int,
    bot_token: str,
    caption: str = "",
    filename: Optional[str] = None
) -> bool:
    """
    Send any file (PDF, DOCX, image, etc.) to the user via Telegram.
    
    Args:
        file_path: Full path to the file on the server
        chat_id: Telegram chat ID of the user
        bot_token: Your Telegram Bot token
        caption: Optional message/caption
        filename: Optional custom filename to show in Telegram
    
    Returns:
        True if sent successfully, False otherwise
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    
    if not filename:
        filename = os.path.basename(file_path)
    
    try:
        bot = Bot(token=bot_token)
        
        with open(file_path, "rb") as document:
            await bot.send_document(
                chat_id=chat_id,
                document=document,
                filename=filename,
                caption=caption
            )
        print(f"File sent successfully: {filename}")
        return True
        
    except TelegramError as e:
        print(f"Telegram error while sending file: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def send_document_sync(
    file_path: str,
    chat_id: int,
    bot_token: str,
    caption: str = "",
    filename: Optional[str] = None
) -> bool:
    """Synchronous version (easier to call from Hermes)."""
    return asyncio.run(
        send_document(file_path, chat_id, bot_token, caption, filename)
    )


# Example usage inside Hermes:
# from telegram_delivery_skill import send_document_sync
#
# success = send_document_sync(
#     file_path="/path/to/report.pdf",
#     chat_id=USER_CHAT_ID,
#     bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
#     caption="Here is your deep research report on Australia hotels & restaurants"
# )
