import logging

from sqlalchemy import select, update, func

from database.sql import async_session_maker

from database.models.user import User

class AdminService:
    
    @staticmethod
    async def is_admin(telegram_id: int) -> bool:
        async with async_session_maker() as session:
            profile_request = select(User).where(User.id == id)
            user = await session.execute(profile_request)
            return user.role == "admin"