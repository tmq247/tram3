from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message, CallbackQuery

from Radha import app
from Radha.utils import help_pannel
from Radha.utils.database import get_lang
from Radha.utils.decorators.language import LanguageStart, languageCB
from Radha.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT, OWNER_ID
from strings import get_string, helpers

# /help in private chat or when returning from settings
@app.on_message(filters.command("help") & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client: app, update: Union[Message, CallbackQuery]):
    is_callback = isinstance(update, CallbackQuery)

    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        await update.edit_message_text(_["help_1"], reply_markup=keyboard)
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=_["help_1"],
            reply_markup=keyboard
        )

# /help in group chat
@app.on_message(filters.command("help") & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client: app, message: Message, _: dict):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))

# Help Callback Handler
@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client: app, callback_query: CallbackQuery, _: dict):
    try:
        await callback_query.answer()
    except:
        pass

    cb_data = callback_query.data.strip().split(None, 1)
    if len(cb_data) < 2:
        return await callback_query.answer("Invalid help request.", show_alert=True)

    cb = cb_data[1]
    keyboard = help_back_markup(_)

    HELP_SECTIONS = {
        "hb1": helpers.HELP_1,
        "hb2": helpers.HELP_2,
        "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4,
    }

    if cb in HELP_SECTIONS:
        return await callback_query.edit_message_text(HELP_SECTIONS[cb], reply_markup=keyboard)

    return await callback_query.answer("Unknown help section.", show_alert=True)