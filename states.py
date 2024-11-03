"""Файл для хранения состояний разных групп."""
from aiogram.fsm.state import StatesGroup, State


class Extras_info(StatesGroup):
    """Класс состояний для отработок."""

    time = State()
    school = State()
    pupil = State()


class Sheduled_Extras_info(StatesGroup):
    """Класс состояний для отработок по расписанию."""

    time = State()


class WorkingOff_info(StatesGroup):
    """Класс состояний для переработок."""

    school = State()
    pupils = State()
    group = State()


class Current_lesson(StatesGroup):
    """Класс состояний для уроков по расписанию."""

    done = State()
    pupils = State()
    reason = State()
    extras = State()


class Forgotten_lesson(StatesGroup):
    """Класс состояний для незаполненных уроков по причине выкл бота."""

    done = State()
    pupils = State()
    reason = State()
    extras = State()
    school = State()
