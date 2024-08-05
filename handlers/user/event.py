from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.filters import and_f, or_f
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.enums.input_media_type import InputMediaType
from aiogram import Bot

from services.message import MessageService
from services.mailing import MalingServcise
from buttons.inline import InlineButtons
from misc.callback_types import EventData

event_router = Router()

@event_router.message(F.chat.type ==  "private", or_f(Command("event"), F.text == "Івенти 🎉"))
async def event(message: Message, bot : Bot):
    id = message.from_user.id
    events = await MessageService.get_events()
    if events != []:
        current_page = len(events) - 1
        event = events[current_page]
        buttons = await InlineButtons.create_event_buttons(page=current_page,
                                                           max=current_page)
        post = await MalingServcise.formulate_event_post(text=event.text,
                                                         time=event.time,
                                                         date=event.date,
                                                         photo=event.photo)
        await bot.send_photo(chat_id = id,
                             photo=post.photo,
                             caption=post.text,
                             reply_markup=buttons.as_markup())
    else:
        await message.answer(text = "Профбюро відпочиває, івентів немає! Це ненадовго!")


@event_router.callback_query(EventData.filter((F.type == "change_page")))
async def event_navigation(query : CallbackQuery, callback_data: EventData, bot : Bot):
    id = query.from_user.id
    message_id = query.message.message_id
    current_page = callback_data.page
    events = await MessageService.get_events()
    if events != []:
        max = len(events)-1
        event = events[current_page]
        buttons = await InlineButtons.create_event_buttons(page=current_page,
                                                           max=max)
        post = await MalingServcise.formulate_event_post(text=event.text,
                                                         time=event.time,
                                                         date=event.date,
                                                         photo=event.photo)
        data = InputMediaPhoto(type=InputMediaType.PHOTO,
                               media = post.photo,
                               caption=post.text)
        await bot.edit_message_media(chat_id=id,
                                     message_id=message_id,
                                     media=data,
                                     reply_markup=buttons.as_markup())
    else:
        await query.message.answer(text = "Профбюро відпочиває, івентів немає! Це ненадовго!")