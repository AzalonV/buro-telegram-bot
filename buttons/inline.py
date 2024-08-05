from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from misc.callback_types import EventData, CalendarData
from misc.material import DAYS
class InlineButtons:
    
    @staticmethod
    async def create_event_buttons(page : int, max : int):
        event_builder = InlineKeyboardBuilder()
        if page != 0:
            callback_data = EventData(type = "change_page", page = page-1).pack()
            left = InlineKeyboardButton(text="⬅️ Вліво", callback_data=callback_data)
            event_builder.add(left)
        if page != max:
            callback_data = EventData(type = "change_page", page = page+1).pack()
            right = InlineKeyboardButton(text="Вправо ➡️", callback_data=callback_data)
            event_builder.add(right)
        event_builder.adjust(2)
        return event_builder
    
    @staticmethod
    async def create_calendar_buttons(group):
        calendar_builder = InlineKeyboardBuilder()
        for day in DAYS:
            callback_data = CalendarData(type = "calendar", group=group, day=day).pack()
            button = InlineKeyboardButton(text=day, callback_data=callback_data)
            calendar_builder.add(button)
            calendar_builder.adjust(3)
        return calendar_builder
