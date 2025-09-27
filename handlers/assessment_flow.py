# handlers/assessment_flow.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import database as db

# Импортируем точки входа из наших файлов с тестами
from handlers.assessments.anxiety_test import start_anxiety_test
from handlers.assessments.final_test import start_final_test

router = Router()

@router.message(F.text == "Пройти начальную оценку")
async def start_initial_assessment_router(message: Message, state: FSMContext):
    """
    Запускает начальный пульс тревожности.
    """
    bookmark = await db.get_user_bookmark(message.from_user.id)
    if not bookmark or not bookmark['current_course_id']:
        # Устанавливаем курс тревожности (ID = 1) если его нет
        await db.update_user_bookmark(message.from_user.id, 1, 1, 1)
        
    # Запускаем пульс тревожности
    await start_anxiety_test(message, state)


@router.message(F.text == "Оценить прогресс")
async def start_final_assessment_router(message: Message, state: FSMContext):
    """
    Запускает финальный пульс тревожности.
    """
    bookmark = await db.get_user_bookmark(message.from_user.id)
    if not bookmark or not bookmark['current_course_id']:
        await message.answer("Пожалуйста, сначала завершите курс.")
        return

    # Запускаем финальный пульс тревожности
    await start_final_test(message, state)