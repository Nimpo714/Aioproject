# -- Modules
from aiogram.dispatcher.filters.state import State, StatesGroup


class QuizCreator(StatesGroup):
    waiting_for_question = State()
    waiting_for_options = State()
    waiting_for_correct = State()

class Game(StatesGroup):
    wait_for_q1 = State()
    wait_for_q2 = State()
    wait_for_q3 = State()
    wait_for_q4 = State()
