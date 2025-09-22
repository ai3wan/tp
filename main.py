import asyncio
import logging
import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, DATABASE_URL
from handlers import common, onboarding, menu, course_flow, assessment_flow, profile
from handlers.assessments import anxiety_test

# Middleware для передачи пула в хендлеры
class DBMiddleware:
    def __init__(self, pool):
        self.pool = pool

    async def __call__(self, handler, event, data):
        data['pool'] = self.pool
        return await handler(event, data)

async def main():
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)

    # Создаем пул соединений с базой данных
    pool = await asyncpg.create_pool(DATABASE_URL)

    # Инициализация бота
    bot = Bot(token=BOT_TOKEN)
    
    # Используем хранилище в памяти для состояний FSM
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрируем middleware для базы данных
    dp.update.middleware()(DBMiddleware(pool))

    # Подключаем роутеры из наших файлов
    dp.include_router(common.router)
    dp.include_router(onboarding.router)
    dp.include_router(menu.router)
    dp.include_router(assessment_flow.router)
    dp.include_router(course_flow.router)
    dp.include_router(profile.router)
    
    dp.include_router(anxiety_test.router)
    
    try:
        # Пропускаем старые апдейты и запускаем polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        # Корректно закрываем пул соединений
        await pool.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")