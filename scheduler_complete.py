import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.schedule import ScheduleService

async def scheduler_start():
    scheduler = AsyncIOScheduler(timezone='Europe/Kiev')
    scheduler.add_job(ScheduleService.delet_unsuitable_event, 'cron', hour=1)
    scheduler.add_job(ScheduleService.delet_unsuitable_message, 'cron', hour=1)
    scheduler.add_job(ScheduleService., 'interval', seconds=3)
    scheduler.start()
