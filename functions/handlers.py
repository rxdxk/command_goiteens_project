from aiogram import types,Router,F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from .keyboards import *
from db_api.db_users import *
from loader import dp, R, db_users 

R = Router()

dp.include_router(R)

class Form(StatesGroup):
    name = State()
    surname = State()
    phone = State()

@R.message(Command("info"))
async def start_func(message: types.Message, state: FSMContext):
    await message.answer('''<b>Що може цей бот?</b>
    <i>-Визначити твій рівень англійської
    -Допомогти прокачати свої знання
    -Давати рекомендації щодо вивчення нових слів та правил
    -Давати завдання
    -Допомогти тобі провести час із користю</i>
                            ''')

@dp.message(F.text == "Реєстрація")
async def reg_func(message: types.Message):
    await message.answer("Як тебе звати ?",reply_markup=types.ReplyKeyboardRemove())

@R.message(Command("start"))
async def start_func(message: types.Message, state: FSMContext):
    await message.answer("Вітаємо тебе у боті для вивчення англіської🇬🇧")
    await message.answer("Щоб почати тобі треба зареєструватись(натисни кнопку)🏁",reply_markup=reg_kb)
    await state.set_state(Form.name)

@R.message(Form.name)
async def name_func(message: types.Message, state: FSMContext):
    
    name = message.text

    if len(name) < 12 and name.isalpha():
        await message.answer(f"Hello {name}")
        await state.update_data(name=name)
        await state.set_state(Form.surname)
        await message.answer(f"{name}, введи своє прізвище")

    else:
        await state.set_state(Form.name)
        await message.answer("Введіть коректне ім'я")

@R.message(Form.surname)

async def surname_func(message: types.Message, state: FSMContext):
    surname = message.text

    if len(surname) < 20 and surname.isalpha():
        await state.update_data(surname=surname)
        await state.set_state(Form.phone)
        await message.answer(f"Тепер введи свій номер телефону ,починаючи з +38")
        
    else:
        await state.set_state(Form.surname)
        await message.answer(f"Введіть коректне прізвище")

@R.message(Form.phone)
async def phone_func(message: types.Message, state: FSMContext):
    phone = message.text

    if len(phone) == 10 and phone.isnumeric():
        await state.update_data(phone=phone)
        data  = await state.get_data()
        
        db_users.register_user(
            username=message.from_user.username,
            name=data.get("name"),
            surname=data.get("surname"),
            lvl=None,
            phone_number=data.get("phone"),
            telegram_user_id=message.from_user.id
        )

        await message.answer("Реєстрацію завершено!")
        await message.answer("Ти вже почав свій рух і скоро ти будеш говорити англіською як він:")
        await message.answer("А зараз ми проунуємо вам пройти короткий тест на ваш рівень англійської мови")

    else:
        await state.set_state(Form.phone)
        await message.answer("Введіть коректний номер")


