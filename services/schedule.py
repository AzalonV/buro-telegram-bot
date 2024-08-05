from datetime import datetime, timedelta
import asyncio
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import delete


from database.sql import async_session_maker
from database.models.event import Event
from database.models.feedback_massage import FeedbackMessage

class ScheduleService:
    
    @staticmethod
    async def delet_unsuitable_event():
        async with async_session_maker() as session:
            time = datetime.now()
            delet_request = delete(Event).where(Event.date > time)
            await session.execute(delet_request)
            await session.commit()

    @staticmethod
    async def delet_unsuitable_message():
        async with async_session_maker() as session:
            three_days_ago = datetime.now() - timedelta(days=3)
            delet_request = delete(FeedbackMessage).where(FeedbackMessage.message_time <= three_days_ago)
            await session.execute(delet_request)
            await session.commit()
    

