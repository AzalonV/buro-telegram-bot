from typing import Union

from aiogram import types
from aiogram.filters import Filter
from aiogram.filters import BaseFilter
from aiogram import F

from services.user import UserService
from services.admin import AdminService


class IsUser(BaseFilter): #фільтр для перевірки ролі на user

    async def __call__(self, message: types.message):
        return await UserService.is_user(message.from_user.id)
    
class IsAdmin(BaseFilter): #фільтр дял перевірки ролі на admin

    async def __call__(self, message: types.message):
        return await AdminService.is_admin(message.from_user.id)
    
class IsSuperAdmin(BaseFilter): #фільтр дял перевірки ролі на admin

    async def __call__(self, message: types.message):
        return await AdminService.is_super_admin(message.from_user.id)
    

class isReplied(BaseFilter):

    async def __call__(self, message : types.message):
        return message.reply_to_message.text is not None
    

