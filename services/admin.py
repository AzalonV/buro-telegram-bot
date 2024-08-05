from aiogram import types
from sqlalchemy import select, update, func

from database.sql import async_session_maker
from database.models.user import User


class AdminService:

    @staticmethod
    async def is_admin(id):
        async with async_session_maker() as session:
            admin_request = select(User).where(User.id == id)
            result = await session.execute(admin_request)
            return result.scalar.user_role == "admin"
        
    @staticmethod
    async def is_super_admin(id):
        async with async_session_maker() as session:
            super_admin_request = select(User).where(User.id == id)
            result = await session.execute(super_admin_request)
            return result.scalar().user_role == "super_admin"

    @staticmethod
    async def set_super_admin(id):
        async with async_session_maker() as session:
            new_user_role = update(User).where(User.id == id).values(user_role = "super_admin")
            await session.execute(new_user_role)
            await session.commit()
    
    @staticmethod
    async def set_admin(id):
        async with async_session_maker() as session:
            new_user_role = update(User).where(User.id == id).values(user_role = "admin")
            await session.execute(new_user_role)
            await session.commit()

    @staticmethod
    async def delete_admin(id):
        async with async_session_maker() as session:
            new_user_role = update(User).where(User.id == id).values(user_role = "user")
            await session.execute(new_user_role)
            await session.commit()

    @staticmethod
    async def set_senoir_student(id):
        async with async_session_maker() as session:
            new_user_role = update(User).where(User.id == id).values(is_senior_student = True)
            await session.execute(new_user_role)
            await session.commit()

    @staticmethod
    async def delete_senoir_student(id):
        async with async_session_maker() as session:
            new_user_role = update(User).where(User.id == id).values(is_senior_student = False)
            await session.execute(new_user_role)
            await session.commit()

    @staticmethod
    async def set_buro(id):
        async with async_session_maker() as session:
            new_user_role = update(User).where(User.id == id).values(is_member_buro = True)
            await session.execute(new_user_role)
            await session.commit()

    @staticmethod
    async def delete_buro(id):
        async with async_session_maker() as session:
            new_user_role = update(User).where(User.id == id).values(is_member_buro = False)
            await session.execute(new_user_role)
            await session.commit()