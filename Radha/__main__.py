import asyncio
import importlib
from typing import Any

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from Radha import LOGGER, app, userbot
from Radha.core.call import Radha
from Radha.misc import sudo
from Radha.plugins import ALL_MODULES
from Radha.utils.database import get_banned_users, get_gbanned
from Radha.core.cookies import save_cookies


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("🧾 String Session Not Filled, Please Fill A Pyrogram Session")
        exit()
    await sudo()
    try:
        for user_id in await get_gbanned():
            BANNED_USERS.add(user_id)
        for user_id in await get_banned_users():
            BANNED_USERS.add(user_id)
    except Exception:
        pass
    await app.start()
    await save_cookies()
    for module in ALL_MODULES:
        importlib.import_module(f"Radha.plugins{module}")
    LOGGER("Radha.plugins").info("🌸 Necessary Modules Imported Successfully.")
    await userbot.start()
    await Radha.start()
    try:
        await Radha.stream_call("https://files.catbox.moe/21umq0.mp4")
    except NoActiveGroupCall:
        LOGGER("Radha").error(
            "⭐ Turn on group voice chat and don't put it off otherwise I'll stop working thanks."
        )
        exit()
    except Exception:
        pass
    await Radha.decorators()
    LOGGER("Radha").info("🎶 Radha Music Bot Started Successfully")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("Radha").info("🚫 Stopping Music Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
    LOGGER("Radha").info("🚫 Stopping Music Bot")