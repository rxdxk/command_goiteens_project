import logging

from aiogram import types
from aiogram.filters import Command, CommandStart, CommandObject

from loader import dp


@dp.message(Command("start"))
async def get_user_by_id(msg: types.Message, command: CommandObject):
    await msg.reply(f"Вітаю! Для реєстрації настисніть кнопку Зареєструватися, для додаткової інформації напишіть комманду /info.")
