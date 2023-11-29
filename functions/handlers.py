from aiogram import types,Router,F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from .translator import translate_eng as eng
from .translator import translate_ukr as ukr
from .tests import *
from .keyboards import *
from db_api.db_users import *
from loader import dp, R, db_users

R = Router()

dp.include_router(R)

class Form(StatesGroup):
    name = State()
    surname = State()
    phone = State()

class transl(StatesGroup):
    choose = State()
    eng = State()
    ukr = State()
    eng_answer = State()
    ukr_answer = State()


class ST(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()

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
    
def format_user_info_string(user_info: tuple):
        return f"""
    <b>
    Username: {user_info[1]}
First Name: {user_info[2]}
Last Name: {user_info[3]}
Telegram ID: {user_info[4]}
Phone Number: +380{user_info[5]}
English Level: {user_info[6]}

    </b>
    """

@R.message(Command("info"))
async def info_func(message: types.Message):
    await message.answer('''<b>Що може цей бот?</b>
    <i>-Визначити твій рівень англійської
    -Допомогти прокачати свої знання
    -Давати рекомендації щодо вивчення нових слів та правил
    -Давати завдання
    -Допомогти тобі провести час із користю</i>
                        ''')

@R.message(Command("test"))
async def reg_func(message: types.Message, state: FSMContext):
    global cur_ques
    await message.answer("Натискай на відповіді які вважаєш правильними")
    await state.set_state(ST.q1)
    cur_ques = 1
    keyb = gen_keyb(cur_ques)
    txt = ques(cur_ques)
    await message.answer(txt,reply_markup=keyb)

@R.message(Command("myprogress"))
async def start_func(message: types.Message):
    telegram_user_id = message.from_user.id
    user_info = db_users.get_user_by_telegram_id(telegram_user_id)
    if user_info:
        await message.reply(format_user_info_string(user_info))
    else:
        await message.reply(f"User with your ID: <b>{telegram_user_id}</b> is not registred")

@R.message(Command("deleteme"))
async def delete_func(message: types.Message):
    telegram_user_id = message.from_user.id
    db_users.delete_user(telegram_user_id)
    await message.answer("Ваш аккаунт видалено")

@R.message(Command("start"))
async def start_func(message: types.Message, state: FSMContext):
    await message.answer("Вітаємо тебе у боті для вивчення англіської🇬🇧")
    await message.answer("Щоб почати напиши мені своє ім'я")
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
    if len(phone) == 10 and phone.isnumeric():
        await state.update_data(phone=phone)
        data  = await state.get_data()

        db_users.update_user(
            username=message.from_user.username,
            name=data.get("name"),
            surname=data.get("surname"),
            lvl=None,
            phone_number=data.get("phone"),
            telegram_user_id=message.from_user.id
        )

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

@R.message(Command("howdoisay"))
async def translate(message: types.Message, state: FSMContext):
    await message.answer("З якої мови бажаєш перкласти?",reply_markup=lang_kb)
    await state.set_state(transl.choose)

@R.message(transl.choose)
async def choose(message: types.Message, state: FSMContext):
    if message.text=='З англійської':
        await message.answer("Напиши слово чи фразу англійською мовою яку хочеш перекласти", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(transl.eng_answer)
    elif message.text=='З української':
        await message.answer("Напиши слово чи фразу українською мовою яку хочеш перекласти", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(transl.ukr_answer)
        
@R.message(transl.eng_answer)
async def translated_eng(message: types.Message, state: FSMContext):
    text = str(message.text)
    answer = eng(text)
    await state.clear()
    await message.answer(f"Ось перекладена фраза/слово: {answer}")
    
@R.message(transl.ukr_answer)
async def translated_ukr(message: types.Message, state: FSMContext):
    text = str(message.text)
    answer = ukr(text)
    await state.clear()
    await message.answer(f"Ось перекладена фраза/слово: {answer}")

@R.message(ST.q1)
async def question1(message: types.Message, state: FSMContext):
    global cur_ques
    global correct_answers
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        correct_answers+=1
        cur_ques += 1
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
    global correct_answers
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        correct_answers+=1
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
    global correct_answers
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        correct_answers+=1
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
    global correct_answers
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        correct_answers+=1
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
    global correct_answers
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        correct_answers+=1
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
    global correct_answers
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        correct_answers+=1
        keyb = gen_keyb(cur_ques)
        await message.answer("+")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q7)
    else:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("-")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q7)

@R.message(ST.q7)
async def question1(message: types.Message, state: FSMContext):
    global cur_ques
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    if answer == True:
        cur_ques += 1
        correct_answers+=1
        keyb = gen_keyb(cur_ques)
        await message.answer("+")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q8)
    else:
        cur_ques += 1
        keyb = gen_keyb(cur_ques)
        await message.answer("-")
        txt = ques(cur_ques)
        await message.answer(f"{txt}",reply_markup=keyb)
        await state.set_state(ST.q8)

@R.message(ST.q8)
async def question1(message: types.Message, state: FSMContext):
    global cur_ques
    user_ans = message.text
    answer = check_ans(cur_ques,user_ans)
    telegram_user_id = message.from_user.id
    if answer == True:
        correct_answers=0
        correct_answers+=1
        await state.clear()
        await message.answer("+")
        lvlok = lvl(correct_answers)
        db_users.update_lvl(telegram_user_id=telegram_user_id, lvl=lvlok)
        await message.answer(f"Ти набрав {correct_answers} вірних відповідей")
        await message.answer(f"Нашим дуже крутим аналізатором було вирішено ,що у тебе {lvlok}",reply_markup=types.ReplyKeyboardRemove())
        correct_answers=0

    else:
        db_users.update_lvl(telegram_user_id=telegram_user_id, lvl=lvlok)
        await state.clear()
        await message.answer("-")
        await message.answer(f"Ти набрав {correct_answers} вірних відповідей")
        await message.answer(f"Нашим дуже крутим аналізатором було вирішено ,що у тебе {lvlok}",reply_markup=types.ReplyKeyboardRemove())
        correct_answers=0
        correct_answers=0
