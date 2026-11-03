# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from MeowMusic.utils.buttons import btn


class BUTTONS:
    MBUTTON = [
        [
            btn("ɢꝛσυᴘs", callback_data="mplus HELP_Group"),
            btn("ɪηғσ", callback_data="mplus HELP_Info"),
            btn("sᴛɪᴄᴋєꝛs", callback_data="mplus HELP_Sticker"),
        ],
        [
            btn("ᴧᴅϻɪηs", callback_data="mplus UPGRADING"),
            btn("ғɪʟᴛєꝛs", callback_data="mplus HELP_FILTERS"),
            btn("ᴛᴧɢ-ᴧʟʟ", callback_data="mplus HELP_TagAll"),
        ],
        [
            btn("ᴡєʟᴄσϻє", callback_data="mplus HELP_WELCOME"),
            btn("ᴄʟєᴧη", callback_data="mplus HELP_CLEAN"),
            btn("ᴧᴄᴛɪση", callback_data="mplus HELP_Action"),
        ],
        [
            btn("ηɪɢʜᴛϻσᴅє", callback_data="mplus HELP_NIGHTMODE"),
            btn("ꝛєᴘσꝛᴛs", callback_data="mplus HELP_REPORTS"),
            btn("ɪϻᴘσsᴛєꝛ", callback_data="mplus HELP_Imposter"),
        ],
        [
            btn("ʙᴧᴄᴋ", callback_data="help_menu_main"),
            btn("ηєxᴛ", callback_data="nextmanagement_help"),
        ],
    ]

    MBUTTON_SECOND = [
        [
            btn("ᴧғᴋ", callback_data="mplus HELP_AFK"),
            btn("ɢᴧϻєs", callback_data="mplus HELP_Game"),
            btn("ᴄʜᴧᴛɢᴘᴛ", callback_data="mplus HELP_ChatGPT"),
        ],
        [
            btn("ᴛᴛs", callback_data="mplus HELP_TTS"),
            btn("ǫυσᴛʟʏ", callback_data="mplus HELP_Q"),
            btn("ғυη", callback_data="mplus HELP_Fun"),
        ],
        [
            btn("ғσηᴛ", callback_data="mplus HELP_Font"),
            btn("ᴛꝛυᴛʜ-ᴅᴧꝛє", callback_data="mplus HELP_TD"),
            btn("ʙυɢ", callback_data="mplus HELP_BUG"),
        ],
        [
            btn("ɢɪᴛʜυʙ", callback_data="mplus HELP_GITHUB"),
            btn("ʜᴧsᴛᴧɢ", callback_data="mplus HELP_HT"),
            btn("ᴛ-ɢꝛᴧᴘʜ", callback_data="mplus HELP_TG"),
        ],
        [
            btn("<", callback_data="secondbackmanagement_help"),
            btn("ʜσϻє", callback_data="help_menu_main"),
            btn(">", callback_data="thirdmanagement_help"),
        ],
    ]

    MBUTTON_THIRD = [
        [
            btn("ɪϻᴧɢє", callback_data="mplus HELP_Image"),
            btn("ᴡєʙsʜσᴛ", callback_data="mplus HELP_WEBSHOT"),
            btn("ᴛꝛᴧηsʟᴧᴛσꝛ", callback_data="mplus HELP_TRANSLATE"),
        ],
        [
            btn("ϻσηɢσᴅʙ", callback_data="mplus HELP_MONGO"),
            btn("sєᴧꝛᴄʜ", callback_data="mplus HELP_Search"),
            btn("єxᴛꝛᴧ", callback_data="mplus HELP_Extra"),
        ],
        [
            btn("ғυη ᴧᴄᴛɪση", callback_data="mplus FUNACTION_HELP"),
            btn("ǫυɪᴢ", callback_data="mplus HELP_QUIZ"),
            btn("ᴡʜɪsᴘєꝛ", callback_data="mplus HELP_WHISPER"),
        ],
        [
            btn("ᴡᴧɪғυ ηᴧϻє", callback_data="mplus HELP_WAIFU"),
            btn("ᴄϻᴅ ʟσᴄᴋ", callback_data="mplus CMDLOCK_HELP"),
        ],
        [btn(text="ʟσɢɢєꝛ", callback_data="mplus HELP_LOGGER")],
        [
            btn("<", callback_data="nextmanagement_help"),
            btn("ʜσϻє", callback_data="help_menu_main"),
            btn(">", callback_data="management_help"),
        ],
    ]
