import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import common, onboarding, menu, course_flow, assessment_flow, profile
from handlers.assessments import anxiety_test
from handlers.modules import day_1_module_1, day_1_module_2

async def main():
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)

    # Инициализация бота
    bot = Bot(token=BOT_TOKEN)
    
    # Используем хранилище в памяти для состояний FSM
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Подключаем роутеры из наших файлов
    dp.include_router(common.router)
    dp.include_router(onboarding.router)
    dp.include_router(menu.router)
    dp.include_router(assessment_flow.router)
    dp.include_router(course_flow.router)
    dp.include_router(profile.router)
    
    # Подключаем роутеры модулей
    dp.include_router(day_1_module_1.router)
    dp.include_router(day_1_module_2.router)
    
    dp.include_router(anxiety_test.router)
    

    # Пропускаем старые апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")