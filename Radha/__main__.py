import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from Radha import LOGGER, app, userbot
from Radha.core.call import Radha
from Radha.misc import sudo
from Radha.plugins import ALL_MODULES
from Radha.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("String Session Not Filled, Please Fill A Pyrogram Session")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("Radha.plugins" + all_module)
    LOGGER("Radha.plugins").info("All features have been successfully loaded")
    await userbot.start()
    await Radha.start()
    try:
        await Radha.stream_call("https://files.catbox.moe/21umq0.mp4")
    except NoActiveGroupCall:
        LOGGER("Radha").error(
            "Please Start Your Log Group VoiceChat Or Channel\n\nRadha Bot Stopped"
        )
        exit()
    except:
        pass
    await Radha.decorators()
    LOGGER("Radha").info(
        "Made By @RadhaSprt"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("Radha").info("Radha Bot Stopped")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
