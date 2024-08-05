import re

from aiogram import Router, F
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated

from services.chat import ChatService

chat_router = Router()

          
@chat_router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def join_check(event: ChatMemberUpdated):
     await ChatService.add_chat_in_base(chat_id=event.chat.id)