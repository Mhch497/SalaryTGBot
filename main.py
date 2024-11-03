import asyncio  # для асинхронного запуска бота
import logging  # для настройки логгирования, которое поможет в отладке
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import API
# хранилища данных для состояний пользователей
import config  # настройки бота, пока что только токен
import handlers
from handlers import router  # функционал нашего бота

# TODO добавить возможность просмотра занятий за определенный день
# TODO напомнить Маше про отработки каждый день (а не по факту) и индивиды
scheduler = AsyncIOScheduler()


def shedule_jobs():
    """Формирование расписания сообщений в боте."""

    shedule_lessons = API.get_group_lessons()
    # FIXME убрать, когда закончится тестирование
    # shedule_lessons = [{'Время начала': datetime.time(14, 20, 1),
    #                     'Время окончания': datetime.time(17, 5),
    #                     'Группа': 'PS 2 Год',
    #                     'Дата': datetime.date(2024, 10, 9),
    #                     'День недели': 3,
    #                     'Тип урока': 'Онлайн (Замена преподавателя)',
    #                     'Школа': 'Онлайн'},
    #                     {'Время начала': datetime.time(14, 0, 1),
    #                     'Время окончания': datetime.time(17, 6),
    #                     'Группа': 'PS 2 Год',
    #                     'Дата': datetime.date(2024, 10, 9),
    #                     'День недели': 3,
    #                     'Тип урока': 'Групповой урок',
    #                     'Школа': 'Уральская'},
    #                     {'Время начала': datetime.time(14, 0, 1),
    #                     'Время окончания': datetime.time(17, 23),
    #                     'Группа': 'PS 2 Год',
    #                     'Дата': datetime.date(2024, 10, 9),
    #                     'День недели': 3,
    #                     'Тип урока': 'Отработка',
    #                     'Ученики': ['Иваненко Мария'],
    #                     'Школа': 'ЖБИ'}]
    for lesson in shedule_lessons:
        time = lesson['Время окончания']
        weekday = config.WEEKDAYS[str(lesson['День недели'])]
        scheduler.add_job(
            handlers.start_shedule,
            'cron',
            day_of_week=weekday,
            hour=time.hour,
            minute=time.minute,
            args=(lesson, bot))


async def main():
    """Создание бота, запуск расписания и ожидания бота."""

    API.auth()
    global bot
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    scheduler.start()
    shedule_jobs()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
