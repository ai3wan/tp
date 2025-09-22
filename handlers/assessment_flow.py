# handlers/assessment_flow.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import database as db

# Импортируем обе "точки входа" из нашего файла с тестом
from handlers.assessments.anxiety_test import start_anxiety_test, start_anxiety_final_test

router = Router()

@router.message(F.text.endswith("Пройти начальную оценку"))
async def start_initial_assessment_router(message: Message, state: FSMContext):
    """
    Этот диспетчер определяет, какой курс у пользователя,
    и запускает соответствующий НАЧАЛЬНЫЙ тест.
    """
    bookmark = await db.get_user_bookmark(message.from_user.id)
    if not bookmark or not bookmark['current_course_id']:
        await message.answer("Пожалуйста, сначала выберите курс в главном меню.")
        return
        
    course_id = bookmark['current_course_id']

    if course_id == 1:
        await start_anxiety_test(message, state)
    else:
        await message.answer("Для этого курса пока нет входного тестирования.")


@router.message(F.text.endswith("Оценить прогресс"))
async def start_final_assessment_router(message: Message, state: FSMContext):
    """
    Этот диспетчер определяет, какой курс у пользователя,
    и запускает соответствующий ФИНАЛЬНЫЙ тест.
    """
    bookmark = await db.get_user_bookmark(message.from_user.id)
    if not bookmark or not bookmark['current_course_id']:
        await message.answer("Пожалуйста, сначала выберите курс в главном меню.")
        return

    course_id = bookmark['current_course_id']

    if course_id == 1:
        # Вызываем новую функцию для запуска финального теста
        await start_anxiety_final_test(message, state)
    else:
        # Заглушка для других курсов
        await message.answer("Для этого курса пока нет финального тестирования.")