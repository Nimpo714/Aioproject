# -- Modules
from aiogram.dispatcher.filters.state import State, StatesGroup


class QuizCreator(StatesGroup):
    waiting_for_question = State()
    waiting_for_options = State()
    waiting_for_correct = State()

class Game(StatesGroup):
    question = State()

class QuestionsCheck(StatesGroup):
    are_you_sure = State()
    are_you_sure_close = State()
    want_change_some_questions = State()