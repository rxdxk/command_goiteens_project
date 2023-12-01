from aiogram.fsm.state import StatesGroup, State




class TC(StatesGroup):
    ch = State()

class ST(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    final = State()

class AT(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    final = State()