import asyncio
import logging
import sys

from bot import dp, bot
from database.sql import create_db_and_tables
from database.sql import async_session_maker
from handlers.text_hendle import text_hendle
from handlers.button_hendle import button_hendle
from handlers.other_hendle import other_hendle
from handlers.state_hendle import state_hendle
from handlers.debug import debug

dp.include_router(text_hendle)
dp.include_router(button_hendle)
dp.include_router(state_hendle)
dp.include_router(other_hendle)
dp.include_router(debug)


async def main() -> None:

    await create_db_and_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())