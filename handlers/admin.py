import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.filters import and_f, or_f

from filters import IsSuperAdmin, IsAdmin
from services.user import UserService
from services.admin import AdminService
from services.message import MessageService
from services.chat import ChatService
from services.mailing import MalingServcise

async def change_user_status(func, message):

    ids = await MessageService.util_for_admin(message)
    for id in ids:
        id = int(id)
        validation = await UserService.is_exist(id)
        
        if not validation:
            await UserService.create_user_profile(id=id)
            await ChatService.add_chat_in_base(id=id)
                
        await func(id=id)

admin_router = Router()

@admin_router.message(Command("set_admin"), IsSuperAdmin())
async def create_admin(message : Message):
    await change_user_status(func=AdminService.set_admin, message=message)
    await message.answer("Додано нового адміна!")

@admin_router.message(Command("set_super_admin"), IsSuperAdmin())
async def create_super_admin(message : Message):
    await change_user_status(func=AdminService.set_super_admin, message=message)
    await message.answer("Додано нового супер адміна!")

@admin_router.message(Command("set_senior_student"), or_f(IsAdmin(), IsSuperAdmin()))
async def create_senior_student(message : Message):
    await change_user_status(func=AdminService.set_senoir_student, message=message)
    await message.answer("Додано нового старосту!")

@admin_router.message(Command("set_buro"), or_f(IsAdmin(), IsSuperAdmin()))
async def create_buro(message : Message):
    await change_user_status(func=AdminService.set_buro, message=message)
    await message.answer("Додано нового уачсника профбюро!")

@admin_router.message(Command("stop_notification"), or_f(IsAdmin(), IsSuperAdmin()))
async def stop_mailing(message : Message):
    id = message.chat.id
    await MalingServcise.stop(id)
    await message.answer("Сповіщення відключені!")

