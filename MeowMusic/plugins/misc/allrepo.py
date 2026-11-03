# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import requests
from pyrogram import filters

from MeowMusic import app


# Function to chunk the repository info into smaller parts
def chunk_string(text, chunk_size):
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


@app.on_message(filters.command("allrepo"))
async def all_repo_command(client, message):
    try:
        # Check if there is a GitHub username after the /giverepo command
        if len(message.command) > 1:
            github_username = message.command[1]

            # Fetch information about all repositories of the GitHub user
            repo_info = get_all_repository_info(github_username)

            # Split repository info into smaller chunks
            chunked_repo_info = chunk_string(
                repo_info, 4000
            )  # Split into chunks of 4000 characters

            # Send the repository information in chunks as separate messages
            for chunk in chunked_repo_info:
                await message.reply_text(chunk)
        else:
            await message.reply_text(
                "Please enter a GitHub username after the /allrepo command."
            )
    except Exception as e:
        await message.reply_text(f"An error occurred: {e!s}")


#######


def get_all_repository_info(github_username):
    # Set up the GitHub API URL for user repositories
    github_api_url = f"https://api.github.com/users/{github_username}/repos"

    # Perform the request to the GitHub API
    response = requests.get(github_api_url)
    data = response.json()

    # Extract relevant information from the response
    repo_info = "\n\n".join(
        [
            f"Repository: {repo['full_name']}\n"
            f"Description: {repo['description']}\n"
            f"Stars: {repo['stargazers_count']}\n"
            f"Forks: {repo['forks_count']}\n"
            f"URL: {repo['html_url']}"
            for repo in data
        ]
    )

    return repo_info
