# -- Modules
from aiogram import types
from aiogram.dispatcher import FSMContext
# -- Local Modules
from src.sql import quest
from src.state_machine import Game


async def quest1(message: types.Message, state: FSMContext):
    Game.wait_for_q1.set()
    await message.answer(f'''
{quest(1)}
''')
