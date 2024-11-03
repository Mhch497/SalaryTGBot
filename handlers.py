import os

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv

import config
import kb
import utils
from states import (Current_lesson, Extras_info, Forgotten_lesson,
                    Sheduled_Extras_info, WorkingOff_info)

router = Router()
data = dict()
load_dotenv()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет, выбери кнопку", reply_markup=kb.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer('Главное меню', reply_markup=kb.menu)


@router.message(F.text == "Какие занятия сегодня?")
async def print_today_lessons(msg: Message):
    await msg.answer(utils.write_lessons(), reply_markup=kb.exit_kb)


@router.message(F.text == "Добавить отработку")
async def ask_extras_time(msg: Message, state: FSMContext):
    await state.set_state(Extras_info.time)
    await msg.delete()
    await msg.answer(text='Сколько длилась отработка?',
                     reply_markup=kb.extras_minutes)


@router.message(F.text == "Добавить отработку")
async def ask_extras_time(msg: Message, state: FSMContext):
    await state.set_state(Extras_info.time)
    await msg.delete()
    await msg.answer(text='Сколько длилась отработка?',
                     reply_markup=kb.extras_minutes)


@router.callback_query(Extras_info.time)
async def ask_extras_school(clb: CallbackQuery, state: FSMContext):
    await state.set_state(Extras_info.school)
    count = int(clb.data)
    data['time'] = count
    await clb.message.delete()
    await clb.message.answer(text='В какой школе?', reply_markup=kb.schools)


@router.callback_query(Extras_info.school)
async def ask_extras_pupil(clb: CallbackQuery, state: FSMContext):
    await state.set_state(Extras_info.pupil)
    schoolname = clb.data
    data['school'] = config.SCHOOLS[schoolname]
    await clb.message.delete()
    await clb.message.answer('Ученик')


@router.message(Extras_info.pupil)
async def print_extras(msg: Message, state: FSMContext):
    global data
    data['pupil'] = msg.text
    await msg.delete()
    await msg.answer(utils.get_text_extras(data))
    await state.clear()
    data = dict()


@router.message(F.text == "Добавить переработку")
async def ask_working_off_school(msg: Message, state: FSMContext):
    await state.set_state(WorkingOff_info.school)
    await msg.delete()
    await msg.answer(text='В какой школе?', reply_markup=kb.schools)


@router.callback_query(WorkingOff_info.school)
async def ask_workingOff_group(clb: CallbackQuery, state: FSMContext):
    await state.set_state(WorkingOff_info.group)
    schoolname = clb.data
    data['school'] = config.SCHOOLS[schoolname]
    await clb.message.delete()
    await clb.message.answer('Группа')


@router.message(WorkingOff_info.group)
async def ask_workingOff_pupil(msg: Message, state: FSMContext):
    await state.set_state(WorkingOff_info.pupils)
    data['group'] = msg.text
    await msg.delete()
    await msg.answer('Сколько учеников было?')


@router.message(WorkingOff_info.pupils)
async def print_workingOff(msg: Message, state: FSMContext):
    await msg.delete()
    try:
        global data
        count = int(msg.text)
        data['count'] = count
        await msg.answer(utils.print_overwork(data))
        await state.clear()
        data = dict()
    except ValueError:
        await msg.answer(text='Необходимо ввести число')


@router.callback_query(Forgotten_lesson.done)
@router.callback_query(F.data == 'Yes')
@router.callback_query(F.data == 'No')
async def ask_pupils_or_reason(clb: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    done = clb.data
    if done == 'Yes':
        if current_state in Forgotten_lesson:
            await state.set_state(Forgotten_lesson.pupils)
            await clb.message.delete()
            data['done'] = True
            await clb.message.answer('Сколько учеников было?')
        elif data['lesson']['Тип урока'] in ["Индивидуальный урок",
                                             "Отработка"]:
            await state.set_state(Sheduled_Extras_info.time)
            await clb.message.delete()
            data['done'] = True
            await clb.message.answer(
                'Сколько длилась отработка?',
                reply_markup=kb.extras_minutes)
        else:
            await state.set_state(Current_lesson.pupils)
            await clb.message.delete()
            data['done'] = True
            await clb.message.answer('Сколько учеников было?')
    elif done == "No":
        if current_state in Forgotten_lesson:
            await state.set_state(Forgotten_lesson.reason)
        elif data['lesson']['Тип урока'] in ["Индивидуальный урок",
                                             "Отработка"]:
            await state.set_state(Sheduled_Extras_info.final)
        else:
            await state.set_state(Current_lesson.reason)
        await clb.message.delete()
        data['done'] = False
        await clb.message.answer('По какой причине?')


@router.callback_query(Sheduled_Extras_info.time)
async def print_shed_extras(clb: CallbackQuery, state: FSMContext):
    global data
    count = int(clb.data)
    data['time'] = count
    await clb.message.delete()
    await clb.message.answer(utils.get_text_extras(data))
    await state.clear()
    data = dict()


@router.message(Current_lesson.pupils)
@router.message(Forgotten_lesson.pupils)
async def print_done_lesson_info(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    try:
        count = int(msg.text)
        data['count'] = count
        if current_state in Forgotten_lesson:
            await state.set_state(Forgotten_lesson.extras)
        else:
            await state.set_state(Current_lesson.extras)
        await msg.delete()
        await msg.answer(text='Отработка до или после занятия была?',
                         reply_markup=kb.completed_extras)
    except ValueError:
        await msg.answer(text='Необходимо ввести число')


@router.callback_query(Current_lesson.extras)
@router.callback_query(Forgotten_lesson.extras)
async def save_extras(clb: CallbackQuery, state: FSMContext):
    global data
    data['extras'] = (True if clb.data == 'Yes_extras' else False)
    await clb.message.answer(utils.print_lesson(data))
    await state.clear()
    data = dict()


@router.message(Current_lesson.reason)
@router.message(Forgotten_lesson.reason)
async def print_undone_lesson_info(msg: Message, state: FSMContext):
    global data
    data['message'] = msg.text
    await msg.answer(utils.print_lesson(data))
    await state.clear()
    data = dict()


@router.message(F.text == "Отметить занятие")
async def ask_forgotten_school(msg: Message, state: FSMContext):
    await state.set_state(Forgotten_lesson.school)
    await msg.delete()
    await msg.answer(text='Выбери группу', reply_markup=kb.builder.as_markup())


@router.callback_query(Forgotten_lesson.school)
async def write_forgotten_lesson(clb: CallbackQuery, state: FSMContext):
    all_lessons_list = utils.readDatabaseSheduel(config.FILENAME)
    school = clb.data[:len(clb.data)-3]
    date = clb.data[len(clb.data)-3:len(clb.data)-2]
    time = clb.data[len(clb.data)-2:]
    lesson = (list(filter(lambda x: x['Школа'] == config.SCHOOLS[school]
                          and str(x["Дата"]) == date
                          and str(x["Время начала"]
                                  )[:str(x["Время начала"]
                                         ).find(':')] == time,
                          all_lessons_list)))
    await state.set_state(Forgotten_lesson.done)
    data['lesson'] = lesson[0]
    await clb.message.answer('Занятиие состоялось?',
                             reply_markup=kb.completed_lesson)


async def start_shedule(lesson: dict,  bot: Bot):
    data['lesson'] = lesson
    if lesson['Тип урока'] in ["Индивидуальный урок", "Отработка"]:
        lessons_message = (f"{lesson['Тип урока']}:\n"
                           f"{', '.join(lesson['Ученики'])}"
                           f" ({lesson['Группа']})\n")
    else:
        lessons_message = (f"{lesson['Тип урока']}:\n"
                           f"{lesson['Группа']}\n")
    await bot.send_message(os.getenv('MY_ID'),
                           text='Занятие состоялось?\n' + lessons_message,
                           reply_markup=kb.completed_lesson)
