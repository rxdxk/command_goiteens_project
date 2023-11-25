from aiogram import types,Router,F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards import reg_kb
from loader import dp, R

R = Router()

dp.include_router(R)

class Form(StatesGroup):
    name = State()
    surname = State()
    phone = State()


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
    global name
    name = message.text
    if len(name) < 12 and name.isalpha():
        await message.answer(f"Hello {name}")
        await state.set_state(Form.surname)
        await message.answer(f"{name}, введи своє прізвище")
    else:
        await state.set_state(Form.name)
        await message.answer("Введіть коректне ім'я")
@R.message(Form.surname)

async def surname_func(message: types.Message, state: FSMContext):
    global surname
    surname = message.text
    if len(surname) < 20 and surname.isalpha():
        await state.set_state(Form.phone)
        await message.answer(f"Тепер введи свій номер телефону ,починаючи з +38")
        
    else:
        await state.set_state(Form.surname)
        await message.answer(f"Введіть коректне прізвище")
        

@R.message(Form.phone)
async def phone_func(message: types.Message, state: FSMContext, command : CommandObject):
    global phone
    phone = message.text

    if len(phone) == 10 and phone.isnumeric():
        await message.answer("Реєстрацію завершено!")
        await message.answer("Ти вже почав свій рух і скоро ти будеш говорити англіською як він:")

    else:
        await state.set_state(Form.phone)
        await message.answer("Введіть коректний номер")
