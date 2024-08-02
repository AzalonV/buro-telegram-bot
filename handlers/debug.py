from aiogram import types, Router, F
from aiogram.filters.command import Command

debug = Router()

@debug.message(Command("id"))
async def group_id(message: types.message):
    chat_id = message.chat.id
    await message.answer(text=str(chat_id))

@debug.message(Command("photo_id"))
async def photo_id(message: types.message):
    await message.answer(text=str((message.reply_to_message.photo[0].file_id)))

@debug.message(Command("file_id"))
async def photo_id(message: types.message):
    await message.answer(text=str((message.reply_to_message.file_id)))

@debug.message(Command("html"))
async def photo_id(message: types.message):
    print(message.reply_to_message.html_text)
    await message.answer(text=str((message.reply_to_message.html_text)))

