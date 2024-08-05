from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot

from texts import EVENT_TEXT_TEMAPLTES 
from misc.state import StatesEvent
from misc.validator import Validators
from services.message import MessageService
from services.mailing import MalingServcise
from buttons.keyboard import KeyboardButtons

buro_hendler = Router()

@buro_hendler.message(F.chat.type ==  "private", Command("create_event"))
async def create_event(message: Message, state : FSMContext):
    await state.set_state(StatesEvent.GET_TEXT)
    cancel_button = await KeyboardButtons.create_cancel_button()
    await message.answer(text="Введіть текст посту:", reply_markup=cancel_button)

@buro_hendler.message(StatesEvent.GET_TEXT, F.chat.type ==  "private", F.text)
async def event_route_1(message: Message, state : FSMContext):
    text = message.text
    validation = await Validators.event_text(text)
    if validation:
        await state.update_data(text = message.html_text)
        await state.set_state(StatesEvent.GET_TIME)
        await message.answer(text="Чудово! тепер відправ час проведення івенту в форматі hh:mm!")
    else:
        await message.answer(text="Зменшіть кількість символів до 1000")

@buro_hendler.message(StatesEvent.GET_TIME, F.chat.type ==  "private", F.text)
async def event_route_2(message: Message, state : FSMContext):
    text = message.text
    validation = await Validators.event_time(text)
    if validation:
        await state.update_data(time = text)
        await state.set_state(StatesEvent.GET_DATE)
        await message.answer(text="Чудово! тепер відправ дату проведення івенту в форматі mm.dd!")
    else:
        await message.answer(text="Час повинен бути у відповідному форматі!!!\nДо прикладу: 01:30")


@buro_hendler.message(StatesEvent.GET_DATE, F.chat.type ==  "private", F.text)
async def event_route_2(message: Message, state : FSMContext):
    text = message.text
    validation = await Validators.event_date(text)
    if validation:
        await state.update_data(date = text)
        await state.set_state(StatesEvent.GET_PHOTO)
        await message.answer(text="Чудово! тепер відправ картинку івенту!")
    else:
        await message.answer(text="Дата повинна бути у відповідному форматі!!!\nДо прикладу: 01.09, 01:21, 12.22")

@buro_hendler.message(StatesEvent.GET_PHOTO, F.chat.type ==  "private", F.photo)
async def event_route_3(message: Message, bot : Bot, state : FSMContext):
    photo = message.photo[0].file_id
    keyboard = await KeyboardButtons.create_start_buttons()
    data = await state.get_data()
    post = await MalingServcise.formulate_event_post(text=data["text"], time=data["time"], date=data["date"], photo=photo)
    await MessageService.create_event_record(text=data["text"], time=data["time"], date=data["date"], photo=photo)
    await MalingServcise.send_event_post(bot, post)
    await state.clear()
    await message.answer(text = "Пост відправлений!", reply_markup=keyboard)