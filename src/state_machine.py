# -- Modules
from aiogram.dispatcher.filters.state import State, StatesGroup


class Questions(StatesGroup):
    quest1 = State()  # -- Вопрос 1 -- #
    quest2 = State()  # -- Вопрос 2 -- #
    quest3 = State()  # -- Вопрос 3 -- #
    quest4 = State()  # -- Вопрос 4 -- #
    quest5 = State()  # -- Вопрос 5 -- #


class Game(StatesGroup):
    wait_for_q1 = State()
    wait_for_q2 = State()
    wait_for_q3 = State()
    wait_for_q4 = State()
