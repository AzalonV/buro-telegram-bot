from sqlalchemy import select, update, func

from database.sql import async_session_maker
from database.models.chat_seeting import ChatSetting

class ChatService:

    @staticmethod
    async def add_chat_in_base(chat_id : int) -> None: #додавання чата в базу даних
        async with async_session_maker() as session:
            new_chat = ChatSetting(chat_id=chat_id)
            session.add(new_chat)
            await session.commit()

