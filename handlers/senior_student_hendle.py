import os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot

from texts import CALENDAR_TEXT_TEMPLATE
from misc.material import TEMPLATE_CALENDAR_FILE, DAYS
from services.student_calendar import CalendarService
from misc.state import StatesCalendar

senior_student_hendler = Router()

@senior_student_hendler.message(F.chat.type ==  "private", Command("send_calendar"))
async def calendar_start(message: Message, bot : Bot, state : FSMContext):
    id = message.from_user.id
    await state.set_state(StatesCalendar.GET_FILE)
    await bot.send_document(chat_id = id, document=TEMPLATE_CALENDAR_FILE, caption=CALENDAR_TEXT_TEMPLATE)

@senior_student_hendler.message(StatesCalendar.GET_FILE, F.chat.type ==  "private", F.document)
async def calendar_load(message: Message, bot : Bot, state : FSMContext):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await state.clear()

    name = await CalendarService.generate_random_name() + ".xlsx"
    await bot.download_file(file_path=file_path, destination=name)
    
    table = await CalendarService.open_calendar_file(file_path=name)
    group = table["group"][0].upper()

    try:
        day = await CalendarService.get_one_day(group, "Понеділок")

        if day != []:
            await CalendarService.delete_group_calendar(group)

        for day in DAYS:
            for number, lesson in enumerate(table[day]):
                number = str(number+1)
                group_name = group
                await CalendarService.add_lesson(group=group_name, day=day, lesson=lesson, num=number)
        await message.answer(text="Розклад завантажено!")
    except:
        await message.answer(text="Помилка, спробуйте перечитати файл та завантажити ще раз")

    os.remove(name)
