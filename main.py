import handlers
import asyncio #для асинхронного запуска бота
import logging # для настройки логгирования, которое поможет в отладке
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode #содержит настройки разметки сообщений (HTML, Markdown)
from aiogram.fsm.storage.memory import MemoryStorage #хранилища данных для состояний пользователей
from aiogram.fsm.context import FSMContext
import config #настройки бота, пока что только токен
import utils
from handlers import router #функционал нашего бота
from states import Current_lesson
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.context import FSMContext
scheduler = AsyncIOScheduler()



def shedule_jobs():
    shedule_lessons = utils.readDatabaseSheduel(config.FILENAME)
    for lesson in shedule_lessons:
        time = lesson['Время окончания']
        weekday = config.WEEKDAYS[str(lesson['Дата'])]
        scheduler.add_job(handlers.start_shedule, 'cron', day_of_week=weekday, hour=time.hour, minute=time.minute, args=(lesson, bot))
async def main():
    global bot
    bot = Bot(token=config.TOKEN)
    #parse_mode отвечает за используемую по умолчанию разметку сообщений. Мы используем HTML, чтобы избежать проблем с экранированием символов.
    dp = Dispatcher(storage=MemoryStorage())
    #создаём объект диспетчера, параметр storage=MemoryStorage() говорит о том, что все данные бота, которые мы не сохраняем в БД (к примеру состояния), будут стёрты при перезапуске.
    dp.include_router(router)
    #подключает к нашему диспетчеру все обработчики, которые используют router, их вы увидите в следующем файле.
    await bot.delete_webhook(drop_pending_updates=True)
    #удаляет все обновления, которые произошли после последнего завершения работы бота.
    # Это нужно, чтобы бот обрабатывал только те сообщения, которые пришли ему непосредственно во время его работы, а не за всё время. следующая строка запускает бота.
    scheduler.start()
    shedule_jobs()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
