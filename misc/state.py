from aiogram.fsm.state import StatesGroup, State

class StatesEvent(StatesGroup):
    GET_TEXT = State()
    GET_TIME = State()
    GET_DATE = State()
    GET_PHOTO = State()

class StatesCalendar(StatesGroup):
    GET_FILE = State()

class StatesProfile(StatesGroup):
    GET_ACADEMIC_GROUP = State()

class StatesFeedback(StatesGroup):
    GET_FEEDBACK_MESSAGE = State()
