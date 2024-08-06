import asyncio
import logging
import sys

from bot import main
from scheduler_complete import scheduler_start
from database.sql import create_db_and_tables



async def start() -> None:

    await scheduler_start()
    №await main()
    #await create_db_and_tables()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
