from aiogram import types
from sqlalchemy import select, update, func

from database.sql import async_session_maker
from database.models.user import User


class UserService:
    
    @staticmethod
    async def is_exist(id: int) -> bool: #перевірка чи є такий юзер в базі данних
        async with async_session_maker() as session:
            stmt = select(User).where(User.id == id)
            is_exist = await session.execute(stmt)
            return is_exist.scalar() is not None
        
    @staticmethod
    async def create_user_profile(id : int):
        async with async_session_maker() as session:
            new_user = User(id = id)
            session.add(new_user)
            await session.commit()
    
    @staticmethod
    async def is_user(id: int) -> bool: #перевірка чи користувач є звичайним юзером
        async with async_session_maker() as session:
            profile_request = select(User).where(User.id == id)
            user = await session.execute(profile_request)
            return user.role == "user"
        

    @staticmethod
    async def get_group(id: int) -> bool: #акакдемічна група юзера
        async with async_session_maker() as session:
            request_user = select(User).where(User.id == id)
            user = await session.execute(request_user)
            result = user.scalar()
            if result is not None:
                return result.group
            return "issue"
     
    @staticmethod
    async def set_academic_group(id : int, group : str) -> bool: #встановити академічну групу
        async with async_session_maker() as session:
            new_group = update(User).where(User.id == id).values(group = group)
            await session.execute(new_group)
            await session.commit()
    

    @staticmethod
    async def formulate_profile_text(id : int):
        async with async_session_maker() as session:
            request_profile = select(User).where(User.id == id)
            user = await session.execute(request_profile)
            user = user.scalar()

            text = f"Ваш профіль:\n🤠 Академічна група: {user.group}"

            if user.is_senior_student:
                text += f"\n🏅 Староста групи {user.group}"
            if user.is_member_buro:
                text += f"\n🐱 Учасник профбюро"
            
            return text
        
