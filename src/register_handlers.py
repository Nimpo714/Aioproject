# -- Modules
from aiogram import Dispatcher

# -- Local Modules
from src.handlers.usually_handlers import *  # start, help, null
from src.handlers.admin import *
from src.handlers.game_handlers import *


def register_handlers(dp: Dispatcher, bot: Bot):
    """ Функция, которая запускает все хэндлеры """

    # -- Стандартные хендлеры
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])

    # -- Игровые хэндлеры
    dp.register_message_handler(play_quiz, commands=['game'], state='*')
    dp.register_message_handler(play_quiz, content_types=types.ContentType.TEXT, state=Game.question)

    # -- Админские хендлеры
    dp.register_message_handler(admin_add, commands=['admin'])
    dp.register_message_handler(start_quiz_creation, commands=['questions'], state="*")

    # - Запуск игры
    dp.register_message_handler(start_game, commands=['startgame'], state="*")
    dp.register_message_handler(game_sure, state=QuestionsCheck.are_you_sure)

    # - Закрытие игры
    dp.register_message_handler(stop_game, commands=['stopgame'], state="*")
    dp.register_message_handler(stop_game_sure, state=QuestionsCheck.are_you_sure_close)
    dp.register_message_handler(close, commands=['close'])

    # - Хэндлеры для создания вопросов администратором
    dp.register_message_handler(process_question, state=QuizCreator.waiting_for_question)
    dp.register_message_handler(process_options, state=QuizCreator.waiting_for_options)
    dp.register_message_handler(process_correct_answer, state=QuizCreator.waiting_for_correct)

    # -- Ловит даже на парковке
    dp.register_message_handler(null_message)
