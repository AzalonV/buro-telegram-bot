from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message

from buttons.keyboard import KeyboardButtons
from middlwares.start import Starter

start_router = Router()

start_router.message.middleware(Starter())

@start_router.message(F.chat.type ==  "private", Command("start"))
async def command_start_handler(message: Message):
    full_name = message.from_user.full_name
    keyboard = await KeyboardButtons.create_start_buttons()
    await message.answer(text = f"Привітик, {full_name}!", reply_markup=keyboard)