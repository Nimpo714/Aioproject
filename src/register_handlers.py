# -- Modules
from aiogram import Dispatcher

# -- Local Modules
from src.handlers.usually_handlers import *  # start, help, null
from src.handlers.admin import *
from src.handlers.game_handlers import quest1


def register_handlers(dp: Dispatcher, storage):
    """ Функция, которая запускает все хэндлеры """

    # -- Стандартные хендлеры
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])

    # -- Игровые хэндлеры
    dp.register_message_handler(quest1, commands=['game'], state='*')

    # -- Админские хендлеры
    dp.register_message_handler(admin_add, commands=['admin'])
    dp.register_message_handler(start_quiz_creation, commands=['questions'], state="*")

    # - Хэндлеры для создания вопросов администратором
    dp.register_message_handler(process_question, state=QuizCreator.waiting_for_question)
    dp.register_message_handler(process_options, state=QuizCreator.waiting_for_options)
    dp.register_message_handler(process_correct_answer, state=QuizCreator.waiting_for_correct)

    # -- Ловит даже на парковке
    dp.register_message_handler(null_message)
