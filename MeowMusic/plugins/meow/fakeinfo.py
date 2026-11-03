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


@app.on_message(filters.command("fake") & filters.private)
async def address(_, message):
    query = message.text.split(maxsplit=1)[1].strip()
    url = f"https://randomuser.me/api/?nat={query}"
    response = requests.get(url)
    data = response.json()

    if "results" in data:
        user_data = data["results"][0]

        name = f"{user_data['name']['title']} {user_data['name']['first']} {user_data['name']['last']}"
        address = f"{user_data['location']['street']['number']} {user_data['location']['street']['name']}"
        city = user_data["location"]["city"]
        state = user_data["location"]["state"]
        country = user_data["location"]["country"]
        postal = user_data["location"]["postcode"]
        email = user_data["email"]
        phone = user_data["phone"]
        picture_url = user_data["picture"]["large"]

        caption = f"""
﹝⌬﹞**ɴᴀᴍᴇ** ⇢ {name}
﹝⌬﹞**ᴀᴅᴅʀᴇss** ⇢ {address}
﹝⌬﹞**ᴄᴏᴜɴᴛʀʏ** ⇢ {country}
﹝⌬﹞**ᴄɪᴛʏ** ⇢ {city}
﹝⌬﹞**sᴛᴀᴛᴇ** ⇢ {state}
﹝⌬﹞**ᴘᴏsᴛᴀʟ** ⇢ {postal}
﹝⌬﹞**ᴇᴍᴀɪʟ** ⇢ {email}
﹝⌬﹞**ᴘʜᴏɴᴇ** ⇢ {phone}

        """

        await message.reply_photo(photo=picture_url, caption=caption)
    else:
        await message.reply_text("ᴏᴏᴘs ɴᴏᴛ ғᴏᴜɴᴅ ᴀɴʏ ᴀᴅᴅʀᴇss.")
