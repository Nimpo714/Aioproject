from aiogram import types
from src.sql import
from src.credits import admin_password

async def admin_add(message: types.Message, token):
    split = ''.split(message.text)
