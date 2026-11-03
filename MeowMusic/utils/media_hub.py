# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import asyncio
import os
from datetime import datetime

import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient

from MeowMusic import LOGGER
from MeowMusic import userbot as us
from MeowMusic.core.userbot import assistants

DATA_CHANNEL = -1004279018420

API_URL = os.environ.get("MEOW_API_URL", "https://music.yukiapi.site")
API_KEY = os.environ.get(
    "MEOW_API_KEY", "yuki_95a6c913e9b5f9094b013ce8e963a320"
)  # 🔑 Get Key: @MeowApiRobot On Telegram

# mongo uri
MONGO_DB_URI = ""

CACHE_MONGO_URI = MONGO_DB_URI
mongo_client = AsyncIOMotorClient(CACHE_MONGO_URI)
cache_db = mongo_client["ytapi"]
media_data = cache_db["media"]


def get_assistant():
    return us.one if 1 in assistants else None


class MediaHub:
    def __init__(self):
        self.session = None

    async def _get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(limit=50)
            )
        return self.session

    async def close(self):
        if self.session:
            await self.session.close()

    async def get_audio(self, video_id: str):
        assistant = get_assistant()
        if not assistant:
            return None

        DOWNLOAD_DIR = "downloads"
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        local_file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")

        if os.path.exists(local_file_path) and os.path.getsize(local_file_path) > 0:
            LOGGER(__name__).info(f"[LOCAL HIT - AUDIO] File available: {video_id}")
            return local_file_path

        doc = await media_data.find_one({"video_id": video_id, "type": "audio"})

        if doc and doc.get("status") == "ready":
            try:
                msg = await assistant.get_messages(DATA_CHANNEL, doc["message_id"])
                if msg and msg.audio:
                    LOGGER(__name__).info(
                        f"[DB HIT - AUDIO] Downloading from Telegram: {video_id}"
                    )
                    downloaded_path = await assistant.download_media(
                        msg, file_name=local_file_path
                    )
                    if downloaded_path:
                        LOGGER(__name__).info(
                            f"[READY] Audio play ready: {downloaded_path}"
                        )
                        return downloaded_path
            except Exception as e:
                LOGGER(__name__).warning(
                    f"[WARNING] Telegram audio download error: {e}"
                )

        LOGGER(__name__).info(f"[API REQUEST - AUDIO] Fetching from API: {video_id}")
        asyncio.create_task(self._cache_audio(video_id))

        return await self._get_direct_download(video_id, media_type="audio")

    async def _cache_audio(self, video_id: str):
        try:
            existing = await media_data.find_one(
                {"video_id": video_id, "type": "audio"}
            )
            if existing and existing.get("status") in ["processing", "ready"]:
                return

            await media_data.update_one(
                {"video_id": video_id, "type": "audio"},
                {"$set": {"status": "processing", "updated_at": datetime.utcnow()}},
                upsert=True,
            )

            file_path = await self._download_external(video_id, media_type="audio")

            if not file_path:
                await media_data.delete_one({"video_id": video_id, "type": "audio"})
                return

            assistant = get_assistant()
            if not assistant:
                return

            LOGGER(__name__).info(f"[UPLOADING] Telegram Channel uploading: {video_id}")
            msg = await assistant.send_audio(
                DATA_CHANNEL, audio=file_path, caption=f"ID: {video_id}"
            )

            await media_data.update_one(
                {"video_id": video_id, "type": "audio"},
                {
                    "$set": {
                        "video_id": video_id,
                        "type": "audio",
                        "file_id": msg.audio.file_id,
                        "file_unique_id": msg.audio.file_unique_id,
                        "message_id": msg.id,
                        "title": msg.audio.file_name or f"{video_id}.mp3",
                        "size": msg.audio.file_size,
                        "status": "ready",
                        "updated_at": datetime.utcnow(),
                    }
                },
                upsert=True,
            )
            LOGGER(__name__).info(f"[DB SAVED] Audio cached in DB: {video_id}")

            if os.path.exists(file_path):
                os.remove(file_path)

        except Exception as e:
            LOGGER(__name__).error(f"Audio Cache Error: {e}")

    async def get_video(self, video_id: str):
        assistant = get_assistant()
        if not assistant:
            return None

        DOWNLOAD_DIR = "downloads"
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        local_file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

        if os.path.exists(local_file_path) and os.path.getsize(local_file_path) > 0:
            LOGGER(__name__).info(f"[LOCAL HIT - VIDEO] File available: {video_id}")
            return local_file_path

        doc = await media_data.find_one({"video_id": video_id, "type": "video"})

        if doc and doc.get("status") == "ready":
            try:
                msg = await assistant.get_messages(DATA_CHANNEL, doc["message_id"])
                if msg and msg.video:
                    LOGGER(__name__).info(
                        f"[DB HIT - VIDEO] Downloading from Telegram: {video_id}"
                    )
                    downloaded_path = await assistant.download_media(
                        msg, file_name=local_file_path
                    )
                    if downloaded_path:
                        LOGGER(__name__).info(
                            f"[READY] Video play ready: {downloaded_path}"
                        )
                        return downloaded_path
            except Exception as e:
                LOGGER(__name__).warning(
                    f"[WARNING] Telegram video download error: {e}"
                )

        LOGGER(__name__).info(f"[API REQUEST - VIDEO] Fetching from API: {video_id}")
        asyncio.create_task(self._cache_video(video_id))

        return await self._get_direct_download(video_id, media_type="video")

    async def _cache_video(self, video_id: str):
        try:
            existing = await media_data.find_one(
                {"video_id": video_id, "type": "video"}
            )
            if existing and existing.get("status") in ["processing", "ready"]:
                return

            await media_data.update_one(
                {"video_id": video_id, "type": "video"},
                {"$set": {"status": "processing", "updated_at": datetime.utcnow()}},
                upsert=True,
            )

            file_path = await self._download_external(video_id, media_type="video")

            if not file_path:
                await media_data.delete_one({"video_id": video_id, "type": "video"})
                return

            assistant = get_assistant()
            if not assistant:
                return

            LOGGER(__name__).info(f"[UPLOADING] Telegram Channel uploading: {video_id}")
            msg = await assistant.send_video(
                DATA_CHANNEL, video=file_path, caption=f"ID: {video_id}"
            )

            await media_data.update_one(
                {"video_id": video_id, "type": "video"},
                {
                    "$set": {
                        "video_id": video_id,
                        "type": "video",
                        "file_id": msg.video.file_id,
                        "file_unique_id": msg.video.file_unique_id,
                        "message_id": msg.id,
                        "title": msg.video.file_name or f"{video_id}.mp4",
                        "size": msg.video.file_size,
                        "status": "ready",
                        "updated_at": datetime.utcnow(),
                    }
                },
                upsert=True,
            )
            LOGGER(__name__).info(f"[DB SAVED] Video cached in DB: {video_id}")

            if os.path.exists(file_path):
                os.remove(file_path)

        except Exception as e:
            LOGGER(__name__).error(f"Video Cache Error: {e}")

    async def _get_direct_download(self, video_id: str, media_type: str = "audio"):
        try:
            quality = 128 if media_type == "audio" else 480
            stream_url = (
                f"{API_URL}/stream/{video_id}?key={API_KEY}"
                f"&type={media_type}&quality={quality}"
            )
            return stream_url
        except Exception as e:
            LOGGER(__name__).error(f"Direct URL Error: {e}")
            return None

    async def _download_external(self, video_id: str, media_type: str = "audio"):
        DOWNLOAD_DIR = "downloads"
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        ext = "mp3" if media_type == "audio" else "mp4"
        file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.{ext}")

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return file_path

        session = await self._get_session()

        quality = 128 if media_type == "audio" else 480
        try:
            async with session.get(
                f"{API_URL}/stream/{video_id}?key={API_KEY}&type={media_type}&quality={quality}",
                timeout=aiohttp.ClientTimeout(total=600),
            ) as resp:

                if resp.status != 200:
                    return None

                with open(file_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(262144):
                        f.write(chunk)

            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                return file_path

            return None

        except Exception as e:
            LOGGER(__name__).error(f"Download Error: {e}")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass
            return None
