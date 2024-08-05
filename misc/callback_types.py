from aiogram.filters.callback_data import CallbackData

class EventData(CallbackData, prefix="event"):
    type: str
    page: int

class CalendarData(CallbackData, prefix="calendar"):
    type: str
    group: str 
    day: str