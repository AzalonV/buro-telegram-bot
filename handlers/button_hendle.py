from aiogram import types, Router, F
from aiogram import Dispatcher

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.enums.input_media_type import InputMediaType
from aiogram import types

from services.user import UserService
from services.mailing import MalingServcise
from services.message import MessageService
from services.message import OwnCallback
from bot import bot

button_hendle = Router()
DAYS = ["Понеділок", "Вівторок", "Середа", "Четверг", "П'ятниця", "Субота"]

@button_hendle.callback_query(OwnCallback.filter((F.type == "change_page")))
async def event_navigation(query : types.callback_query, callback_data: OwnCallback):
    id = query.from_user.id
    message_id = query.message.message_id
    data = query.data
    current_page = callback_data.page
    events = await MessageService.get_events()
    max = len(events)-1
    buttons = await MessageService.create_event_buttons(page=current_page, max=max, is_buuto_request=False)
    event = events[current_page]
    post = await MalingServcise.formulate_event_post(text=event.text, time=event.time, date=event.date, photo=event.photo)
    data = InputMediaPhoto(type=InputMediaType.PHOTO, media = post.photo, caption=post.text)
    await bot.edit_message_media(media=data, chat_id=id, message_id=message_id, reply_markup=buttons.as_markup())

@button_hendle.callback_query(OwnCallback.filter(F.type == "event_page"))
async def event_navigation(query : types.callback_query):
    id = query.from_user.id
    events = await MessageService.get_events()
    current_page = len(events) - 1
    buttons = await MessageService.create_event_buttons(page=current_page, max=current_page, is_buuto_request=False)
    event = events[current_page]
    post = await MalingServcise.formulate_event_post(text=event.text, time=event.time, date=event.date, photo=event.photo)
    await bot.send_photo(chat_id = id,  photo=post.photo, caption=post.text, reply_markup=buttons.as_markup())

@button_hendle.callback_query(OwnCallback.filter(F.type == "calendar"))
async def calendar(query : types.callback_query, callback_data : OwnCallback):
    id = query.from_user.id
    message_id = query.message.message_id
    group = callback_data.group
    day = callback_data.day
    day = await UserService.get_one_day(group=group, day=day)
    text = await UserService.formulate_calendar(day)
    buttons = await create_calendar_buttons(group)
    await bot.edit_message_text(message_id=message_id, chat_id = id, text=text,reply_markup=buttons.as_markup())


async def create_calendar_buttons(group):
    calendar_builder = InlineKeyboardBuilder()
    for day in DAYS:
        callback_data = OwnCallback(type = "calendar", group=group, day=day, page=0).pack()
        button = types.InlineKeyboardButton(text=day, callback_data=callback_data)
        calendar_builder.add(button)
    calendar_builder.adjust(3)
    return calendar_builder