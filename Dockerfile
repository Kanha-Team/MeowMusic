# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved

FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
        curl \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app/

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev \
    && uv pip uninstall pyrogram \
    && uv pip install --reinstall kurigram

# PyTgCalls & Pyrogram Error Fixes (Permanent Patch)
RUN sed -i "s/from pyrogram.errors import GroupcallForbidden/# from pyrogram.errors import GroupcallForbidden/g" /app/.venv/lib/python3.12/site-packages/pytgcalls/mtproto/pyrogram_client.py || true
RUN sed -i "s/from pyrogram.errors import GroupcallInvalid/# from pyrogram.errors import GroupcallInvalid/g" /app/.venv/lib/python3.12/site-packages/pytgcalls/mtproto/pyrogram_client.py || true

ENV PATH="/app/.venv/bin:${PATH}"

COPY . /app/

CMD ["bash", "start"]
