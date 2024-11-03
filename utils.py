import datetime

import config
from config import KEYS
import openpyxl
import API


# def write_lessons():
#     today = datetime.date.today()
#     global weekday
#     weekday = today.weekday() + 1
#     today_lessons = readDatabase(FILENAME, weekday)
#     lessons_message = ''
#     if len(today_lessons) >= 1:
#         i = 1
#         for elem in today_lessons:
#             lessons_message += f"{elem['Время начала']} - {elem['Группа']}\n"
#             i += 1

#     return 'Занятия сегодня: \n' + lessons_message

def write_lessons():
    """Печать расписаний на сегодня."""

    today_lessons = API.get_group_lessons()
    lessons_message = ''
    if len(today_lessons) >= 1:
        for elem in today_lessons:
            if elem['Тип урока'] in ["Индивидуальный урок", "Отработка"]:
                lessons_message += (f"{elem['Тип урока']}:\n"
                                    f"{elem['Время начала'].strftime('%H:%M')}"
                                    f" - {', '.join(elem['Ученики'])}"
                                    f" ({elem['Группа']})\n")
            else:
                lessons_message += (f"{elem['Тип урока']}:\n"
                                    f"{elem['Время начала'].strftime('%H:%M')}"
                                    f" - {elem['Группа']}\n")
    return 'Занятия сегодня: \n' + lessons_message


# def readDatabase(filename, weekday):
#     try:
#         wb = openpyxl.load_workbook(filename)
#         sheet = wb.active
#         today_lessons = []
#         for result in sheet['B']:
#             if result.internal_value == weekday:
#                 res_row = result.row
#                 dict_lesson = {}
#                 i = 0
#                 for letter in 'ABCDE':
#                     dict_lesson[str(KEYS[i])] = (sheet[letter + str(res_row)]
#                                                  ).internal_value
#                     today_lessons.append(dict_lesson)
#                     i += 1
#         return today_lessons
#     except FileNotFoundError:
#         print('Файл не найден')


# def readDatabaseSheduel(filename):
#     try:
#         wb = openpyxl.load_workbook(filename)
#         sheet = wb.active
#         today_lessons = []
#         for result in sheet['B']:
#             if result.internal_value != 'День':
#                 res_row = result.row
#                 dict_lesson = {}
#                 i = 0
#                 for letter in 'ABCDE':
#                     dict_lesson[str(KEYS[i])] = (sheet[letter + str(res_row)]
#                                                  ).internal_value
#                 today_lessons.append(dict_lesson)
#         return today_lessons
#     except FileNotFoundError:
#         print('Файл не найден')


def get_text_extras(data):
    """Формирование текста отработки."""

    date = datetime.date.today()
    day = date.day
    month = date.month
    students = ', '.join(data['lesson']['Ученики']
                         ) if 'pupil' not in data else data['pupil']
    school = data['lesson']['Школа'] if 'school' not in data else data['school']
    lesson = data['lesson']['Группа'] if 'lesson' in data else ''
    cost = int(200 * data["time"] / 30)
    data_save = {
        'school': school,
        'cost': cost,
        'Pupils': students
    }
    save_extras_excel(data_save)
    return (f'{"0" + str(day) if day < 10 else str(day)}.'
            f'{"0" + str(month) if month < 10 else str(month)}.'
            f'{str(date.year)}\n'
            f"Отработка: {students} ({lesson})\n"
            f'Школа: {school}\n'
            f'Сумма: {cost}\n'
            f'#зарплата')


def print_overwork(data):
    """Печать переработки."""

    lesson = data['lesson']
    date = datetime.date.today()
    day = date.day
    month = date.month
    cost = (350 + 100 * data["count"] if data["count"] > 3 else 700
            ) if data['lesson']["Тип урока"].find('Онлайн') == -1 else (600 + 60 * data["count"])
    data_save = {
        'group': lesson['Группа'],
        'school': lesson["Школа"],
        'count': data["count"],
        'cost': cost,
        'extras': 200 if data["extras"] else 0,
        'done': True
    }
    save_lesson_excel(data_save)
    return (f'{"0" + str(day) if day < 10 else str(day)}.'
            f'{"0" + str(month) if month < 10 else str(month)}.'
            f'{str(date.year)}\n'
            'Замена преподавателя\n'
            f'Школа: {data["school"]}\n'
            f'Количество детей: {data["count"]}\n'
            f'Стоимость занятия: {cost}\n'
            f'Отработка: {200 if data["extras"] else 0}\n'
            '#зарплата')


def print_lesson(data):  # TODO Добавить онлайн/офлайн
    """Печать урока."""

    lesson = data['lesson']
    date = datetime.date.today()
    day = date.day
    month = date.month
    data_save = {
        'group': lesson['Группа'],
        'school': lesson["Школа"],
        'count': data["count"],
        'done': data['done'],
    }
    if data['done']:
        cost = (350 + 100 * data["count"] if data["count"] > 3 else 700
                ) if data['lesson']["Тип урока"].find('Онлайн') == -1 else (600 + 60 * data["count"])
        data_save['cost'] = cost
        data_save['extras'] = 200 if data["extras"] else 0,
        save_lesson_excel(data_save)
        return (f'{"0" + str(day) if day < 10 else str(day)}.'
                f'{"0" + str(month) if month < 10 else str(month)}.'
                f'{str(date.year)}\n'
                f'Группа: {lesson["Группа"]}\n'
                f'Школа: {lesson["Школа"]}\n'
                f'Количество детей: {data["count"]}\n'
                f'Стоимость занятия: {cost}\n'
                f'Отработка: {200 if data["extras"] else 0}\n'
                '#зарплата')
    else:
        data_save['message'] = data["message"]
        save_lesson_excel(data_save)
        return (f'{"0" + str(day) if day < 10 else str(day)}.'
                f'{"0" + str(month) if month < 10 else str(month)}.'
                f'{str(date.year)}\n'
                f'Группа: {lesson["Группа"]}\n'
                f'Школа: {lesson["Школа"]}\n'
                f'Причина: {data["message"]}\n'
                '#зарплата')


def save_lesson_excel(data):
    """Сохранение урока в Эксель."""

    try:
        wb = openpyxl.load_workbook(config.SAVE_fILENAME)
        sheet = wb.active
        now = datetime.datetime.now()
        sheet.append([
            data['school'],
            now,
            data['group'],
            350 if data['done'] else 0,
            100,
            data["count"] if data['done'] else 0,
            200 if data["extras"] else 0,
            data['cost'] + (200 if data["extras"] else 0),
            data["message"] if 'message' in data else ''
        ])
        wb.save(config.SAVE_fILENAME)
    except FileNotFoundError:
        print('Файл не найден')


def save_extras_excel(data):
    """Сохранение отработки в Эксель."""

    try:
        wb = openpyxl.load_workbook(config.SAVE_fILENAME)
        sheet = wb.active
        now = datetime.datetime.now()
        sheet.append([
            data['school'],
            now,
            "Отработка " + data['Pupils'],
            0,
            0,
            0,
            data['cost'],
            data['cost']
        ])
        wb.save(config.SAVE_fILENAME)
    except FileNotFoundError:
        print('Файл не найден')
