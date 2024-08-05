from typing import Dict, Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from database.models.user import User
from database.sql import async_session_maker
from services.user import UserService
from services.chat import ChatService

class Starter(BaseMiddleware):

    async def __call__(self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        id = event.from_user.id
        if await UserService.is_exist(id) is False:
            await UserService.create_user_profile(id)
            await ChatService.add_chat_in_base(chat_id=id)
        return await handler(event, data)