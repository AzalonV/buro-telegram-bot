import asyncio
import logging
import sys
from datetime import datetime

from aiogram import F
from aiogram import types, Router, F
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

from database.sql import async_session_maker
from database.models.user import User
from services.user import UserService

dp = Dispatcher()
bot = Bot(token="7212921039:AAHN6s9gHjW3dgz5n9AOafFMWTQwim40m3s", default=DefaultBotProperties(parse_mode=ParseMode.HTML))


