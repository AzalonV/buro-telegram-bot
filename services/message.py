from datetime import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from sqlalchemy import select, update, func

from database.sql import async_session_maker
from database.models.feedback_massage import FeedbackMessage
from database.models.event import Event


class OwnCallback(CallbackData, prefix="ok"):
    type: str
    page: int
    group: str
    day: str


class MessageService:

    @staticmethod
    async def create_feedback_message(message_id : int, user_id : int, from_user_message_id):
        async with async_session_maker() as session:
            new_feedbac_message = FeedbackMessage(message_id=message_id, user_id=user_id, from_user_message_id=from_user_message_id)
            session.add(new_feedbac_message)
            await session.commit()

    @staticmethod
    async def request_feedback_message(message_id : int):
        async with async_session_maker() as session:
            message_request = select(FeedbackMessage).where(FeedbackMessage.message_id == message_id)
            message_answer = await session.execute(message_request)
            return message_answer.scalar()
        
    @staticmethod
    async def create_event_record(text : str, time : str, date : str, photo : str):
        async with async_session_maker() as session:
            current_year = datetime.now().year
            date_string = f"{current_year}.{date} {time}:00"
            date_format = "%Y.%m.%d %H:%M:%S"
            date_object = datetime.strptime(date_string, date_format)
            print(date_object)
            new_event = Event(photo=photo,text=text, time=time,date=date, date_time=date_object)
            session.add(new_event)
            await session.commit()

    @staticmethod
    async def get_events() -> list:
        async with async_session_maker() as session:
            events_request = select(Event)
            events = await session.execute(events_request)
            return events.scalars().all()
        
    @staticmethod
    async def create_event_buttons(page : int, max : int, is_buuto_request : bool):
        event_builder = InlineKeyboardBuilder()
        if page != 0:
            callback_data = OwnCallback(type = "change_page",
                                              page = page-1).pack()
            left = InlineKeyboardButton(text="⬅️ Вліво", callback_data=callback_data)
            event_builder.add(left)
        if page != max:
            callback_data = OwnCallback(type = "change_page",
                                              page = page+1).pack()
            right = InlineKeyboardButton(text="Вправо ➡️", callback_data=callback_data)
            event_builder.add(right)
        event_builder.adjust(2)
        return event_builder

    
        
