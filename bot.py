from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# from handlers.user.start import start_router
# from handlers.user.event import event_router
# from handlers.user.profile import profile_router
# from handlers.user.calendar import calendar_router
# from handlers.feedback import feedback_router
# from handlers.user.union import union_router
# from handlers.rollback import roolback_router
# from handlers.buro import buro_hendler
# from handlers.senior_student_hendle import senior_student_hendler
# from handlers.debug import debug
# from handlers.admin import admin_router
# from handlers.chat import chat_router

WEBHOOK_PATH = f"/bot/7212921039:AAHN6s9gHjW3dgz5n9AOafFMWTQwim40m3s"

async def on_startup(bot: Bot) -> None:
    await set_commands(bot)
    # Set webhook
    await bot.set_webhook(
        f"10.88.0.5{WEBHOOK_PATH}",
        secret_token="dwrrfacw4octhw73a0",
        allowed_updates=[
            "message",
            "chat_member",
            "callback_query",
            "channel_post",
        ],  # allow updates needed
    )



async def main():

    # routers_list = [start_router,
    #                 union_router,
    #                 roolback_router,
    #                 feedback_router,
    #                 buro_hendler,
    #                 event_router,
    #                 profile_router,
    #                 calendar_router,
    #                 senior_student_hendler,
    #                 debug,
    #                 admin_router,
    #                 chat_router] 
    
    app = web.Application()

    web.run_app(app, host="0.0.0.0", port=8080)

    # bot = Bot(token="7212921039:AAHN6s9gHjW3dgz5n9AOafFMWTQwim40m3s", default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # dp = Dispatcher()

    # dp.include_routers(*routers_list)
    # dp.startup.register(on_startup)

    
    # webhook_requests_handler = SimpleRequestHandler(
    #     dispatcher=dp, bot=bot, secret_token="dwrrfacw4octhw73a0"
    # )
    
    # webhook_requests_handler.register(app, path=WEBHOOK_PATH)
