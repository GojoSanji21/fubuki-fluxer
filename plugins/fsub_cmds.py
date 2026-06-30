import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS
from database.database import add_fsub, del_fsub, get_fsubs, is_fsub
from bot import Bot

@Bot.on_message(filters.private & filters.command('add_fsub') & filters.user(ADMINS))
async def add_fsub_cmd(client: Bot, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/add_fsub [chat_id]`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ • ᴄʟᴏsᴇ • ]", callback_data="close")]]))

    chat_id = message.command[1]

    try:
        chat_id = int(chat_id)
        chat = await client.get_chat(chat_id)
        title = chat.title
        await add_fsub(chat_id, title)

        text = f"<b>ᴄʜᴀɴɴᴇʟ ᴀᴅᴅᴇᴅ</b>\n<b>\"{title}\"</b>\nID: <code>{chat_id}</code>"
        await message.reply(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ • ᴄʟᴏsᴇ • ]", callback_data="close")]]))
    except ValueError:
        await message.reply("Invalid Chat ID format.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ • ᴄʟᴏsᴇ • ]", callback_data="close")]]))
    except Exception as e:
        await message.reply(f"Error: {str(e)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ • ᴄʟᴏsᴇ • ]", callback_data="close")]]))

@Bot.on_message(filters.private & filters.command('del_fsub') & filters.user(ADMINS))
async def del_fsub_cmd(client: Bot, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/del_fsub [chat_id]`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ • ᴄʟᴏsᴇ • ]", callback_data="close")]]))

    chat_id = message.command[1]

    try:
        chat_id = int(chat_id)
        if not await is_fsub(chat_id):
            return await message.reply("Channel not found in database.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ • ᴄʟᴏsᴇ • ]", callback_data="close")]]))

        try:
            chat = await client.get_chat(chat_id)
            title = chat.title
        except:
            title = "Unknown"

        await del_fsub(chat_id)

        text = f"<b>ᴄʜᴀɴɴᴇʟ ʀᴇᴍᴏᴠᴇᴅ</b>\n<b>\"{title}\"</b>\nID: <code>{chat_id}</code>"
        await message.reply(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ • ᴄʟᴏsᴇ • ]", callback_data="close")]]))
    except ValueError:
        await message.reply("Invalid Chat ID format.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ • ᴄʟᴏsᴇ • ]", callback_data="close")]]))
    except Exception as e:
        await message.reply(f"Error: {str(e)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ • ᴄʟᴏsᴇ • ]", callback_data="close")]]))

@Bot.on_message(filters.private & filters.command('list_fsub') & filters.user(ADMINS))
async def list_fsub_cmd(client: Bot, message: Message):
    try:
        fsubs = await get_fsubs()
        if not fsubs:
            return await message.reply("<b>ᴄʜᴀɴɴᴇʟ ʟɪꜱᴛ:</b>\nNo channels found.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ • ᴄʟᴏsᴇ • ]", callback_data="close")]]))

        text = "<b>ᴄʜᴀɴɴᴇʟ ʟɪꜱᴛ:</b>\n"
        for fsub in fsubs:
            text += f"<b>\"{fsub['title']}\"</b> - <code>{fsub['chat_id']}</code>\n"

        await message.reply(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ • ᴄʟᴏsᴇ • ]", callback_data="close")]]))
    except Exception as e:
        await message.reply(f"Error: {str(e)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ • ᴄʟᴏsᴇ • ]", callback_data="close")]]))
