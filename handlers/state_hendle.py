import re

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types, Router, F
from aiogram.filters.command import Command
from aiogram.filters import and_f, or_f
from aiogram.types.input_file import URLInputFile

from bot import bot
from texts import EVENT_TEXT_TEMAPLTES
from config import FEEDBACK_MANAGER, TEMPLATE_FILE
from database.sql import async_session_maker
from services.message import MessageService, OwnCallback
from services.mailing import MalingServcise
from services.user import UserService



state_hendle = Router()

def STATE_FILTER(message, state):
    return state_hold.get(message.from_user.id, DEFAULT)["state"] == state

state_hold = {}
DEFAULT = {"state" : "standart", "text" : None}
DAYS = ["Понеділок", "Вівторок", "Середа", "Четверг", "П'ятниця", "Субота"]


@state_hendle.message(F.chat.type ==  "private", Command("create_event"), lambda message: STATE_FILTER(message, "standart"))
async def event_start(message: types.message):
    id = message.from_user.id   
    new_user_state = {id : {"state" : "event_1", "text" : None}}
    state_hold.update(new_user_state)
    await message.answer(text=EVENT_TEXT_TEMAPLTES)

@state_hendle.message(F.chat.type ==  "private", F.text, lambda message: STATE_FILTER(message, "event_1"))
async def event_route(message: types.message):
    id = message.from_user.id
    text = message.html_text
    new_user_state = {id : {"state" : "event_2", "text" : text}}
    state_hold.update(new_user_state)
    await message.answer(text="Чудово! тепер відправ картинку!")

@state_hendle.message(F.chat.type ==  "private", F.photo, lambda message: STATE_FILTER(message, "event_2"))
async def event_route_2(message: types.message):
    photo = message.photo[0].file_id
    id = message.from_user.id
    text = state_hold.get(id)["text"]
    post_text = (re.search("\"(.+)\"",text, re.DOTALL)[0])[1:-1]
    time = (re.search("Час: \d+:\d+", text)[0])[5:]
    date = (re.search("Дата: \d+.\d+", text)[0])[6:]
    post = await MalingServcise.formulate_event_post(text=post_text, time=time, date=date, photo=photo)
    await MessageService.create_event_record(text=post_text, time=time, date=date, photo=photo)
    await MalingServcise.send_event_post(bot, post)
    new_user_state = {id : DEFAULT}
    state_hold.update(new_user_state)
    await bot.send_message(chat_id = id, text = "Пост відправлений!")

@state_hendle.message(F.chat.type ==  "private",or_f(Command("feedback"), F.text == "feedback ✉️"),  lambda message: STATE_FILTER(message, "standart"))
async def feedback(message: types.message):
    id = message.from_user.id
    new_user_state = {id : {"state" : "feedback", "text" : None}}
    state_hold.update(new_user_state)
    await message.answer("Чудово напишіть нам свій відгук/пропозицію/побажання\n\nЗамітка: зворотній зв'язок анонімний!")

@state_hendle.callback_query(OwnCallback.filter(F.type == "feedback"))
async def feedback(callback : types.callback_query):
    id = callback.from_user.id
    new_user_state = {id : {"state" : "feedback", "text" : None}}
    state_hold.update(new_user_state)
    await bot.send_message(id, "Чудово напишіть нам свій відгук/пропозицію/побажання\n\nЗамітка: зворотній зв'язок анонімний!")

@state_hendle.message(F.chat.type ==  "private", lambda message: STATE_FILTER(message, "feedback"))
async def feedback_route(message: types.message):
    id = message.from_user.id
    f_message = await bot.send_message(FEEDBACK_MANAGER, message.text)
    await MessageService.create_feedback_message(message_id=f_message.message_id, user_id=id, from_user_message_id=message.message_id)
    new_user_state = {id : {"state" : "standart", "text" : None}}
    state_hold.update(new_user_state)
    await bot.send_message(id, "Дякую за відгук!")

@state_hendle.message(F.chat.type ==  "private", or_f(Command("calendar"), F.text == "Розклад 🗓️"))
async def calendar(message: types.message):
    id = message.from_user.id
    group = await UserService.get_group(id)
    if group == 'None':
        new_user_state = {id : {"state" : "academic", "text" : None}}
        state_hold.update(new_user_state)
        await message.answer("Вам слід вибрати групу\nПриклад групи: МТА-11С\nВведіть академічну групу:")
    else:
        rozklad = await UserService.get_one_day(group, "Понеділок")
        print(rozklad)
        if rozklad is not []:
            text = await UserService.formulate_calendar(rozklad)
            buttons = await create_calendar_buttons(group)
            await message.answer(text = text, reply_markup=buttons.as_markup())
        else:
            await message.answer(text="Для вашої групи ще нема розкладу")

async def create_calendar_buttons(group):
    calendar_builder = InlineKeyboardBuilder()
    for day in DAYS:
        callback_data = OwnCallback(type = "calendar", group=group, day=day, page=0).pack()
        button = types.InlineKeyboardButton(text=day, callback_data=callback_data)
        calendar_builder.add(button)
    calendar_builder.adjust(3)
    return calendar_builder

@state_hendle.message(F.chat.type ==  "private", F.text, lambda message: STATE_FILTER(message, "academic"))
async def academic_group(message: types.message):
    id = message.from_user.id
    text = message.text
    new_user_state = {id : {"state" : "standart", "text" : None}}
    state_hold.update(new_user_state)
    await UserService.set_academic_group(id, text)
    await message.answer("Вибрана академічна група!")

@state_hendle.message(Command("send_calendar"), F.chat.type == "private")
async def send_calendar(message: types.message):
    id = message.from_user.id
    new_user_state = {id : {"state" : "create_calendar", "text" : None}}
    state_hold.update(new_user_state)
    file = URLInputFile(url="https://docs.google.com/spreadsheets/d/e/2PACX-1vSHiME2ms7tuSvUgR_G_ZadoR0_axWkOF6Resj3Vk1Xire0aBrOE7dIpbsBcx8tYg/pub?output=xlsx", filename="template.xlsx")
    await bot.send_document(chat_id = id, document=file, caption="""Щоб завантжити розклад вам потрібно:
1) Вже мати встановлену академічну групу
2) Надіслати заповнений ексель файл
*Якщо потрібно описати знаменник та чисельник виеористайте бек слеш '\\'
*Якщо чисельник або знаменник пустий заповніть як 'пусто'
Приклад: пусто\математичний аналіз❤️
*Кожного разу намагайтесь міняти ім'я заповненого зразку
Надішліть заповнений зразок:""")
    
@state_hendle.message(F.chat.type == "private", F.document, lambda message: STATE_FILTER(message, "create_calendar"))
async def input_calendar(message: types.message):
    print(message)
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    new_user_state = {id : DEFAULT}
    state_hold.update(new_user_state)
    name = await UserService.generate_random_name() + ".xlsx"
    await bot.download_file(file_path=file_path, destination=name)
    table = await UserService.open_calendar_file(file_path=name)
    print(table)
    for day in DAYS:
        for number, lesson in enumerate(table[day]):
            number = str(number+1)
            group_name = str(table["group"][0]).upper()
            await UserService.add_lesson(group=group_name, day=day, lesson=lesson, num=number)
    await message.answer(text="Розклад завантажено!")

