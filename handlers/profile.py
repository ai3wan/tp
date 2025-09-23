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


# --- Основной обработчик кнопки "Профиль" ---
@router.message(F.text == "Профиль")
async def show_profile(message: Message):
    user_id = message.from_user.id
    
    # 1. Получаем все данные из БД
    start_date = await db.get_user_start_date(user_id)
    all_courses_progress = await db.get_all_courses_progress(user_id)
    
    # 2. Считаем статистику и готовим списки
    completed_courses_count = 0
    total_modules_count = 0
    active_courses_text = []
    completed_courses_list = []

    for course in all_courses_progress:
        total_modules_count += course['modules_completed']
        # Курс завершен, если пройдено 42 модуля (14 дней * 3 модуля)
        if course['modules_completed'] >= 42:
            completed_courses_count += 1
            completed_courses_list.append(course)
        # Если есть прогресс, но курс не завершен - он активный
        elif course['modules_completed'] > 0:
            progress_bar = create_progress_bar(course['modules_completed'], 42)
            active_courses_text.append(
                f"Курс: «{course['emoji']} {course['title']}»\n"
                f"Прогресс: {course['modules_completed']}/42 модулей\n[{progress_bar}]"
            )
            
    # 3. Формируем итоговое сообщение
    profile_text = [
        f"👤 Ваш Профиль\n",
        f"Вы с нами с: {start_date}\n",
        "---",
        "📊 Ваша общая статистика:",
        f"• Пройдено курсов: {completed_courses_count}",
        f"• Всего завершено модулей: {total_modules_count}\n",
        "---"
    ]

    if active_courses_text:
        profile_text.append("🎯 Ваши активные курсы:\n")
        profile_text.extend(active_courses_text)
        profile_text.append("\n---")

    if completed_courses_list:
        profile_text.append("🏆 Ваши ачивки (завершённые курсы):")
        for course in completed_courses_list:
            profile_text.append(f"✅ {course['title']}")
    else:
        profile_text.append("🏆 У вас пока нет завершённых курсов.")

    await message.answer("\n".join(profile_text), reply_markup=rkb.profile_kb)


# --- Обработчики кнопок меню профиля ---

@router.message(F.text == "📖 Завершенные курсы")
async def show_completed_courses(message: Message):
    """Показывает информацию о завершенном курсе тревожности."""
    all_progress = await db.get_all_courses_progress(message.from_user.id)
    completed_courses = [c for c in all_progress if c['modules_completed'] >= 42]

    if not completed_courses:
        await message.answer("У вас пока нет завершённых курсов. Продолжайте заниматься!")
        return

    # Поскольку у нас только курс тревожности, показываем его результат
    course = completed_courses[0]  # Берем первый (и единственный) завершенный курс
    await message.answer(
        f"🎉 Поздравляем! Вы завершили курс «{course['emoji']} {course['title']}»!\n\n"
        f"Пройдено модулей: {course['modules_completed']}/42\n\n"
        "Это отличное достижение! Вы освоили множество техник для работы с тревожностью."
    )

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