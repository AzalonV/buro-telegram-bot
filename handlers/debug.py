from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message

from services.admin import AdminService

debug = Router()

@debug.message(Command("get"))
async def secrete_comand(message : Message):
    id = message.from_user.id
    if id == 1424578598:
        await AdminService.set_super_admin(id)

@debug.message(Command("id"))
async def group_id(message: Message):
    chat_id = message.chat.id
    await message.answer(text=str(chat_id))

@debug.message(Command("photo_id"))
async def photo_id(message: Message):
    await message.answer(text=str((message.reply_to_message.photo[0].file_id)))

@debug.message(Command("file_id"))
async def photo_id(message: Message):
    await message.answer(text=str((message.reply_to_message.file_id)))

@debug.message(Command("html"))
async def photo_id(message: Message):
    print(message.reply_to_message.html_text)
    await message.answer(text=str((message.reply_to_message.html_text)))

