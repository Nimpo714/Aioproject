# -- Modules
import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# -- Local Modules
from src.credits import token
from src.register_handlers import register_handlers

# Настройки Логирования и Токен бота
BOT_TOKEN = token
logging.basicConfig(level=logging.INFO)

# Настройки и подключение к Telegram API
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)  # -- бот
dp = Dispatcher(bot, storage=storage)        # -- диспетчер

# -- регистр хэндлеров
dp.data['bot'] = bot  # для bot.send
register_handlers(dp, storage)      

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

