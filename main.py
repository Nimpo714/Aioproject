import logging
from aiogram import Bot, Dispatcher, executor
from src.credits import token
from src.register_handlers import register_handlers

BOT_TOKEN = token
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)  # -- бот
dp = Dispatcher(bot)        # -- диспетчер
register_handlers(dp)       # -- регистр хэндлеров

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

