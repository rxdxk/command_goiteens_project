from aiogram import  types

reg_but = [[types.KeyboardButton(text="Реєстрація")]]
reg_kb = types.ReplyKeyboardMarkup(keyboard=reg_but)

lang_but = [[types.KeyboardButton(text='З англійської')],
            [types.KeyboardButton(text='З української')]]
lang_kb=types.ReplyKeyboardMarkup(keyboard=lang_but)