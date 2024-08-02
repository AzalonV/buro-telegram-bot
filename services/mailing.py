from aiogram import types
from aiogram.types import MessageEntity, InputMediaPhoto
from aiogram.enums.input_media_type import InputMediaType
from aiogram.enums import ParseMode
from sqlalchemy import select, update, func

from database.sql import async_session_maker
from database.models.chat_seeting import ChatSetting

class EventPost:

    def __init__(self, text, photo):
        self.text = text
        self.photo = photo

class MalingServcise:

    @staticmethod
    async def formulate_event_post(text : str, time : str, date : str, photo : str) -> str: #сформулювати івентовий пост
        return EventPost(text=f"{text}\n\nЧас: {time}\nДата: {date}", photo = photo)
    
    @staticmethod 
    async def send_event_post(bot, post): #розіслати івентовий пост
        async with async_session_maker() as session:
            chats_request = select(ChatSetting).where(ChatSetting.is_mailing == True)
            chats = await session.execute(chats_request)
            for chat in chats.scalars():
                try:
                    await bot.send_photo(chat_id = chat.chat_id, photo=post.photo, caption=post.text, parse_mode=ParseMode.HTML)
                except:
                    pass
