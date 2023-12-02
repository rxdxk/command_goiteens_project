from environs import Env
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from db_api.db_users import  DbUsers
from db_api.db import BotDb

env = Env()
env.read_env() 
BOT_TOKEN = env.str("BOT_TOKEN")
DB_FILE = env.str("DB_FILE")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

R = Router()
dp.include_router(R)

bot_db = BotDb(DB_FILE)
db_users = DbUsers()

my_dict = {}
