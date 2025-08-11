import os
import asyncio
import yt_dlp
from time import time
from pyrogram import filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch
import requests

from Radha import app  # your bot instance

# Anti-spam settings
user_last_message_time = {}
user_command_count = {}
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5

COOKIES_FILE = 'cookies/cookies.txt'


@app.on_message(filters.command("song"))
async def download_song(_, message: Message):
    user_id = message.from_user.id
    current_time = time()

    # Anti-spam logic
    last_time = user_last_message_time.get(user_id, 0)
    if current_time - last_time < SPAM_WINDOW_SECONDS:
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        user_last_message_time[user_id] = current_time
        if user_command_count[user_id] > SPAM_THRESHOLD:
            warn = await message.reply_text(
                f"{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴀᴠᴏɪᴅ sᴘᴀᴍᴍɪɴɢ. ᴛʀʏ ᴀɢᴀɪɴ ɪɴ 5 sᴇᴄᴏɴᴅs."
            )
            await asyncio.sleep(3)
            await warn.delete()
            return
    else:
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    # Extract query
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("**Usage: /song [Song Name]**")
        return

    m = await message.reply("🔍 Searching...")

    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            return await m.edit("❌ No results found. Try a different song name.")

        video = results[0]
        title = video["title"]
        duration = video["duration"]
        views = video["views"]
        channel_name = video["channel"]
        link = f"https://youtube.com{video['url_suffix']}"
        thumbnail_url = video["thumbnails"][0]

        # Sanitize file names
        safe_title = "".join(i for i in title if i.isalnum() or i in (" ", "_", "-")).strip()
        thumb_name = f"{safe_title}.jpg"

        # Download thumbnail
        thumb = requests.get(thumbnail_url, allow_redirects=True)
        with open(thumb_name, "wb") as f:
            f.write(thumb.content)

        await m.edit(f"📥 Downloading `{title}`\n⏱ Duration: {duration}")

        ydl_opts = {
            "format": "bestaudio[ext=m4a]",
            "noplaylist": True,
            "quiet": True,
            "cookiefile": COOKIES_FILE,
        }

        # Download audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.download([link])

        # Convert duration to seconds
        try:
            dur = sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration.split(":"))))
        except:
            dur = 0  # fallback

        await m.edit("📤 Uploading...")

        await message.reply_audio(
            audio_file,
            title=title,
            performer=channel_name,
            duration=dur,
            thumb=thumb_name,
            caption=(
                f"🎵 <b>{title}</b>\n"
                f"👤 <b>Requested by:</b> {message.from_user.mention}\n"
                f"👁‍🗨 <b>Views:</b> {views}\n"
                f"📡 <b>Channel:</b> {channel_name}"
            ),
        )

        await m.delete()

    except Exception as e:
        await m.edit("❗ An error occurred during processing.")
        print(f"[ERROR] {e}")

    finally:
        # Clean up
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
            if os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as e:
            print(f"[Cleanup Error] {e}")