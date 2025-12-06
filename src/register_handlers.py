from src.handlers.usually_handlers import *  # start, help
from src.handlers.admin import *
from aiogram import Dispatcher

def register_handlers(dp: Dispatcher):
    """ Функция, которая запускает все хэндлеры """

    # -- Стандартные хендлеры
    dp.message_handler(start, commands=['start'])
    dp.message_handler(help, commands=['help'])

    # -- Админские хендлеры
    dp.message_handler()
