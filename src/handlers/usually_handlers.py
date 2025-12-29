from aiogram import types
from src.sql import update_player_top_position, add_user, user_in_table


async def start(message: types.Message):
    await message.answer(f"Привет Это мини-игра с вопросами введи /help для доп информации")
    if user_in_table(message.chat.id, 'users_top'):  # if false then
        add_user(message.chat.id)

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
""")


async def null_message(message: types.Message):
    await message.answer('Комманда не была распознана введите /help для более подробной информации о командах')
