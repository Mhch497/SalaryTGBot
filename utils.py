import datetime

import config
from config import FILENAME, my_ID
import openpyxl

def write_lessons():
    today = datetime.date.today()
    global weekday
    weekday = today.weekday() + 1
    # weekday = 3
    today_lessons = readDatabase(FILENAME, weekday)

    lessons_message = ''
    if len(today_lessons) >= 1:
        i = 1
        for elem in today_lessons:
            lessons_message += f"{elem['Время начала']} - {elem['Группа']}\n"
            i += 1

    return 'Занятия сегодня: \n' + lessons_message

def readDatabase(filename, weekday): #чтение информации из БД Notion
    try:
        wb = openpyxl.load_workbook(filename)
        sheet = wb.active
        now = datetime.datetime.now().time()
        str_now = str(now)
        today_lessons = []
        for result in sheet['B']:
            if result.internal_value == weekday:
                res_row = result.row
                dict_lesson = {}
                dict_lesson['Школа'] = sheet['A' + str(res_row)].internal_value
                dict_lesson['Дата'] = sheet['B' + str(res_row)].internal_value
                dict_lesson['Время начала'] = sheet['D' + str(res_row)].internal_value
                dict_lesson['Группа'] = sheet['C' + str(res_row)].internal_value
                dict_lesson['Время окончания'] = sheet['E' + str(res_row)].internal_value
                today_lessons.append(dict_lesson)
        return today_lessons
    except:
        print('Файл не найден')

def readDatabaseSheduel(filename): #чтение информации из БД Notion
    try:
        wb = openpyxl.load_workbook(filename)
        sheet = wb.active
        now = datetime.datetime.now().time()
        str_now = str(now)
        today_lessons = []
        for result in sheet['B']:
            if result.internal_value != 'День':
                res_row = result.row
                dict_lesson = {}
                dict_lesson['Школа'] = sheet['A' + str(res_row)].internal_value
                dict_lesson['Дата'] = sheet['B' + str(res_row)].internal_value
                dict_lesson['Время начала'] = sheet['D' + str(res_row)].internal_value
                dict_lesson['Группа'] = sheet['C' + str(res_row)].internal_value
                dict_lesson['Время окончания'] = sheet['E' + str(res_row)].internal_value
                today_lessons.append(dict_lesson)
        return today_lessons
    except:
        print('Файл не найден')

def get_text_extras(data):
    date = datetime.date.today()
    day = date.day
    month = date.month
    return (f'{"0" + str(day) if day < 10 else str(day)}.'
                                 f'{"0" + str(month) if month < 10 else str(month)}.'
                                 f'{str(date.year)}\n'
                                 f'Отработка: {data["pupil"]}\n'
                                 f'Школа: {data["school"]}\n'
                                 f'Сумма: {int(200 * data["time"] / 30)}\n'
                                 f'#зарплата')

def print_overwork(data): # Печать информации для зп
    date = datetime.date.today()
    day = date.day
    month = date.month
    return (f'{"0" + str(day) if day < 10 else str(day)}.'
                                 f'{"0" + str(month) if month < 10 else str(month)}.'
                                 f'{str(date.year)}\n'
                                 f'Замена преподавателя\n'
                                 f'Школа: {data["school"]}\n'
                                 f'Количество детей: {data["count"]}\n'
                                 f'Стоимость занятия: '
                                 f'{350 + 100 * data["count"] if data["count"] > 3 else 700}\n'
                                 f'#зарплата')


def print_lesson(data): # Печать информации для зп !!!Добавить онлайн/офлайн
    lesson = data['lesson']
    date = datetime.date.today()
    day = date.day
    month = date.month
    if data['done']:
        return (f'{"0" + str(day) if day < 10 else str(day)}.'
                                     f'{"0" + str(month) if month < 10 else str(month)}.'
                                     f'{str(date.year)}\n'
                                     f'Группа: {lesson["Группа"]}\n'
                                     f'Школа: {lesson["Школа"]}\n'
                                     f'Количество детей: {data["count"]}\n'
                                     f'Стоимость занятия: '
                                     f'{(350 + 100 * data["count"] if data["count"] > 3 else 700) if lesson["Школа"] != "Эврика" else 900}\n'
                                     f'Отработка: {200 if data["extras"] else 0}\n'
                                     f'#зарплата')
    else:

        return (f'{"0" + str(day) if day < 10 else str(day)}.'
                                     f'{"0" + str(month) if month < 10 else str(month)}.'
                                     f'{str(date.year)}\n'
                                     f'Группа: {lesson["Группа"]}\n'
                                     f'Школа: {lesson["Школа"]}\n'
                                     f'Причина: {data["message"]}\n'
                                     f'#зарплата')


def save_lesson_excel(data):
    if 'lesson' in data:
        lesson = data['lesson']
        school = lesson["Школа"]
        group = lesson["Группа"]
    else:
        school = data["school"]
        group = data["group"]
        data['done'] = True
        data["extras"] = False
    try:
        wb = openpyxl.load_workbook(config.SAVE_fILENAME)
        sheet = wb.active
        now = datetime.datetime.now().time()
        sheet.append([
            school,
            now,
            group,
            350 if data['done'] else 0,
            100,
            data["count"] if data['done'] else 0,
            200 if data["extras"] else 0,
            (350 if data['done'] else 0) + (100 * data["count"] if data['done'] else 0) + (200 if data["extras"] else 0),
            data["message"] if 'message' in data else ''
        ])
        wb.save(config.SAVE_fILENAME)
    except:
        print('Файл не найден')

def save_extras_excel(data):

    if 'lesson' in data:
        lesson = data['lesson']
        school = lesson["Школа"]
        group = lesson["Группа"]
    else:
        school = data["school"]
        data['done'] = True
    try:
        wb = openpyxl.load_workbook(config.SAVE_fILENAME)
        sheet = wb.active
        now = datetime.datetime.now().time()
        sheet.append([
            school,
            now,
            "Отработка " + data['pupil'],
            0,
            0,
            0,
            200 * data['time'] / 30,
            200 * data['time'] / 30
        ])
        wb.save(config.SAVE_fILENAME)
    except:
        print('Файл не найден')


