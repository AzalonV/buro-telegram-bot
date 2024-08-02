from aiogram import types
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

class isReplied(BaseFilter):

    async def __call__(self, message : types.message):
        try:
            msg = message.reply_to_message.text
            return True
        except AttributeError:
            return False
      
# class StateFilter(F.text): #фльтр на те чи знаходиться юзер в якомусь стані

#     async def __Call__(self, message: types.message):
#         answer = UserService.State(message.from_user.id)
#         if answer:
#             return True
#         return answer