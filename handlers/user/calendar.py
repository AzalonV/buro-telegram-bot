from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters import and_f, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


from services.user import UserService
from services.student_calendar import CalendarService
from buttons.inline import InlineButtons
from misc.state import StatesProfile
from misc.callback_types import CalendarData


calendar_router = Router()

@calendar_router.message(F.chat.type ==  "private", or_f(Command("calendar"), F.text == "Розклад 🗓️"))
async def calendar(message: Message, state : FSMContext):
    id = message.from_user.id
    group = await UserService.get_group(id)

    print(group)
    if group == None:
        state.set_state(StatesProfile.GET_ACADEMIC_GROUP)
        await message.answer("Вам слід вибрати групу\nПриклад групи: МТА-11C\nВведіть академічну групу:")

    else:
        rozklad = await CalendarService.get_one_day(group, "Понеділок")

        if rozklad != []:
            text = await CalendarService.formulate_calendar(rozklad)
            buttons = await InlineButtons.create_calendar_buttons(group)
            await message.answer(text = text, reply_markup=buttons.as_markup())

        else:
            await message.answer(text="Для вашої групи ще нема розкладу")

@calendar_router.callback_query(CalendarData.filter(F.type == "calendar"))
async def calendar(query : CallbackQuery, callback_data : CalendarData):
    id = query.from_user.id
    message_id = query.message.message_id
    group = callback_data.group
    day = callback_data.day
    day = await CalendarService.get_one_day(group=group, day=day)
    text = await CalendarService.formulate_calendar(day)
    buttons = await InlineButtons.create_calendar_buttons(group)
    await query.message.edit_text(text=text, reply_markup=buttons.as_markup())
