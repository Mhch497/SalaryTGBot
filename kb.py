from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Какие занятия сегодня?")],
    [KeyboardButton(text="Добавить отработку")],
    [KeyboardButton(text="Добавить переработку")],
    [KeyboardButton(text="Отметить занятие")]
], resize_keyboard=True)
exit_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню",
                                           callback_data="menu")]])

extras_minutes = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='30 минут', callback_data='30'),
         InlineKeyboardButton(text='1 час', callback_data='60'),
         InlineKeyboardButton(text='1.5 часа', callback_data='90'),]
         ], resize_keyboard=True)

schools = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Уральская, 59', callback_data='ur'),
            InlineKeyboardButton(text='Эврика', callback_data='evrika')
        ],
        [
            InlineKeyboardButton(text='ЖБИ', callback_data='zhbi'),
            InlineKeyboardButton(text='Пышма', callback_data='pyshma')
        ]
    ], resize_keyboard=True)


completed_lesson = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='Yes'),
         InlineKeyboardButton(text='Нет', callback_data='No'),]
    ], resize_keyboard=True)


completed_extras = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='Yes_extras'),
         InlineKeyboardButton(text='Нет', callback_data='No_extras'),]
    ], resize_keyboard=True)

#  TODO переделать кнопки
# all_lessons_list = utils.readDatabaseSheduel(config.FILENAME)
# builder = InlineKeyboardBuilder()

# for lesson in all_lessons_list:
#     callback = ''
#     if lesson["Школа"] == 'Уральская':
#         callback += 'ur'
#     elif lesson["Школа"] == 'ЖБИ':
#         callback += 'zhbi'
#     elif lesson["Школа"] == 'Эврика':
#         callback += 'evrika'
#     elif lesson["Школа"] == 'Пышма':
#         callback += 'pyshma'
#     callback += str(lesson["Дата"])
#     callback += str(lesson["Время начала"]
#                     )[:str(lesson["Время начала"]).find(':')]
#     builder.button(text=f'{lesson["Группа"]}', callback_data=f"{callback}")
# builder.adjust(2)
