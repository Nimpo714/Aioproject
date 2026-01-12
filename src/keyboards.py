# -- Modules
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def check_questions():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # - Хотите ли вы сверить вопросы?
    keyboard.add("Да", "Нет")
    return keyboard