# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import asyncio
import os
import random
import re
from collections import OrderedDict
from io import BytesIO

import aiohttp
from pyrogram import filters
from pyrogram.enums import ChatAction, ChatMemberStatus, ChatType
from pyrogram.types import Message

try:
    import edge_tts
except ImportError:
    edge_tts = None

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None

from config import BANNED_USERS
from MeowMusic import LOGGER, app
from MeowMusic.core.mongo import mongodb
from MeowMusic.misc import SUDOERS

logger = LOGGER(__name__)
DB = mongodb.chatbotdb

API_URL = os.environ.get("CHATBOT_API_URL", "https://chatbot.riteshyt.in/api/chat")
API_KEY = os.environ.get(
    "CHATBOT_API_KEY", "ritesh-8179b3a5da99f300be2d50e1e9789729"
)
CUTE_GIRL_VOICE = os.environ.get("CHATBOT_VOICE", "hi-IN-SwaraNeural")
TRIGGERS = ["hi", "hello", "hey", "baby", "meow"]


def get_send_status() -> bool:
    return True


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return []
        self.cache.move_to_end(key)
        return list(self.cache[key])

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# Conversation history tracking (chat_id -> list of messages)
# Max 1000 chats in memory to prevent leaks
chat_histories = LRUCache(1000)
HISTORY_LIMIT = 30


async def is_admin(message: Message, user_id: int) -> bool:
    if user_id in SUDOERS:
        return True
    try:
        member = await app.get_chat_member(message.chat.id, user_id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except Exception:
        return False


def load_prompt() -> str:
    try:
        path = os.path.join(os.path.dirname(__file__), "prompt.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
    except Exception:
        pass
    return (
        "You are a sweet, cute friendly Indian girl chatting naturally in Hinglish and English. "
        "Keep replies very short and human-like. User is {user_name}. Never admit you are an AI."
    )


SYSTEM_PROMPT = load_prompt()


@app.on_message(filters.command("chatbot") & filters.group & ~BANNED_USERS)
async def chatbot_toggle(_, message: Message):
    if not message.from_user or not await is_admin(message, message.from_user.id):
        return await message.reply_text("❗ Only admins can use this command.")

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/chatbot on - Enable\n/chatbot off - Disable"
        )

    arg = message.command[1].lower()
    if arg == "on":
        await DB.update_one(
            {"chat_id": message.chat.id}, {"$set": {"enabled": True}}, upsert=True
        )
        await message.reply_text("✅ Chatbot is now ENABLED in this group.")
    elif arg == "off":
        await DB.update_one(
            {"chat_id": message.chat.id}, {"$set": {"enabled": False}}, upsert=True
        )
        await message.reply_text("❌ Chatbot is now DISABLED in this group.")
    else:
        await message.reply_text("Invalid argument. Use `on` or `off`.")


@app.on_message(filters.command("voice") & filters.group & ~BANNED_USERS)
async def voice_toggle(_, message: Message):
    if not message.from_user or not await is_admin(message, message.from_user.id):
        return await message.reply_text("❗ Only admins can use this command.")

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/voice on - Enable Voice Mode (Bot will reply with Audio)\n"
            "/voice off - Disable Voice Mode (Bot will reply with Text)"
        )

    arg = message.command[1].lower()
    if arg == "on":
        await DB.update_one(
            {"chat_id": message.chat.id}, {"$set": {"voice_enabled": True}}, upsert=True
        )
        await message.reply_text(
            "🎙 Voice Mode is now ENABLED. I will reply with cute voice notes!"
        )
    elif arg == "off":
        await DB.update_one(
            {"chat_id": message.chat.id}, {"$set": {"voice_enabled": False}}, upsert=True
        )
        await message.reply_text("📝 Voice Mode is now DISABLED. I will reply with text.")
    else:
        await message.reply_text("Invalid argument. Use `on` or `off`.")


async def text_to_speech(text: str) -> BytesIO:
    # Clean formatting markers so speech sounds natural
    clean_text = re.sub(r"[*_`#~]", "", text).strip()
    # Remove code blocks or file notices from spoken audio
    clean_text = re.sub(r"\[Long code block.*?\]", "", clean_text).strip()
    if not clean_text:
        clean_text = "Haanji!"

    mp3_data = b""

    # 1. First priority: High-quality cute girl voice via Edge-TTS (Swara Neural)
    if edge_tts:
        try:
            communicate = edge_tts.Communicate(
                clean_text,
                voice=CUTE_GIRL_VOICE,
                pitch="+10Hz",
                rate="+5%",
            )
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    mp3_data += chunk["data"]
        except Exception as e:
            logger.error(f"Edge-TTS error: {e}")
            mp3_data = b""

    # 2. Fallback: gTTS if Edge-TTS is unavailable or failed
    if not mp3_data:
        if not gTTS:
            raise RuntimeError("Neither edge-tts nor gTTS is installed.")
        loop = asyncio.get_running_loop()

        def _gtts():
            tts = gTTS(clean_text, lang="hi")
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()

        mp3_data = await loop.run_in_executor(None, _gtts)

    # Convert to Telegram Opus voice format
    if AudioSegment:
        try:
            audio = AudioSegment.from_file(BytesIO(mp3_data), format="mp3")
            ogg_fp = BytesIO()
            ogg_fp.name = "voice.ogg"
            audio.export(ogg_fp, format="ogg", codec="libopus")
            ogg_fp.seek(0)
            return ogg_fp
        except Exception as e:
            logger.error(f"Audio conversion error: {e}")

    mp3_fp = BytesIO(mp3_data)
    mp3_fp.name = "voice.mp3"
    return mp3_fp


async def fetch_chat_response(payload: dict) -> dict | None:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    max_retries = 3
    timeout = aiohttp.ClientTimeout(total=60)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        for attempt in range(max_retries):
            try:
                async with session.post(API_URL, json=payload, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json(content_type=None)
                        reply = (
                            data.get("response")
                            or data.get("reply")
                            or data.get("message")
                        )
                        if isinstance(reply, dict):
                            reply = reply.get("content", "")
                        if reply and "503" not in reply and "系统通知" not in reply:
                            return {"response": reply}
                        if attempt < max_retries - 1:
                            await asyncio.sleep(2)
                            continue
                    elif (
                        resp.status in (429, 500, 502, 503)
                        and attempt < max_retries - 1
                    ):
                        await asyncio.sleep(2)
                        continue
                    else:
                        break
            except (aiohttp.ClientError, asyncio.TimeoutError):
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                    continue
                break
            except Exception as e:
                logger.error(f"Chatbot request error: {e}")
                break
    return None


async def transcribe_voice(file_path: str) -> str:
    loop = asyncio.get_running_loop()

    def _transcribe():
        if not AudioSegment or not sr:
            logger.error("Voice transcription requires pydub and speech_recognition.")
            return ""
        wav_path = file_path + ".wav"
        try:
            audio = AudioSegment.from_ogg(file_path)
            audio.export(wav_path, format="wav")

            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="hi-IN")

            return text
        except Exception as e:
            logger.error(f"STT Error: {e}")
            return ""
        finally:
            if os.path.exists(wav_path):
                os.remove(wav_path)

    return await loop.run_in_executor(None, _transcribe)


@app.on_message(
    (filters.text | filters.caption | filters.voice)
    & ~filters.regex(r"^/")
    & ~filters.bot
    & ~BANNED_USERS,
    group=10,
)
async def chatbot_handler(_, message: Message):
    chat_id = message.chat.id
    voice_enabled = False

    # Check database early so we don't process voice/text if bot is disabled in this group
    if message.chat.type != ChatType.PRIVATE:
        settings = await DB.find_one({"chat_id": chat_id})
        if not settings or not settings.get("enabled", False):
            return
        voice_enabled = settings.get("voice_enabled", False)

    input_text = message.text or message.caption

    # Handle incoming voice messages
    if message.voice:
        try:
            await app.send_chat_action(chat_id, ChatAction.TYPING)
            downloaded_file = await message.download()
            input_text = await transcribe_voice(downloaded_file)
            if downloaded_file and os.path.exists(downloaded_file):
                os.remove(downloaded_file)
            if not input_text:
                return
        except Exception as e:
            logger.error(f"Voice handling error: {e}")
            if "ffprobe" in str(e).lower() or "ffmpeg" in str(e).lower():
                await message.reply_text(
                    "❗ Voice feature requires `ffmpeg` installed on the server."
                )
            return

    if not input_text:
        return

    text_lower = input_text.lower().strip()

    if message.chat.type != ChatType.PRIVATE:
        is_trigger = any(t.lower() in text_lower for t in TRIGGERS)
        is_reply_to_bot = (
            message.reply_to_message
            and message.reply_to_message.from_user
            and message.reply_to_message.from_user.is_self
        )
        is_mentioned = (
            app.me
            and app.me.username
            and (f"@{app.me.username.lower()}" in text_lower)
        )

        if not (is_trigger or is_reply_to_bot or is_mentioned):
            return

    # Clean text from mention
    if app.me and app.me.username:
        bot_mention = f"@{app.me.username}"
        if bot_mention in input_text:
            input_text = input_text.replace(bot_mention, "").strip()
            if not input_text:
                return

    user_name = message.from_user.first_name if message.from_user else "Friend"
    group_name = message.chat.title if message.chat else "Private Chat"

    prompt = SYSTEM_PROMPT.replace("{user_name}", user_name)
    prompt += (
        f"\n\nYou are talking in a group named: {group_name}. "
        "Be helpful, cute, and engaging."
    )

    # Update history
    history = chat_histories.get(chat_id)
    history.append({"role": "user", "content": f"{user_name}: {input_text}"})
    if len(history) > HISTORY_LIMIT:
        history = history[-HISTORY_LIMIT:]
    chat_histories.put(chat_id, history)

    history_str = "\n".join([f"[{m['role']}]: {m['content']}" for m in history])
    formatted_prompt = (
        f"System: {prompt}\n\nRecent Chat Context:\n{history_str}\n\n"
        f"User: {input_text}\nAssistant:"
    )

    messages_payload = [{"role": "system", "content": prompt}] + history

    payload = {
        "messages": messages_payload,
        "prompt": formatted_prompt,
    }

    # Decide if we send a voice note this time.
    # If explicitly enabled, always True.
    # If the user sent a voice message, reply with a voice message.
    # Otherwise, give a 15% random chance in normal mode to keep it natural.
    if message.voice:
        should_send_voice = True
    else:
        should_send_voice = True if voice_enabled else (random.random() < 0.15)

    try:
        action = ChatAction.RECORD_AUDIO if should_send_voice else ChatAction.TYPING
        await app.send_chat_action(chat_id, action)
    except Exception:
        pass

    try:
        data = await fetch_chat_response(payload)
        if data:
            reply = data.get("response") or data.get("reply") or data.get("message")
            if isinstance(reply, dict):
                reply = reply.get("content", "")
            if reply:
                # Add assistant response to history
                current_history = chat_histories.get(chat_id)
                current_history.append({"role": "assistant", "content": reply})
                chat_histories.put(chat_id, current_history)

                # Extract and handle long code blocks
                code_blocks = re.findall(r"```([a-zA-Z]*)\n(.*?)```", reply, re.DOTALL)
                files_to_send = []

                for lang, code in code_blocks:
                    lines = code.strip().split("\n")
                    if len(lines) > 5:
                        ext = f".{lang}" if lang else ".txt"
                        if lang == "python":
                            ext = ".py"
                        elif lang in ("javascript", "js"):
                            ext = ".js"
                        elif lang == "html":
                            ext = ".html"
                        elif lang == "css":
                            ext = ".css"
                        elif lang == "json":
                            ext = ".json"
                        elif lang in ("cpp", "c++"):
                            ext = ".cpp"
                        elif lang in ("sh", "bash"):
                            ext = ".sh"

                        filename = f"code_snippet{ext}"
                        file_obj = BytesIO(code.strip().encode("utf-8"))
                        file_obj.name = filename
                        files_to_send.append(file_obj)

                        original_block = f"```{lang}\n{code}```"
                        reply = reply.replace(
                            original_block,
                            f"**[Long code block sent as file: {filename}]**",
                        )

                if reply.strip():
                    if should_send_voice and not code_blocks and (edge_tts or gTTS):
                        try:
                            voice_fp = await text_to_speech(reply)
                            await message.reply_voice(voice=voice_fp)
                        except Exception as e:
                            logger.error(f"TTS error: {e}")
                            await message.reply_text(reply)
                    else:
                        await message.reply_text(reply)

                for f in files_to_send:
                    await message.reply_document(document=f)
    except Exception as e:
        logger.error(f"Chatbot error: {e}")
