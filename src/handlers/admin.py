# -- Modules
from aiogram import types

# -- Local Modules
from src.sql import add_admin, user_in_table, quest
from src.credits import admin_password
from src.servicec import spliter
from src.state_machine import Questions


async def admin_add(message: types.Message):
    split = spliter(message.text)
    # !!! Реализовать user_in_table
    if split[1] == admin_password:
        try:
            add_admin(message.chat.id)
            await message.answer("Админ был добавлен")

        except IndexError:
            await message.answer('ты че >:(')


async def quest_set(message: types.Message):
    split = spliter(message.text)
