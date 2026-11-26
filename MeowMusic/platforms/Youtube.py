# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import asyncio
import os
import re
from urllib.parse import parse_qs, urlparse

import aiohttp
import yt_dlp
from py_yt import Playlist, VideosSearch
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

API_URL = "http://201.18.222.133"
API_KEY = "INFLEX37954428D"

DOWNLOAD_DIR = "downloads"
_AUDIO_EXTS = ("ogg", "mp3", "m4a", "webm", "opus")


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


def _extract_video_id(link: str) -> str | None:
    if not link:
        return None
    link = link.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{6,20}", link):
        return link
    parsed = urlparse(link)
    host = (parsed.netloc or "").lower()
    path = (parsed.path or "").strip("/")
    if "youtu.be" in host and path:
        return path.split("/")[0]
    if "youtube.com" in host or "youtube-nocookie.com" in host:
        qs = parse_qs(parsed.query)
        if qs.get("v"):
            return qs["v"][0]
        parts = path.split("/")
        if len(parts) >= 2 and parts[0] in ("shorts", "live", "embed", "v"):
            return parts[1]
    if "v=" in link:
        return link.split("v=")[-1].split("&")[0]
    return None


def _normalize_yt_url(link: str) -> tuple[str | None, str | None]:
    video_id = _extract_video_id(link)
    if not video_id:
        return None, None
    return video_id, f"https://www.youtube.com/watch?v={video_id}"


async def _request_inflex_media(
    session: aiohttp.ClientSession,
    yt_url: str,
    media_type: str,
    timeout_sec: int = 30,
    retries: int = 2,
) -> dict | None:
    headers = {"X-API-KEY": API_KEY}
    payload = {"url": yt_url, "type": media_type}
    for attempt in range(retries + 1):
        try:
            async with session.post(
                f"{API_URL}/download",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=timeout_sec),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json(content_type=None)
                    if isinstance(data, dict) and data.get("status") == "success":
                        return data
                if resp.status in (401, 403, 404):
                    return None
        except Exception:
            pass
        if attempt < retries:
            await asyncio.sleep(0.5)
    return None


async def _download_to_file(
    session: aiohttp.ClientSession,
    url: str,
    dest_path: str,
    timeout_sec: int,
    retries: int = 2,
) -> bool:
    part_path = f"{dest_path}.part"
    for attempt in range(retries + 1):
        try:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=timeout_sec)
            ) as resp:
                if resp.status in (200, 206):
                    with open(part_path, "wb") as f:
                        async for chunk in resp.content.iter_chunked(131072):
                            f.write(chunk)
                    if os.path.exists(part_path) and os.path.getsize(part_path) > 1024:
                        os.replace(part_path, dest_path)
                        return True
        except Exception:
            pass
        if os.path.exists(part_path):
            try:
                os.remove(part_path)
            except Exception:
                pass
        if attempt < retries:
            await asyncio.sleep(0.5)
    return False


async def _mux_av(video_path: str, audio_path: str, output_path: str) -> bool:
    tmp_out = f"{output_path}.mux.mp4"
    for audio_codec in ("copy", "aac"):
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            video_path,
            "-i",
            audio_path,
            "-c:v",
            "copy",
            "-c:a",
            audio_codec,
            "-movflags",
            "+faststart",
            tmp_out,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        if (
            proc.returncode == 0
            and os.path.exists(tmp_out)
            and os.path.getsize(tmp_out) > 1024
        ):
            os.replace(tmp_out, output_path)
            return True
        if os.path.exists(tmp_out):
            try:
                os.remove(tmp_out)
            except Exception:
                pass
    return False


async def download_song(link: str) -> str | None:
    video_id, yt_url = _normalize_yt_url(link)
    if not video_id or not yt_url:
        return None

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    for ext in _AUDIO_EXTS:
        cached = os.path.join(DOWNLOAD_DIR, f"{video_id}.{ext}")
        if os.path.exists(cached) and os.path.getsize(cached) > 1024:
            return cached

    file_path = None
    try:
        async with aiohttp.ClientSession() as session:
            data = await _request_inflex_media(session, yt_url, "audio", timeout_sec=60)
            if not data:
                return None
            audio_url = data.get("audio_url") or data.get("stream_url")
            if not audio_url:
                return None

            api_name = data.get("file_name") or ""
            ext = os.path.splitext(api_name)[1].lstrip(".").lower()
            if ext not in _AUDIO_EXTS:
                ext = "ogg"
            file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.{ext}")

            if await _download_to_file(session, audio_url, file_path, timeout_sec=300):
                return file_path
            return None
    except Exception:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        return None


async def download_video(link: str) -> str | None:
    video_id, yt_url = _normalize_yt_url(link)
    if not video_id or not yt_url:
        return None

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

    if os.path.exists(file_path) and os.path.getsize(file_path) > 1024:
        return file_path

    tmp_video = os.path.join(DOWNLOAD_DIR, f"{video_id}.video.tmp")
    tmp_audio = os.path.join(DOWNLOAD_DIR, f"{video_id}.audio.tmp")
    try:
        async with aiohttp.ClientSession() as session:
            data = await _request_inflex_media(session, yt_url, "video", timeout_sec=90)
            if not data:
                return None
            video_url = data.get("video_url") or data.get("stream_url")
            audio_url = data.get("audio_url")
            if not video_url:
                return None

            if audio_url:
                v_ok, a_ok = await asyncio.gather(
                    _download_to_file(session, video_url, tmp_video, timeout_sec=600),
                    _download_to_file(session, audio_url, tmp_audio, timeout_sec=300),
                )
                if not v_ok or not a_ok:
                    return None
                if await _mux_av(tmp_video, tmp_audio, file_path):
                    return file_path
                return None

            if await _download_to_file(session, video_url, file_path, timeout_sec=600):
                return file_path
            return None
    except Exception:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        return None
    finally:
        for tmp in (tmp_video, tmp_audio):
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: bool | str | None = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> str | None:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset : entity.offset + entity.length]
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: bool | str | None = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            duration_sec = int(time_to_seconds(duration_min)) if duration_min else 0
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: bool | str | None = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["title"]

    async def duration(self, link: str, videoid: bool | str | None = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["duration"]

    async def thumbnail(self, link: str, videoid: bool | str | None = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["thumbnails"][0]["url"].split("?")[0]

    async def video(self, link: str, videoid: bool | str | None = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            downloaded_file = await download_video(link)
            if downloaded_file:
                return 1, downloaded_file
            return 0, "Video download failed"
        except Exception as e:
            return 0, f"Video download error: {e}"

    async def playlist(self, link, limit, user_id, videoid: bool | str | None = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            plist = await Playlist.get(link)
        except Exception:
            return []
        videos = plist.get("videos") or []
        ids = []
        for data in videos[:limit]:
            if not data:
                continue
            vid = data.get("id")
            if not vid:
                continue
            ids.append(vid)
        return ids

    async def track(self, link: str, videoid: bool | str | None = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid

    async def formats(self, link: str, videoid: bool | str | None = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        ytdl_opts = {"quiet": True}
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    if "dash" not in str(format["format"]).lower():
                        formats_available.append(
                            {
                                "format": format["format"],
                                "filesize": format.get("filesize"),
                                "format_id": format["format_id"],
                                "ext": format["ext"],
                                "format_note": format["format_note"],
                                "yturl": link,
                            }
                        )
                except Exception:
                    continue
        return formats_available, link

    async def slider(
        self, link: str, query_type: int, videoid: bool | str | None = None
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        title = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        vidid = result[query_type]["id"]
        thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

    async def stream_url(self, link: str, videoid: bool | str | None = None):
        """Return a direct audio stream URL (no full download), or None on failure."""
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        _vid, yt_url = _normalize_yt_url(link)
        if yt_url:
            try:
                async with aiohttp.ClientSession() as session:
                    data = await _request_inflex_media(
                        session, yt_url, "audio", timeout_sec=30
                    )
                    if data:
                        direct_url = data.get("audio_url") or data.get("stream_url")
                        if direct_url:
                            return direct_url
            except Exception:
                pass

        def _extract():
            opts = {"quiet": True, "format": "bestaudio/best", "noplaylist": True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(link, download=False)
                return info.get("url")

        try:
            return await asyncio.to_thread(_extract)
        except Exception:
            return None

    async def download(
        self,
        link: str,
        mystic,
        video: bool | str | None = None,
        videoid: bool | str | None = None,
        songaudio: bool | str | None = None,
        songvideo: bool | str | None = None,
        format_id: bool | str | None = None,
        title: bool | str | None = None,
    ):
        if videoid:
            link = self.base + link
        try:
            if songvideo:
                return await download_video(link)
            if songaudio:
                return await download_song(link)
            if video:
                downloaded_file = await download_video(link)
            else:
                downloaded_file = await download_song(link)
            if downloaded_file:
                return downloaded_file, True
            return None, False
        except Exception:
            return (None if (songvideo or songaudio) else (None, False))


YouTube = YouTubeAPI()
