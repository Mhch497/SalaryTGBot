from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

import utils
import config
menu = [
    [KeyboardButton(text="Какие занятия сегодня?")],
    [KeyboardButton(text="Добавить отработку")],
    [KeyboardButton(text="Добавить переработку")],
    [KeyboardButton(text="Отметить занятие")]
]
menu = ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

extras_minutes = [
    [
    InlineKeyboardButton(text='30 минут', callback_data='30'),
    InlineKeyboardButton(text='1 час', callback_data='60'),
    InlineKeyboardButton(text='1.5 часа', callback_data='90'),]
]
extras_minutes = InlineKeyboardMarkup(inline_keyboard=extras_minutes, resize_keyboard=True)

schools = [
        [
            InlineKeyboardButton(text='Уральская, 59', callback_data='ur'),
            InlineKeyboardButton(text='Эврика', callback_data='evrika')

        ],
        [
            InlineKeyboardButton(text='ЖБИ', callback_data='zhbi'),
            InlineKeyboardButton(text='Пышма', callback_data='pyshma')
        ]
]

schools = InlineKeyboardMarkup(inline_keyboard=schools, resize_keyboard=True)

completed_lesson = [
    [
    InlineKeyboardButton(text='Да', callback_data='Yes'),
    InlineKeyboardButton(text='Нет', callback_data='No'),]
]
completed_lesson = InlineKeyboardMarkup(inline_keyboard=completed_lesson, resize_keyboard=True)

completed_extras = [
    [
    InlineKeyboardButton(text='Да', callback_data='Yes_extras'),
    InlineKeyboardButton(text='Нет', callback_data='No_extras'),]
]
completed_extras = InlineKeyboardMarkup(inline_keyboard=completed_extras, resize_keyboard=True)

all_lessons_list = utils.readDatabaseSheduel(config.FILENAME)
builder = InlineKeyboardBuilder()

for lesson in all_lessons_list:
    callback = ''
    if lesson["Школа"] == 'Уральская':
        callback += 'ur'
    elif lesson["Школа"] == 'ЖБИ':
        callback += 'zhbi'
    elif lesson["Школа"] == 'Эврика':
        callback += 'evrika'
    elif lesson["Школа"] == 'Пышма':
        callback += 'pyshma'
    callback += str(lesson["Дата"])
    callback += str(lesson["Время начала"])[:str(lesson["Время начала"]).find(':')]
    builder.button(text=f'{lesson["Группа"]}', callback_data = f"{callback}")
builder.adjust(2)


"""builder = InlineKeyboardBuilder()
for i in range(15):
    builder.button(text=f”Кнопка {i}”, callback_data=f”button_{i}”)
builder.adjust(2)
await msg.answer(“Текст сообщения”, reply_markup=builder.as_markup())
Здесь мы создаём Keyboard Builder и в цикле добавляем в него кнопки.
builder.adjust(2) группирует кнопки в 2 столбца. 
Далее отправляется сообщение с созданной клавиатурой, 
которая из Keyboard Builder преобразовывается в Keyboard Markup 
функцией builder.as_markup() ."""