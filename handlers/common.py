# handlers/common.py

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
async def start_handler(message: Message, state: FSMContext):
    # Добавляем пользователя (если его нет) и получаем его ID
    user_db_id = await db.add_user(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        username=message.from_user.username
    )
    
    # --- УПРОЩЕННАЯ ЛОГИКА ---
    # Проверяем, есть ли у пользователя активный курс
    bookmark = await db.get_user_bookmark(message.from_user.id)
    
    # Если курса нет, устанавливаем курс тревожности (ID = 1) и начинаем онбординг
    if not bookmark or not bookmark['current_course_id']:
        await state.set_state(Onboarding.q1_thoughts)
        # Отправляем видео с текстом
        import os
        from aiogram.types import FSInputFile
        
        video_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "welcome.mp4")
        video_file = FSInputFile(video_path)
        
        await message.answer_video(
            video=video_file,
            caption="👋 **Привет!**\n\n"
                    "Тихие практики — это пространство, где мы помогаем заботиться о своём эмоциональном здоровье и ментальном комфорте.\n\n"
                    "📚 **Здесь нет скучных лекций.**\n"
                    "Вместе с профессиональными психологами мы создали:\n\n"
                    "• **Чёткую и ёмкую теорию** — только то, что действительно работает\n"
                    "• **Интерактивные форматы**, которые вовлекают, а не усыпляют\n"
                    "• **Научно обоснованные практики** для реальных ситуаций современной жизни\n\n"
                    "💡 **Каждая практика** — это конкретный шаг к спокойствию, фокусу и внутренней опоре.\n\n"
                    "✨ **Давай познакомимся ближе?**\n"
                    "Ответь на пару вопросов, чтобы начать.",
            reply_markup=kb.onboarding_start_kb
        )
    else:
        # Если курс уже есть, показываем главное меню
        await show_main_menu(message, message.from_user.id)

# Этот хендлер сработает на любой из двух первых кнопок
@router.message(F.text.in_({"🚀 Давай попробуем", "🙂 Поехали"}))
async def start_onboarding_q1(message: Message, state: FSMContext):
    await state.set_state(Onboarding.q1_thoughts)
    await message.answer(
        "Бывает, что мысли начинают кружиться, и сложно их остановить?",
        reply_markup=kb.onboarding_q1_kb
    )