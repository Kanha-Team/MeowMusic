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

############.....


@app.on_message(filters.command(["ip"]))
def ip_info(_, message):
    if len(message.command) != 2:
        message.reply_text(
            "Please provide an IP address after the command. Example: /ip 8.8.8.8"
        )
        return

    ip_address = message.command[1]
    info = get_ip_info(ip_address)

    if info:
        message.reply_text(info)
    else:
        message.reply_text("Unable to fetch information for the provided IP address.")


def get_ip_info(ip_address):
    api_url = f"https://api.safone.dev/ipinfo?ip={ip_address}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            info = f"IP: {data['ip']}\nCountry: {data['country']}\nCity: {data['city']}\nISP: {data['isp']}"
            return info
    except Exception as e:
        print(f"Error fetching IP information: {e}")
