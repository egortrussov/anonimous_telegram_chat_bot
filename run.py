from aiogram import executor, types
import os

from bot.bot import get_dispatcher
from db.db import global_init_db

from handlers.register_handlers import register_handlers

database_path = os.path.join(os.path.abspath(os.getcwd()), 'db', 'db.sqlite') 

global_init_db(database_path)

dp = get_dispatcher()

register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(get_dispatcher(), skip_updates=True)