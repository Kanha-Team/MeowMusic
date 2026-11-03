# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import os
import shutil

import git
from pyrogram import filters

from MeowMusic import app


@app.on_message(filters.command(["downloadrepo"]))
def download_repo(_, message):
    if len(message.command) != 2:
        message.reply_text(
            "Please provide the GitHub repository URL after the command. Example: /downloadrepo Repo Url "
        )
        return

    repo_url = message.command[1]
    zip_path = download_and_zip_repo(repo_url)

    if zip_path:
        with open(zip_path, "rb") as zip_file:
            message.reply_document(zip_file)
        os.remove(zip_path)
    else:
        message.reply_text("Unable to download the specified GitHub repository.")


def download_and_zip_repo(repo_url):
    try:
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_path = f"{repo_name}"

        # Clone the repository
        git.Repo.clone_from(repo_url, repo_path)

        # Create a zip file of the repository
        shutil.make_archive(repo_path, "zip", repo_path)

        return f"{repo_path}.zip"
    except Exception as e:
        print(f"Error downloading and zipping GitHub repository: {e}")
        return None
    finally:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
