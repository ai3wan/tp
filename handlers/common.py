# handlers/common.py

import asyncpg
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import database as db
import keyboards.reply as kb
from FSM.states import Onboarding
# Импортируем нашу функцию для показа меню
from handlers.course_flow import show_main_menu 

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext, pool: asyncpg.Pool):
    await db.add_user(
        pool=pool,
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        username=message.from_user.username
    )
    
    bookmark = await db.get_user_bookmark(pool, message.from_user.id)
    
    # Проверяем, что и закладка, и ID курса в ней существуют
    if bookmark and bookmark['current_course_id']:
        # Если курс уже есть, показываем главное меню
        await show_main_menu(message, message.from_user.id, pool)
    else:
        # Если курса нет, начинаем онбординг
        await state.set_state(Onboarding.q1_thoughts) # Сразу переходим к первому вопросу
        await message.answer(
            "👋 Привет! Тихие практики — это пространство, где мы помогаем заботиться о своём эмоциональном здоровье и ментальном комфорте.\n"
            "📚 Здесь нет скучных лекций. Вместе с профессиональными психологами мы создали:\n"
            "• Чёткую и ёмкую теорию — только то, что действительно работает\n"
            "• Интерактивные форматы, которые вовлекают, а не усыпляют\n"
            "• Научно обоснованные практики для реальных ситуаций современной жизни\n"
            "💡 Каждая практика — это конкретный шаг к спокойствию, фокусу и внутренней опоре.\n"
            "✨ Давай познакомимся ближе?\nОтветь на пару вопросов, чтобы начать.",
            reply_markup=kb.onboarding_start_kb
        )

# Этот хендлер сработает на любой из двух первых кнопок
@router.message(F.text.in_({"🚀 Давай попробуем", "🙂 Поехали"}))
async def start_onboarding_q1(message: Message, state: FSMContext):
    await state.set_state(Onboarding.q1_thoughts)
    await message.answer(
        "Бывает, что мысли начинают кружиться, и сложно их остановить?",
        reply_markup=kb.onboarding_q1_kb
    )