# handlers/profile.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

import database as db
import keyboards.reply as rkb
import keyboards.inline as ikb
from FSM.states import ResetProgress
from handlers.course_flow import show_main_menu

router = Router()

# --- Вспомогательная функция для создания прогресс-бара ---
def create_progress_bar(completed: int, total: int) -> str:
    """Создает текстовый прогресс-бар. Пример: [🟩🟩🟩⬜️⬜️⬜️⬜️⬜️⬜️⬜️]"""
    progress_percent = int((completed / total) * 10)
    return "🟩" * progress_percent + "⬜️" * (10 - progress_percent)

# --- Вспомогательная функция для получения результатов всех пульсов тревожности ---
async def get_all_assessments_display(user_id: int, course_id: int) -> list:
    """Возвращает список строк с результатами всех пульсов тревожности."""
    import asyncpg
    conn = await asyncpg.connect(db.DATABASE_URL)
    try:
        db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
        if not db_user_id:
            return ["🔘 Пульс тревожности не пройден"]
            
        sql = """
            SELECT assessment_type, score, self_assessment_score FROM assessment_results
            WHERE user_id = $1 AND course_id = $2
            ORDER BY assessment_type;
        """
        results = await conn.fetch(sql, db_user_id, course_id)
        
        if not results:
            return ["🔘 Пульс тревожности не пройден"]
        
        assessments = []
        for result in results:
            assessment_type = result['assessment_type']
            score = result['score']
            self_assessment = result['self_assessment_score']
            
            # Определяем цвет индикатора по уровню тревожности
            if 0 <= score <= 13:
                indicator = "🟢"  # Низкий уровень
            elif 14 <= score <= 26:
                indicator = "🟡"  # Средний уровень
            else:
                indicator = "🔴"  # Высокий уровень
            
            # Определяем название теста
            if assessment_type == 'initial':
                test_name = "Пульс тревожности до курса"
            elif assessment_type == 'intermediate':
                test_name = "Промежуточный пульс тревожности"
            elif assessment_type == 'final':
                test_name = "Пульс тревожности после курса"
            else:
                test_name = f"Пульс тревожности ({assessment_type})"
            
            assessments.append(f"{indicator} {test_name}: {score}/42 баллов (самооценка: {self_assessment}/10)")
        
        return assessments
        
    finally:
        await conn.close()


# --- Основной обработчик кнопки "Профиль" ---
@router.message(F.text == "🙍 Профиль")
async def show_profile(message: Message):
    user_id = message.from_user.id
    
    # 1. Получаем все данные из БД
    start_date = await db.get_user_start_date(user_id)
    all_courses_progress = await db.get_all_courses_progress(user_id)
    
    # 2. Получаем результаты всех пульсов тревожности
    assessments_display = await get_all_assessments_display(user_id, 1)  # Курс тревожности (ID = 1)
    
    # 3. Считаем статистику и готовим списки
    total_modules_count = 0
    active_courses_text = []
    completed_courses_list = []

    for course in all_courses_progress:
        total_modules_count += course['modules_completed']
        # Курс завершен, если пройдено 42 модуля (14 дней * 3 модуля)
        if course['modules_completed'] >= 42:
            completed_courses_list.append(course)
        # Если есть прогресс, но курс не завершен - он активный
        elif course['modules_completed'] > 0:
            progress_bar = create_progress_bar(course['modules_completed'], 42)
            active_courses_text.append(
                f"Прогресс: {course['modules_completed']}/42 модулей\n[{progress_bar}]"
            )
            
    # 4. Формируем итоговое сообщение
    profile_text = [
        f"👤 Ваш Профиль\n",
        f"Вы с нами с: {start_date}\n",
        "---",
        "📊 Ваша статистика:",
        f"• Всего завершено модулей: {total_modules_count}\n",
        "---"
    ]

    # Добавляем результаты пульсов тревожности
    if assessments_display:
        profile_text.append("💓 Пульс тревожности:")
        for assessment in assessments_display:
            profile_text.append(f"• {assessment}")
        profile_text.append("\n---")

    # Добавляем прогресс курса
    if active_courses_text:
        profile_text.extend(active_courses_text)

    await message.answer("\n".join(profile_text), reply_markup=rkb.profile_kb)


# --- Обработчики кнопок меню профиля ---

# --- Логика сброса прогресса ---

@router.message(F.text == "🗑️ Сбросить прогресс")
async def reset_progress_start(message: Message):
    """Предлагает сбросить прогресс по курсу тревожности."""
    all_progress = await db.get_all_courses_progress(message.from_user.id)
    courses_with_progress = [c for c in all_progress if c['modules_completed'] > 0]

    if not courses_with_progress:
        await message.answer("У вас нет прогресса по курсу, который можно сбросить.")
        return

    # Поскольку у нас только курс тревожности, сразу предлагаем сброс
    course = courses_with_progress[0]
    await message.answer(
        f"Вы хотите сбросить весь прогресс по курсу «{course['emoji']} {course['title']}»?\n\n"
        f"Текущий прогресс: {course['modules_completed']}/42 модулей\n\n"
        "⚠️ Внимание: это действие необратимо. Все ваши достижения будут удалены.",
        reply_markup=ikb.get_confirm_reset_kb()
    )

@router.callback_query(F.data == "confirm_reset")
async def reset_progress_execute(callback: CallbackQuery, state: FSMContext):
    """Выполняет сброс прогресса по курсу тревожности."""
    # Устанавливаем курс тревожности (ID = 1) для сброса
    await db.reset_progress_for_course(callback.from_user.id, 1)
    
    await state.clear()
    await callback.message.edit_text("✅ Прогресс по курсу успешно сброшен. Вы можете начать заново!")

@router.callback_query(F.data == "cancel_reset")
async def reset_progress_cancel(callback: CallbackQuery, state: FSMContext):
    """Отменяет сброс прогресса."""
    await state.clear()
    await callback.message.edit_text("Сброс отменён. Ваш прогресс сохранён.")

# --- Вернуться в меню ---
@router.message(F.text == "↩️ Вернуться в меню")
async def back_to_main_menu_from_profile(message: Message):
    await message.answer("Возвращаю...", reply_markup=ReplyKeyboardRemove())
    await show_main_menu(message, message.from_user.id)