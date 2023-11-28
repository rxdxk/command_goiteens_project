from aiogram import types,Router,F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from tests import *
from .keyboards import *
from db_api.db_users import *
from loader import dp, R, db_users

R = Router()

dp.include_router(R)

class Form(StatesGroup):
    name = State()
    surname = State()
    phone = State()




class ST(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()

correct_answers = 0
lvlok = " "

def ques(current_ques):
    a = questions[str(current_ques)]
    txt = a["question"]
    return txt
def gen_keyb(num):
    but = []
    a = questions[str(num)] #1
    b = a["options"] # "0": "goed",etc
    for x in range(len(b)):
        txt = b[f"{x}"]
        but.append([types.KeyboardButton(text = f"{txt}")])
        keyb  = types.ReplyKeyboardMarkup(keyboard=but) 
    return keyb

def check_ans(current_ques,user_ans):
    global correct_answers
    a = questions[str(current_ques)] #1
    answer = a["answer"]
    print(answer)
    if user_ans == answer:
        correct_answers += 1
        return True
    else:
        return False

def lvl(correct_answers):
    if correct_answers == 1:
        lvl = "A1"
        return lvl
    elif correct_answers == 2:
        lvl  = "A2"
        return lvl
    elif correct_answers == 3:
        lvl = "B1"
        return lvl
    elif correct_answers ==4:
        lvl = "B2"
        return lvl
    elif correct_answers == 5:
        lvl = "C1"
        return lvl
    elif correct_answers == 6:
        lvl =" C2"
        return lvl


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

    if len(name) < 12  and len(name) >= 3 and name.isalpha():
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

    if len(surname) < 20  and surname.isalpha() :
        await state.update_data(surname=surname)
        await state.set_state(Form.phone)
        await message.answer(f"Тепер введи свій номер телефону ,починаючи з +38")
        
    else:
        await state.set_state(Form.surname)
        await message.answer(f"Введіть коректне прізвище")

@R.message(Form.phone)
async def phone_func(message: types.Message, state: FSMContext):
    phone = message.text
    global cur_ques
    genius_num = ["1234567890","0987654321"]
    if len(phone) == 10 and phone.isnumeric() and phone not in genius_num:
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
        await message.answer("А зараз ми пропонуємо вам пройти короткий тест на ваш рівень англійської мови")
        cur_ques = 1
        keyb = gen_keyb(cur_ques)
        await state.set_state(ST.q1)
        await message.answer("Натискайте на відповіді ,які вважайте правильними")
        txt = ques(cur_ques)
        await message.answer(txt,reply_markup=keyb)
    else:
        await state.set_state(Form.phone)
        await message.answer("Введіть коректний номер")

@R.message(ST.q1)
async def question1(message: types.Message, state: FSMContext):
    global cur_ques
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        print(cur_ques)
        keyb = gen_keyb(cur_ques)
        await message.answer("+")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q2)
    else:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("-")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q2)

@R.message(ST.q2)
async def question1(message: types.Message, state: FSMContext):
    global cur_ques
    print(cur_ques)
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        print(cur_ques)
        keyb = gen_keyb(cur_ques)
        await message.answer("+")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q3)
    else:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("-")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q3)

@R.message(ST.q3)
async def question1(message: types.Message, state: FSMContext):
    global cur_ques
    print(cur_ques)
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        #dddd
        keyb = gen_keyb(cur_ques)
        await message.answer("+")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q4)
    else:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("-")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q4)

@R.message(ST.q2)
async def question1(message: types.Message, state: FSMContext):
    global cur_ques
    print(cur_ques)
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("+")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q3)
    else:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("-")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q3)
    
@R.message(ST.q3)
async def question1(message: types.Message, state: FSMContext):
    global cur_ques
    print(cur_ques)
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("+")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q4)
    else:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("-")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q4)

@R.message(ST.q4)
async def question1(message: types.Message, state: FSMContext):
    global cur_ques
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("+")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q5)
    else:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("-")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q5)

@R.message(ST.q5)
async def question1(message: types.Message, state: FSMContext):
    global cur_ques
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("+")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q6)
    else:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("-")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q6)

@R.message(ST.q6)
async def question1(message: types.Message, state: FSMContext):
    global cur_ques
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        keyb = gen_keyb(cur_ques)
        await message.answer("+")
        lvlok = lvl(correct_answers)
        await message.answer(f"Ти набрав {correct_answers} вірних відповідей")
        await message.answer(f"Нашим дуже крутим аналізатором було вирішено ,що у тебе {lvlok}")
    else:
        keyb = gen_keyb(cur_ques)
        await message.answer("-")
        await message.answer(f"Ти набрав {correct_answers} вірних відповідей")
        await message.answer(f"Нашим дуже крутим аналізатором було вирішено ,що у тебе {lvlok}")


    
    
    
    



