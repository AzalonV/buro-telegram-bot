from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import and_f, or_f

from texts import JOIN_UNION_TEXT, ABOUT_TRADE_UNION
from buttons.keyboard import KeyboardButtons

union_router = Router()

@union_router.message(F.chat.type ==  "private", or_f(Command("about_union"), F.text == "Про профспілку ℹ️"))
async def about_union(message: Message):
    keyboard = await KeyboardButtons.create_union_buttons()
    await message.answer(text="Що вас цікавить?", reply_markup=keyboard)

@union_router.message(F.chat.type ==  "private", F.text == "Профком 🦁")
async def about_union(message: Message):
    await message.answer(text=ABOUT_TRADE_UNION)

@union_router.message(F.chat.type ==  "private", F.text == "Профбюро 🔹")
async def about_union(message: Message):
    await message.answer(text="Профбюро - представник профкому на факульеті (буде більше тексту)")

@union_router.message(F.chat.type ==  "private", F.text == "Вступ в профспілку/профбюро 📜")
async def about_union(message: Message):
    await message.answer(text = JOIN_UNION_TEXT, parse_mode = ParseMode.HTML)