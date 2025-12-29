from src.handlers.usually_handlers import *  # start, help, null
from src.handlers.admin import *
from src.handlers.game_handlers import quest1
from aiogram import Dispatcher


def register_handlers(dp: Dispatcher):
    """ Функция, которая запускает все хэндлеры """

    # -- Стандартные хендлеры
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])

    # -- Игровые хэндлеры
    dp.register_message_handler(quest1, commands=['game'], state='*')

    # -- Админские хендлеры
    dp.register_message_handler(admin_add, commands=['admin'])

    # -- Ловит даже на парковке
    dp.register_message_handler(null_message)
