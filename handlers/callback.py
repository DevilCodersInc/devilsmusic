from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from helpers.wrappers import admins_only
import sira

from tgcalls import pytgcalls



@Client.on_callback_query(filters.regex("close"))
async def close(client: Client, query: CallbackQuery):
    await query.message.delete()



@Client.on_callback_query(filters.regex("leavevc"))
async def leavevc(client: Client, query: CallbackQuery):
    await query.edit_message_text("Left Voice Chat !")
    pytgcalls.leave_group_call(query.message.chat.id)


@Client.on_callback_query(filters.regex("skip"))
@admins_only
async def skip(client: Client, query: CallbackQuery):
    sira.task_done(query.message.chat.id)
    await query.message.edit_text("Processing ♻️")
    if sira.is_empty(query.message.chat.id):
        pytgcalls.leave_group_call(query.message.chat.id)
        await query.message.edit_text("nothing in queue")
    else:
        pytgcalls.change_stream(
            query.message.chat.id, sira.get(query.message.chat.id)["file_path"]
        )

        await query.message.edit_text("⏩ Skipped the current song.")
