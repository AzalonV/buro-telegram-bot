from random import randint, choice
from datetime import datetime, date

from sqlalchemy import select, update, func, delete
import pandas

from database.sql import async_session_maker
from database.models.calendar import Calendar
from misc.material import EMOJI

class CalendarService:
    
    @staticmethod
    async def get_one_day(group : str, day : str):
        async with async_session_maker() as session:
            request_calendar = select(Calendar).where(Calendar.group == group, Calendar.day == day)
            calendar = await session.execute(request_calendar)
            return calendar.scalars().all()
        
    @staticmethod
    async def get_one_day(group : str, day : str):
        async with async_session_maker() as session:
            request_calendar = select(Calendar).where(Calendar.group == group, Calendar.day == day)
            calendar = await session.execute(request_calendar)
            return calendar.scalars().all()
        
    @staticmethod
    async def add_lesson(group : str, day : str, lesson : str, num : str):
        async with async_session_maker() as session:
            new_lesson = Calendar(group=group, day=day, num=num, lesson=lesson)
            session.add(new_lesson)
            await session.commit()

    @staticmethod
    async def generate_random_name():
        random_number = randint(1000, 100000)
        return str(random_number)
    
    @staticmethod
    async def open_calendar_file(file_path : str):
        return pandas.read_excel(file_path)
    
    @staticmethod
    async def formulate_calendar(data : list):
        today = date.today()
        week_number = today.isocalendar()[1] % 2
        week_type = ["Чисельник", "Знаменник"]
        random_emoji = choice(EMOJI)
        day = data[0].day
        text = "День: "
        text += f"{day} {random_emoji}\nЦього тижня: {week_type[week_number]}\n"

        for one_chunck in data:
            num = one_chunck.num
            lesson = one_chunck.lesson
            text += num + ". "

            if lesson is None:
                text += "\n"

            elif "\\" in lesson:
                choose = lesson.split("\\")[0]
                if choose == "пусто":
                    text += "\n"
                else:
                    text += choose + "\n"

            else:
                text +=  lesson + "\n"

        return text
    
    @staticmethod
    async def delete_group_calendar(group : str):
        async with async_session_maker() as session:
            delet_request = delete(Calendar).where(Calendar.group == group)
            await session.execute(delet_request)
            await session.commit()
