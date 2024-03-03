from aiogram.fsm.state import StatesGroup, State


class Extras_info(StatesGroup):
    time = State()
    school = State()
    pupil = State()

class WorkingOff_info(StatesGroup):
    school = State()
    pupils = State()
    group = State()

class Current_lesson(StatesGroup):
    done = State()
    pupils = State()
    reason = State()
    extras = State()

class Forgotten_lesson(StatesGroup):
    done = State()
    pupils = State()
    reason = State()
    extras = State()