from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters import and_f, or_f
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from services.user import UserService
from buttons.keyboard import KeyboardButtons
from misc.state import StatesProfile



profile_router = Router()

@profile_router.message(F.chat.type ==  "private", or_f(Command("my_profile"), F.text == "Мій профіль 👤"))
async def my_profile(message: Message):
    id = message.from_user.id
    text = await UserService.formulate_profile_text(id)
    buttons = await KeyboardButtons.create_profile_buttons()
    await message.answer(text=text, reply_markup=buttons)

@profile_router.message(F.chat.type ==  "private", or_f(Command("change_group"), F.text == "Змінити академічну групу ✍️"))
async def change_group(message: Message, state : FSMContext):
    button = await KeyboardButtons.create_cancel_button()
    await state.set_state(StatesProfile.GET_ACADEMIC_GROUP)
    await message.answer(text="Приклад групи: МТА-11C\nВведіть академічну групу:", reply_markup=button)

@profile_router.message(StatesProfile.GET_ACADEMIC_GROUP, F.chat.type ==  "private", F.text)
async def set_group(message: Message, state : FSMContext):
    id = message.from_user.id
    text = message.text.upper()
    keyboard = await KeyboardButtons.create_profile_buttons()
    await UserService.set_academic_group(id=id, group=text)
    await state.clear()
    await message.answer("Академічна група змінена!", reply_markup=keyboard)
