from aiogram import types,Router,F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from db_api.db_users import *
from loader import dp, R, db_users
from .translator import translate_eng as eng
from .translator import translate_ukr as ukr
from .tests import *
from .keyboards import *
from .learn import *
from .states import *
import random

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
        
lvls = {"a1":questions_a1,
        "a2":questions_a2,
        "b1":questions_b1,
        "b2":questions_b2,
        "c1":questions_c1,
        "c2":questions_c2}

eng_levels = ["A1","A2","B1","B2","C1","C2"]

def dynamic_reply_kb(options: list):
    return types.ReplyKeyboardMarkup(
        keyboard = [
            [types.KeyboardButton(text=option) for option in options] 
        ], resize_keyboard=True
    )

def question_generator(prev_number,curr_number, state_name, next_state,test_name):
    @dp.message(state_name, F.text.in_(test_name[prev_number]['options']))
    async def questiongen(message: types.Message, state: FSMContext):
        our_data = await state.get_data()
        print(message.text)
        right_ans = test_name[prev_number]["answer"]
        if message.text == right_ans:
            await state.update_data(
                {
                    "score":our_data['score'] + test_name[prev_number]["point"],
                    "name":test_name[3]['answer']
                }
            
            )
        our_data = await state.get_data()
        print(our_data)
        print(f"1111111111111:{our_data['score']}")
        await message.answer(f"Відповідь зарахована")
        await message.answer(f"Ти відповів:{message.text}")
        await message.answer(f"Правильна відповідь:{right_ans}")
        await message.answer(f"{curr_number} Питання:")
        await message.answer(test_name[curr_number]["question"], reply_markup=dynamic_reply_kb(test_name[curr_number]["options"]))
        await state.set_state(next_state)
def init_questions():
    question_generator(1, 2, ST.q2, ST.q3,questions_start)
    question_generator(1, 2, ST.q2, ST.q3,questions_start)
    question_generator(2, 3, ST.q3, ST.q4,questions_start)
    question_generator(3, 4, ST.q4, ST.q5,questions_start)
    question_generator(4, 5, ST.q5, ST.q6,questions_start)
    question_generator(5, 6, ST.q6, ST.final,questions_start)
    for x in lvls.values():
        question_generator(1,2, AT.q2, AT.q3,x)
        question_generator(2,3, AT.q3, AT.final,x)

@dp.message(ST.final)
async def final_score(message: types.Message, state: FSMContext):
    telegram_user_id = message.from_user.id
    our_data = await state.get_data()
    right_ans = questions_start[6]["answer"]
    if message.text == right_ans:
        await message.answer(f"Ти відповів:{message.text}")
        await message.answer(f"✅Правильна відповідь:{right_ans}")
        our_data['score'] += 1
    print(our_data)
    score = our_data['score']
    await message.answer("Давай підрахуємо твої результати📝",reply_markup=types.ReplyKeyboardRemove())
    eng_levels.insert(0,"A0")
    for x in range(len(eng_levels)):
        if score == x:
            await message.answer(eng_levels[x])
            lvl = eng_levels[x]
            db_users.update_lvl(telegram_user_id=telegram_user_id, lvl=lvl)
        await state.clear()
    eng_levels.pop(0)
    await state.set_state(TC.ch)
    await state.update_data(score=0)
    await message.answer("📋Для інформації про бота /info")
    await message.answer("📚Ось бібліотека тестів",reply_markup=dynamic_reply_kb(eng_levels))

@dp.message(AT.final)
async def final_score(message: types.Message, state: FSMContext):
    our_data = await state.get_data()
    print(our_data)
    right_ans = our_data["name"]
    if message.text == right_ans:
        await message.answer(f"Ти відповів:{message.text}")
        await message.answer(f"✅Правильна відповідь:{right_ans}")
        our_data['score'] += 1
    score = our_data['score']

    await message.answer("Давай підрахуємо твої результати",reply_markup=types.ReplyKeyboardRemove())
    await message.answer(f"Ти набрав {score} з 3")
    await state.set_state(TC.ch)
    await state.update_data(score=0)
    await message.answer("Ось бібліотека тестів",reply_markup=dynamic_reply_kb(eng_levels))

def format_user_info_string(user_info: tuple):
        return f"""
    <b>
👨First Name: {user_info[1]}
👨Last Name: {user_info[2]}
🆔Telegram ID: {user_info[3]}
☎️Phone Number: +380{user_info[4]}
🇬🇧English Level: {user_info[5]}
    </b>
    """

@dp.message(Command("info"))
async def info_func(message: types.Message):
    await message.answer('''<b>Що може цей бот❓</b>
    <i>-Визначити твій рівень англійської🇬🇧
    -Допомогти прокачати свої знання🧠
    -Давати рекомендації щодо вивчення нових слів та правил🤔
    -Давати завдання🧑‍💻
    -Допомогти тобі провести час із користю🕓</i>
    ''')

@dp.message(Command("myprogress"))
async def progres_func(message: types.Message):
    telegram_user_id = message.from_user.id
    user_info = db_users.get_user_by_telegram_id(telegram_user_id)
    print(user_info)
    if user_info:
        await message.reply(format_user_info_string(user_info))
    else:
        await message.reply(f"User with your ID: <b>{telegram_user_id}</b> is not registred🤷")

@dp.message(Command("deleteme"))
async def delete_func(message: types.Message):
    telegram_user_id = message.from_user.id
    db_users.delete_user(telegram_user_id)
    await message.answer("❌Ваш аккаунт видалено")

@dp.message(Command("updateme"))
async def delete_func(message: types.Message, state: FSMContext):
    await message.answer("🔄Давайте оновимо ваші данні, вкажіть нове ім'я")
    await state.set_state(update.name)

@dp.message(update.name)
async def surname_func(message: types.Message, state: FSMContext):
    name = message.text
    if len(name) < 12  and len(name) >= 3 and name.isalpha():
        await message.answer(f"🙋Hello {name}")
        await state.update_data(name=name)
        await state.set_state(update.surname)
        await message.answer(f"{name}, введи своє прізвище")
    else:
        await state.set_state(update.name)
        await message.answer("❌Введіть коректне ім'я")
    
@dp.message(update.surname)
async def surname_func(message: types.Message, state: FSMContext):
    surname = message.text
    if len(surname) < 20  and surname.isalpha():
        await state.update_data(surname=surname)
        await state.set_state(update.phone)
        await message.answer(f"☎️Тепер введи свій номер телефону ,починаючи з +38")   
    else:
        await state.set_state(update.surname)
        await message.answer(f"❌Введіть коректне прізвище")

@dp.message(update.phone)
async def phone_func(message: types.Message, state: FSMContext):
    phone = message.text
    telegram_user_id = message.from_user.id
    user_info = db_users.get_user_by_telegram_id(telegram_user_id)
    if len(phone) == 10 and phone.isnumeric():
        state_data=await state.get_data()
        surname=state_data["surname"]
        name=state_data["name"]
        db_users.update_user(
            name=name,
            surname=surname,
            lvl=None,
            phone=int(phone),
            telegram_user_id=telegram_user_id
        )                
        await message.answer("✅Оновлення профілю завершено!")
        await state.clear()
    else:
        await state.set_state(Form.phone)
        await message.answer("❌Введіть коректний номер")

@dp.message(Command("start"))
async def start_func(message: types.Message, state: FSMContext):
    await message.answer("Вітаємо тебе у боті для вивчення англіської🇬🇧")
    await message.answer("Щоб почати напиши мені своє ім'я")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name_func(message: types.Message, state: FSMContext):
    name = message.text
    if len(name) < 12  and len(name) >= 3 and name.isalpha():
        await message.answer(f"🙋Hello {name}")
        await state.update_data(name=name)
        await state.set_state(Form.surname)
        await message.answer(f"{name}, введи своє прізвище")
    else:
        await state.set_state(Form.name)
        await message.answer("❌Введіть коректне ім'я")

@dp.message(Form.surname)
async def surname_func(message: types.Message, state: FSMContext):
    surname = message.text
    if len(surname) < 20  and surname.isalpha():
        await state.update_data(surname=surname)
        await state.set_state(Form.phone)
        await message.answer(f"☎️Тепер введи свій номер телефону ,починаючи з +38")
    else:
        await state.set_state(Form.surname)
        await message.answer(f"❌Введіть коректне прізвище")

@dp.message(Form.phone)
async def phone_func(message: types.Message, state: FSMContext):
    phone = message.text
    telegram_user_id = message.from_user.id
    if len(phone) == 10 and phone.isnumeric():
        await state.update_data(phone=phone)
        state_data=await state.get_data()
        name=state_data["name"]
        surname=state_data["surname"]
        db_users.register_user(
            name=name,
            surname=surname,
            telegram_user_id=telegram_user_id,
            phone=phone,
            lvl=None
        )
        await message.answer("✅Реєстрацію завершено!")
        await message.answer("📋А зараз ми пропонуємо вам пройти короткий тест на ваш рівень англійської мови")
        await state.update_data(score=0)
        await message.answer(f"1 Питання:")
        await message.answer(questions_start[1]["question"], reply_markup=dynamic_reply_kb(questions_start[1]["options"]))
        await state.set_state(ST.q2)
    else:
        await state.set_state(Form.phone)
        await message.answer("❌Введіть коректний номер")

@dp.message(Command("learn"))
async def learn(message: types.Message):
    await message.answer(f"📹Ось тобі корисне відео:")
    await message.answer(f"{random.choice(links)}")
    await message.answer(f"🗣Лови нове слово:")
    word = str(random.choice(english_words))
    await message.answer(f"{word}")
    await message.answer(f"🔀Переклад:{eng(word)}")
    
@dp.message(Command("test"))
async def translate(message: types.Message, state: FSMContext):
    await message.answer("🚀Почнемо проходити тести!")
    await state.set_state(TC.ch)
    await state.update_data(score=0)
    await message.answer("📚Ось бібліотека тестів",reply_markup=dynamic_reply_kb(eng_levels))

@dp.message(Command("howdoisay"))
async def translate(message: types.Message, state: FSMContext):
    await message.answer("❓З якої мови бажаєш перкласти?",reply_markup=lang_kb)
    await state.set_state(transl.choose)

@dp.message(transl.choose)
async def choose(message: types.Message, state: FSMContext):
    if message.text=='З англійської🇬🇧':
        await message.answer("Напиши слово чи фразу англійською мовою яку хочеш перекласти", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(transl.eng_answer)
    elif message.text=='З української🇺🇦':
        await message.answer("Напиши слово чи фразу українською мовою яку хочеш перекласти", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(transl.ukr_answer)
        
@dp.message(transl.eng_answer)
async def translated_eng(message: types.Message, state: FSMContext):
    text = message.text
    answer = eng(text)
    await state.clear()
    await message.answer(f"✅Ось перекладена фраза/слово: {answer}")
    
@dp.message(transl.ukr_answer)
async def translated_ukr(message: types.Message, state: FSMContext):
    text = message.text
    answer = ukr(text)
    await state.clear()
    await message.answer(f"✅Ось перекладена фраза/слово: {answer}")

@dp.message(TC.ch)
async def main_handler(message: types.Message,state: TC):
    user_ans = message.text #A1
    if user_ans in eng_levels:
        await state.update_data(lvl=user_ans)
        await message.answer(f"📋Тест для рівня {user_ans}")
        await message.answer(f"1 Питання:")
        value = user_ans.lower() #a1
        if value in lvls:
            await message.answer(lvls[value][1]["question"], reply_markup=dynamic_reply_kb(lvls[value][1]["options"]))
        await state.set_state(AT.q2)
