from environs import Env
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage


env = Env()
env.read_env() 
BOT_TOKEN = env.str("BOT_TOKEN")


bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
R = Router()
dp.include_router(R)