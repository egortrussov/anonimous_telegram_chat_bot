import logging 
from aiogram import Bot, Dispatcher, types 

from middleware.get_json_data import get_json_data 

BOT_TOKEN = get_json_data(['BOT_TOKEN'])['BOT_TOKEN'] 

logging.basicConfig(level=logging.INFO) 

bot = Bot(token=BOT_TOKEN) 

dp = Dispatcher(bot)

def get_dispatcher():
    return dp




