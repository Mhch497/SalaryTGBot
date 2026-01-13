import datetime
import os

import requests
from dotenv import load_dotenv

from config import lessons_type, room_id, subjects_id
from transformer import Transformer

load_dotenv()
URL = 'https://algoritmikakirrn.s20.online/'


def auth():
    """Получение токена."""

    body = {"email": os.getenv('email'),
            "api_key": os.getenv('api_key')}
    response = requests.post(URL + 'v2api/auth/login', json=body)
    response = response.json()
    os.environ["X_ALFACRM_TOKEN"] = response['token']


def get_headers():
    """Формирование заголовков."""

    return {
            'X-ALFACRM-TOKEN': os.getenv("X_ALFACRM_TOKEN"),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }


def get_subjects():
    """Получение предметов и создание словаря id - название."""

    if os.getenv("X_ALFACRM_TOKEN") is not None:
        headers = get_headers()
        response = requests.post(URL + 'v2api/1/subject/index',
                                 headers=headers)
        response = response.json()
        global subjects_id
        subjects_id = dict()
        for item in response['items']:
            subjects_id[item['id']] = item['name']
    else:
        auth()
        get_subjects()



def get_group_lessons():
    """Получение текущих недельных занятий."""

    item2dict = Transformer((
        ('lesson_type_id', 'Тип урока', Transformer.lookup(lessons_type)),
        ('room_id', 'Школа', Transformer.lookup(room_id)),
        ('date', 'Дата', Transformer.strpdate),
        ('date', 'День недели', Transformer.strpweekday),
        ('subject_id', 'Группа', Transformer.lookup(subjects_id)),
        ('time_from', 'Время начала', Transformer.strptime),
        ('time_to', 'Время окончания', Transformer.strptime)
    ))

    today_lessons = []
    if os.getenv("X_ALFACRM_TOKEN") is not None:
        headers = get_headers()
        today = datetime.date.today().strftime('%Y-%m-%d')
        body = {"status": 1,
                "teacher_id": 4,
                "date_from": today,
                "date_to": today
                }
        response = requests.post(URL + 'v2api/1/lesson/index',
                                 headers=headers, json=body)
        if response.ok:
            response = response.json()
            for item in response['items']:
                dict_lesson = item2dict.transform(item)
                # TODO introduce LessonTypeEnum and use instead [2, 3, 5] here.
                if item['lesson_type_id'] not in [2, 3, 5]:
                    dict_lesson['Ученики'] = [get_pupil(pupil)
                                              for pupil in item['customer_ids']
                                              ]
                shedule = get_shedule()
                is_match = False
                # TODO introduce LessonTypeEnum and use instead [2, 5] here.
                if item['lesson_type_id'] in [2, 5]:
                    for elem in shedule:
                        if (dict_lesson['Тип урока'] == elem['Тип урока']
                            and dict_lesson['Школа'] == elem['Школа']
                            and dict_lesson['День недели'] == (elem['День недели'])
                            and dict_lesson['Группа'] == elem['Группа']
                            and dict_lesson['Время начала'].strftime('%H:%M') == elem['Время начала']):
                            is_match = True
                    if not is_match:
                        dict_lesson['Тип урока'] += ' (Замена преподавателя)'
                today_lessons.append(dict_lesson)
            return today_lessons
    auth()
    get_group_lessons()


def get_pupil(id):
    """Получение ученика по id."""

    if os.getenv("X_ALFACRM_TOKEN") is not None:
        headers = get_headers()
        body = {
            "is_study": 1,
            "id": id
        }
        response = requests.post(URL + 'v2api/1/customer/index',
                                 headers=headers, json=body)
        if response.ok:
            response = response.json()
            try:
                return response['items'][0]['name']
            except IndexError:
                body = {
                    "is_study": 0,
                    "id": id
                }
                response = requests.post(URL + 'v2api/1/customer/index',
                                         headers=headers, json=body)
                if response.ok:
                    response = response.json()
                    return response['items'][0]['name']
    auth()
    get_pupil()


def get_shedule():
    """Получение расписания."""

    shedule = []
    if os.getenv("X_ALFACRM_TOKEN") is not None:
        headers = get_headers()
        body = {
                "teacher_id": 4
                }
        response = requests.post(URL + 'v2api/1/regular-lesson/index',
                                 headers=headers, json=body)
        if response.ok:
            item2lesson = Transformer((
                ('lesson_type_id', 'Тип урока', Transformer.lookup(lessons_type)),
                ('room_id', 'Школа', Transformer.lookup(room_id)),
                ('day', 'День недели', Transformer.identity),
                ('subject_id', 'Группа', Transformer.lookup(subjects_id)),
                ('time_from_v', 'Время начала', Transformer.identity),
            ))
            response = response.json()
            return [item2lesson.transform(item) for item in response['items']]
    auth()
    get_shedule()


if __name__ == "__main__":
    auth()
    get_group_lessons()
