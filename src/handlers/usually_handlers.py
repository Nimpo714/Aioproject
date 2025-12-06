from aiogram import types
from src.sql import update_player_top_position

async def start(message: types.Message):
    await message.answer(f"Привет Это мини-игра с вопросами введи /help для доп информации")

async def help(message: types.Message):
    await message.answer("""
    Администратор задает 5 вопросов
    На которые всего 1 ответ из 4 вариантов
    
    1. Команда /start - начало диалога с ботом.
    2. Команда /admin <пароль> - для аутентификации администратора.
    3. Команда /questions - для создания вопросов с вариантами ответов.
    4. Команда /startgame - для запуска игры.
    5. Команда /stopgame - для остановки игры.
    6. Команда /close - для подведения итогов дня и выдачи промокодов.
    7. Ответы пользователя на вопросы квиза.""")

async def player_top(message: types.Message):
    update_player_top_position()