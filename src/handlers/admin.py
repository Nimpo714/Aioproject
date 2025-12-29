# -- Modules
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

# -- Local Modules
from src.sql import add_admin, user_in_table, quest
from src.credits import admin_password
from src.servicec import spliter


class Questions(StatesGroup):
    quest1 = State()  # -- Вопрос 1 -- #
    quest2 = State()  # -- Вопрос 2 -- #
    quest3 = State()  # -- Вопрос 3 -- #
    quest4 = State()  # -- Вопрос 4 -- #
    quest5 = State()  # -- Вопрос 5 -- #

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
