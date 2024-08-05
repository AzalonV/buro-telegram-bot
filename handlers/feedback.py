from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.filters import and_f, or_f
from aiogram.fsm.context import FSMContext
from aiogram import Bot

from config import FEEDBACK_MANAGER
from services.message import MessageService
from misc.state import StatesFeedback
from buttons.keyboard import KeyboardButtons
from filters import isReplied

feedback_router = Router()

@feedback_router.message(F.chat.type ==  "private", or_f(Command("feedback"), F.text == "feedback ✉️"))
async def feedback(message: Message, state : FSMContext):
    await state.set_state(StatesFeedback.GET_FEEDBACK_MESSAGE)
    cancel_button = await KeyboardButtons.create_cancel_button()
    await message.answer("Чудово напишіть нам свій відгук/пропозицію/побажання\n\nЗамітка: зворотній зв'язок анонімний!", reply_markup=cancel_button)

@feedback_router.message(StatesFeedback.GET_FEEDBACK_MESSAGE, F.chat.type ==  "private")
async def feedback_route(message: Message, bot : Bot, state : FSMContext):
    id = message.from_user.id
    await state.clear()
    keyboard = await KeyboardButtons.create_start_buttons()
    f_message = await bot.send_message(FEEDBACK_MANAGER, message.text)
    await MessageService.create_feedback_message(message_id=f_message.message_id,
                                                 from_user_message_id=message.message_id,
                                                 user_id=id)
    await bot.send_message(id, "Дякую за відгук!",
                           reply_markup=keyboard)
    
@feedback_router.message(F.chat.id == FEEDBACK_MANAGER, isReplied())
async def feedback_answer(message: Message, bot : Bot):
    message_id = message.reply_to_message.message_id
    answer = await MessageService.request_feedback_message(message_id)
    if answer:
        user_id = answer.user_id
        reply = answer.from_user_message_id
        await bot.send_message(chat_id=user_id,
                               reply_to_message_id=reply,
                               text = "ВІдповідь на ваше звернення:\n" + message.text)
        await bot.edit_message_text(chat_id=FEEDBACK_MANAGER,
                                    message_id=message_id,
                                    text=message.reply_to_message.text + " ✅")
