from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.filters import and_f, or_f
from aiogram.fsm.context import FSMContext

from buttons.keyboard import KeyboardButtons

roolback_router = Router()

@roolback_router.message(F.chat.type ==  "private", F.text == "Назад 🔙")
async def about_union(message: Message):
    keyboard = await KeyboardButtons.create_start_buttons()
    await message.answer(text="Меню", reply_markup=keyboard)

@roolback_router.message(F.chat.type ==  "private", or_f(Command("cancel"), F.text == "Скасувати ❌"))
async def cancel_action(message: Message, state : FSMContext):
    current_state = await state.get_state()
    keyboard = await KeyboardButtons.create_start_buttons()
    await message.answer(text="Дія скасована", reply_markup=keyboard)
    if current_state is None:
        return
    
    await state.clear()
