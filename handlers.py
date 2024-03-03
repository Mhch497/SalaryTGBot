from aiogram import types, F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import kb
import text
from aiogram.fsm.context import FSMContext
import utils
from states import WorkingOff_info, Extras_info, Current_lesson, Forgotten_lesson
import config

router = Router() #создаём роутер для дальнешей привязки к нему обработчиков

data = dict()
#Command("start") запускает обработчик только если входящее сообщение — команда /start
@router.message(Command("start")) #функция является обработчиком входящих сообщений.
async def start_handler(msg: Message):
    await msg.answer("Привет, выбери кнопку", reply_markup=kb.menu)
    #msg.answer("Text"), что является аналогом await bot.send_message(msg.chat.id, "Text").

# @router.message() #реагирует на все сообщения, так как у него не задан ни один фильтр.
# async def message_handler(msg: Message):
#     await msg.answer(f"Твой ID: {msg.from_user.id}")

@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer('Главное меню', reply_markup=kb.menu)

@router.message(F.text == "Какие занятия сегодня?")
async def print_today_lessons(msg: Message):#, state: FSMContext):
    # await state.set_state(Gen.text_prompt)
    # await clbck.message.edit_text(text.gen_text)
    # await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)
    await msg.answer(utils.write_lessons(), reply_markup=kb.exit_kb)

# @router.message(Gen.text_prompt)#брабатываем сообщения с фильтром состояния @router.message(Gen.text_prompt). Это означает что функция будет реагировать только на те входящие сообщения, которые были отправлены после установки состояния в предыдущей функции.
# async def generate_text(msg: Message, state: FSMContext):
#     prompt = msg.text
#     mesg = await msg.answer(text.gen_wait)
#     res = await utils.generate_text(prompt)
#     if not res:
#         return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
#     await mesg.edit_text(res[0] + text.text_watermark, disable_web_page_preview=True)

@router.message(F.text == "Добавить отработку") #функция будет реагировать на нажатия inline-кнопок с определённым фильтром
async def ask_extras_time(msg: Message, state: FSMContext):
        await state.set_state(Extras_info.time)
        await msg.delete()
        await msg.answer(text=f'Сколько длилась отработка?', reply_markup=kb.extras_minutes)


# @router.callback_query(F.data == "30")
# @router.callback_query(F.data == "60")
# @router.callback_query(F.data == "90")
@router.callback_query(Extras_info.time)
async def ask_extras_school(clb: CallbackQuery, state: FSMContext):
    await state.set_state(Extras_info.school)
    count = int(clb.data)
    data['time'] = count
    await clb.message.delete()
    await clb.message.answer(text=f'В какой школе?', reply_markup=kb.schools)


# @router.callback_query(F.data == "ur")
# @router.callback_query(F.data == "zhbi")
# @router.callback_query(F.data == "evrika")
# @router.callback_query(F.data == "pyshma")
@router.callback_query(Extras_info.school)
async def ask_extras_pupil(clb: CallbackQuery, state: FSMContext):
    await state.set_state(Extras_info.pupil)
    schoolname = clb.data
    data['school'] = config.SCHOOLS[schoolname]
    await clb.message.delete()
    await clb.message.answer('Ученик')

@router.message(Extras_info.pupil)  # функция будет реагировать на нажатия inline-кнопок с определённым фильтром
async def print_extras(msg: Message, state: FSMContext):
    global data
    data['pupil'] = msg.text
    await msg.delete()
    await msg.answer(utils.get_text_extras(data))
    utils.save_extras_excel(data)
    await state.clear()
    data = dict()



@router.message(F.text == "Добавить переработку")  # функция будет реагировать на нажатия inline-кнопок с определённым фильтром
async def ask_working_off_school(msg: Message, state: FSMContext):
    await state.set_state(WorkingOff_info.school)
    await msg.delete()
    await msg.answer(text=f'В какой школе?', reply_markup=kb.schools)

@router.callback_query(WorkingOff_info.school)
async def ask_workingOff_group(clb: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state in WorkingOff_info:
        pass
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
            utils.save_lesson_excel(data)
            await state.clear()
            data = dict()
        except:
            await msg.answer(text=f'Необходимо ввести число')

@router.callback_query(Forgotten_lesson.done)
@router.callback_query(F.data == 'Yes')
@router.callback_query(F.data == 'No')
async def ask_pupils_or_reason(clb: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    done = clb.data
    if done == 'Yes':
        if current_state in Forgotten_lesson:
            await state.set_state(Forgotten_lesson.pupils)
        else:
            await state.set_state(Current_lesson.pupils)
        await clb.message.delete()
        data['done'] = True
        await clb.message.answer('Сколько учеников было?')
    elif done == "No":
        if current_state in Forgotten_lesson:
            await state.set_state(Forgotten_lesson.reason)
        else:
            await state.set_state(Current_lesson.reason)
        await clb.message.delete()


        await clb.message.delete()
        data['done'] = False
        await clb.message.answer('По какой причине?')

@router.message(Current_lesson.pupils)
@router.message(Forgotten_lesson.pupils)
async def print_done_lesson_info(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    try:
        global count
        count = int(msg.text)
        data['count'] = count
        if current_state in Forgotten_lesson:
            await state.set_state(Forgotten_lesson.extras)
        else:
            await state.set_state(Current_lesson.extras)

        await msg.delete()
        await msg.answer(text=f'Отработка до или после занятия была?', reply_markup=kb.completed_extras)
    except:
        await msg.answer(text=f'Необходимо ввести число')

@router.callback_query(Current_lesson.extras)
@router.callback_query(Forgotten_lesson.extras)
async def ask_pupils_or_reason(clb: CallbackQuery, state: FSMContext):
    global data
    data['extras'] = (True if clb.data == 'Yes_extras' else False )
    await clb.message.answer(utils.print_lesson(data))
    utils.save_lesson_excel(data)
    await state.clear()
    data = dict()


@router.message(Current_lesson.reason)
@router.message(Forgotten_lesson.reason)
async def print_undone_lesson_info(msg: Message, state: FSMContext):
    global data
    data['message'] = msg.text
    await msg.answer(utils.print_lesson(data))
    utils.save_lesson_excel(data)
    await state.clear()
    data = dict()


@router.message(F.text == "Отметить занятие")  # функция будет реагировать на нажатия inline-кнопок с определённым фильтром
async def ask_working_off_school(msg: Message, state: FSMContext):
    await state.set_state(WorkingOff_info.school)
    await msg.delete()
    await msg.answer(text=f'Выбери группу', reply_markup=kb.builder.as_markup())





async def start_shedule( lesson: dict,  bot: Bot):
    # state = FSMContext
    # await state.set_state(Current_lesson.done)
    # lesson = args[0]
    # bot = args[1]
    data['lesson'] = lesson
    await bot.send_message(config.my_ID, text=f'Занятиие {lesson["Группа"]} состоялось?', reply_markup=kb.completed_lesson)
