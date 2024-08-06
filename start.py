import asyncio
import logging
import sys

from bot import main
from scheduler_complete import scheduler_start
from database.sql import create_db_and_tables
from hypercorn.asyncio import serve
from hypercorn.config import Config
from flask import app


async def start() -> None:
    
    config = Config()
    config.bind = ["0.0.0.0:5000"]
    await serve(app, config)
    await scheduler_start()
    await create_db_and_tables()
    await main()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
