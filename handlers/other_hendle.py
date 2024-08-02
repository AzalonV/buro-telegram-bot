import re

from aiogram import types, Router, F
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated

from config import FEEDBACK_MANAGER
from bot import bot
from database.sql import async_session_maker
from services.user import UserService
from services.message import MessageService
from services.chat import ChatService
from services.mailing import MalingServcise
from filters import isReplied


other_hendle = Router()

          
@other_hendle.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def join_check(event: ChatMemberUpdated):
     await ChatService.add_chat_in_base(chat_id=event.chat.id)
     