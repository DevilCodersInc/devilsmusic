from pyrogram import Client, filters
from pyrogram.types import Message

import tgcalls
from converter import convert
from youtube import download
import sira
from config import DURATION_LIMIT
from helpers.wrappers import errors
from helpers.errors import DurationLimitError


@Client.on_message(
    filters.command("play")
    & filters.group
    & ~ filters.edited
)
@errors
async def play(client: Client, message_: Message):
    audio = (message_.reply_to_message.audio or message_.reply_to_message.voice) if message_.reply_to_message else None

    res = await message_.reply_text("🔄 Processing...")

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {audio.duration / 60} minute(s)"
            )

        file_name = audio.file_id + audio.file_name.split(".")[-1]
        file_path = await convert(await message_.reply_to_message.download(file_name))
    else:
        messages = [message_]
        text = ""
        offset = None
        length = None

        if message_.reply_to_message:
            messages.append(message_.reply_to_message)

        for message in messages:
            if offset:
                break

            if message.entities:
                for entity in message.entities:
                    if entity.type == "url":
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break

        if offset == None:
            await res.edit_text("❕ You did not give me anything to play.")
            return

        url = text[offset:offset+length]

        file_path = await convert(download(url))

    try:
        is_playing = tgcalls.pytgcalls.is_playing(message_.chat.id)
    except:
        is_playing = False

    if is_playing:
        position = await sira.add(message_.chat.id, file_path)
        await res.edit_text(f"#️⃣ Queued at position {position}.")
    else:
        await res.edit_text("▶️ Playing...")
        tgcalls.pytgcalls.join_group_call(message_.chat.id, file_path, 48000)
async def deezer(requested_by, query):
    global playing
    m = await app.send_message(
        sudo_chat_id, text=f"Searching for `{query}` on Deezer"
    )
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://52.0.6.104:8000/deezer?query={query}&count=1"
            ) as resp:
                r = json.loads(await resp.text())
        title = r[0]["title"]
        duration = convert_seconds(int(r[0]["duration"]))
        thumbnail = r[0]["thumbnail"]
        artist = r[0]["artist"]
        url = r[0]["url"]
    except:
        await m.edit(
            "Found Literally Nothing, You Should Work On Your English!"
        )
        playing = False
        return
    await m.edit("Generating Thumbnail")
    await generate_cover_square(requested_by, title, artist, duration, thumbnail)

    await m.delete()
    m = await app.send_photo(
        chat_id=sudo_chat_id,
        photo="final.png",
        caption=f"Playing [{title}]({url}) Via Deezer.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Skip", callback_data="end")]]
        ),
        parse_mode="markdown",
    )

    s = await asyncio.create_subprocess_shell(
        f"mpv {url} --no-video",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await s.wait()
    await m.delete()
    playing = False


# Jiosaavn--------------------------------------------------------------------------------------

async def jiosaavn(requested_by, query):
    global playing
    res = await message_.reply_text("Searching 🔍🔎🔍🔎 for `{query}` on jio saavn")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://jiosaavnapi.bhadoo.uk/result/?query={query}"
            ) as resp:
                r = json.loads(await resp.text())
        sname = r[0]["song"]
        slink = r[0]["media_url"]
        ssingers = r[0]["singers"]
        sthumb = r[0]["image"]
        sduration = r[0]["duration"]
        sduration_converted = convert_seconds(int(sduration))
    except Exception as e:
        await m.edit(
            "Found Literally Nothing!, You Should Work On Your English."
        )
        print(str(e))
        playing = False
        return
    file_path=wget.download(slink)
    try:
        is_playing = tgcalls.pytgcalls.is_playing(message_.chat.id)
    except:
        is_playing = False

    if is_playing:
        position = await sira.add(message_.chat.id, file_path)
        await res.edit_text(f"#️⃣ Queued at position {position}.")
    else:
        await res.edit_text("▶️ Playing...")
        tgcalls.pytgcalls.join_group_call(message_.chat.id, file_path, 48000)
    await res.edit("Processing Thumbnail.")
    await generate_cover_square(requested_by, sname, ssingers, sduration_converted, sthumb)
    await res.delete()
    m = await client.send_photo(
        chat_id=sudo_chat_id,
        caption=f"Playing `{sname}` Via Jiosaavn",
        photo="final.png",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Skip", callback_data="end")]]
        ),
        parse_mode="markdown",
    )
