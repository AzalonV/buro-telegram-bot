from datetime import datetime
import asyncio
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler

def tick():
    print('Tick! The time is: %s' % datetime.now())


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)
    scheduler.start()
    


if __name__ == '__main__':
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass