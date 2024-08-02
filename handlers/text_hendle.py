from aiogram import types, Router, F

from aiogram.filters.command import Command
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import and_f, or_f

from config import FEEDBACK_MANAGER
from texts import ABOUT_TRADE_UNION
from database.sql import async_session_maker
from database.models.user import User
from services.user import UserService
from services.message import MessageService
from services.message import OwnCallback
from services.mailing import MalingServcise
from services.chat import ChatService
from bot import bot
from filters import isReplied

text_hendle = Router()

@text_hendle.message(F.chat.type ==  "private", CommandStart())
async def command_start_handler(message: Message):
    id = message.from_user.id
    keyboard = await create_start_buttons()
    if await UserService.is_exist(id) is False:
        async with async_session_maker() as session:
            await ChatService.add_chat_in_base(chat_id=id)
            new_user = User(id = id)
            session.add(new_user)
            await session.commit()
    await bot.send_message(message.from_user.id, f"Привітик, {message.from_user.full_name}!", reply_markup=keyboard)


async def create_start_buttons():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text = 'feedback ✉️'), 
        KeyboardButton(text = 'Івенти 🎉'), 
        KeyboardButton(text = 'Про бюро ℹ️')], 
        [KeyboardButton(text="Розклад 🗓️")]
        ], resize_keyboard=True)


@text_hendle.message(F.chat.type ==  "private", or_f(Command("event"), F.text == "Івенти 🎉"))
async def event(message: types.message):
    id = message.from_user.id
    events = await MessageService.get_events()
    current_page = len(events) - 1
    buttons = await MessageService.create_event_buttons(page=current_page, max=current_page, is_buuto_request=False)
    event = events[current_page]
    post = await MalingServcise.formulate_event_post(text=event.text, time=event.time, date=event.date, photo=event.photo)
    await bot.send_photo(chat_id = id,  photo=post.photo, caption=post.text, reply_markup=buttons.as_markup())


@text_hendle.message(F.chat.type ==  "private", or_f(Command("about_union"), F.text == "Про бюро ℹ️"))
async def about_union(message: types.message):
    await message.answer(text=ABOUT_TRADE_UNION)

@text_hendle.message(F.chat.id == FEEDBACK_MANAGER, isReplied())
async def feedback_answer(message: types.message):
     message_id = message.reply_to_message.message_id
     answer = await MessageService.request_feedback_message(message_id)
     if answer:
          user_id = answer.user_id
          reply = answer.from_user_message_id
          await bot.send_message(chat_id=user_id, reply_to_message_id=reply, text = "ВІдповідь на ваше звернення:\n" + message.text)
          await bot.edit_message_text(chat_id=FEEDBACK_MANAGER, message_id=message_id, text=message.reply_to_message.text + " ✅")

# async def create_menu_buttons():
#     callback_data_feedback = OwnCallback(type = "feedback", page = 0).pack()
#     callback_data_event = OwnCallback(type = "event_page", page = 0).pack()
#     callback_data_buro = OwnCallback(type = "trade_union", page = 0).pack()
#     menu_builder = InlineKeyboardBuilder()
#     menu_buttons = [types.InlineKeyboardButton(text="feedback", callback_data=callback_data_feedback),
#                     types.InlineKeyboardButton(text="Івенти", callback_data=callback_data_event),
#                     types.InlineKeyboardButton(text="Про бюро", callback_data=callback_data_buro)]
#     for button in menu_buttons:
#         menu_builder.add(button)
#     menu_builder.adjust(3)
#     return menu_builder

# @text_hendle.message(F.chat.type ==  "private", Command("menu"))
# async def menu(message: types.message):
#     buttons = await create_menu_buttons()
#     button1 = KeyboardButton(text = 'test')
#     keyboard = ReplyKeyboardMarkup(keyboard=[[button1]])
#     await message.answer("Меню навігації:", reply_markup=keyboard)
