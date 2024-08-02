import logging
from random import randint

from aiogram import types
from sqlalchemy import select, update, func
import pandas

from database.sql import async_session_maker
from database.models.user import User
from database.models.calendar import Calendar


class UserService:
    
    @staticmethod
    async def is_exist(id: int) -> bool: #перевірка чи є такий юзер в базі данних
        async with async_session_maker() as session:
            stmt = select(User).where(User.id == id)
            is_exist = await session.execute(stmt)
            return is_exist.scalar() is not None
    
    @staticmethod
    async def is_user(id: int) -> bool: #перевірка чи користувач є звичайним юзером
        async with async_session_maker() as session:
            profile_request = select(User).where(User.id == id)
            user = await session.execute(profile_request)
            return user.role == "user"
        
    @staticmethod
    async def state_check(id: int) -> str: #перевірка стану користувача
        async with async_session_maker() as session:
            profile_request = select(User).where(User.id == id)
            user = await session.execute(profile_request)
            user =result = user.scalars().first()
            return user.state
        
    @staticmethod
    async def change_state(id : int, state : str) -> None: #зміна стану
        async with async_session_maker() as session:
            new_state = update(User).where(User.id == id).values(state = state)
            await session.execute(new_state)
            await session.commit()

    @staticmethod
    async def get_group(id: int) -> bool: #акакдемічна група юзера
        async with async_session_maker() as session:
            request_user = select(User).where(User.id == id)
            user = await session.execute(request_user)
            return user.scalar().group
        
    @staticmethod
    async def set_academic_group(id : int, group : str) -> bool: #встановити академічну групу
        async with async_session_maker() as session:
            new_group = update(User).where(User.id == id).values(group = group)
            await session.execute(new_group)
            await session.commit()
    
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
        text = "День: "
        text += data[0].day + "\n"
        for one_chunck in data:
            num = str(one_chunck.num)
            lesson = one_chunck.lesson
            if lesson is None:
                text += num + "\n"
            elif "\\" in lesson:
                choose = lesson.split("\\")[0]
                if choose == "пусто":
                    text += num + ".\n"
                else:
                    text += num + ". " + choose + "\n"
            else:
                text += num + ". " + lesson + "\n"

        return text
