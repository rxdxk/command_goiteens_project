from aiogram import  types

lang_but = [[types.KeyboardButton(text='З англійської')],
            [types.KeyboardButton(text='З української')]]
lang_kb=types.ReplyKeyboardMarkup(keyboard=lang_but)
