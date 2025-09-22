import asyncpg
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

import database as db
import keyboards.reply as rkb
import keyboards.inline as ikb
from FSM.states import ResetProgress
from handlers.course_flow import show_main_menu

router = Router()

def create_progress_bar(completed: int, total: int) -> str:
    """Создает текстовый прогресс-бар. Пример: [🟩🟩🟩⬜️⬜️⬜️⬜️⬜️⬜️⬜️]"""
    progress_percent = int((completed / total) * 10)
    return "🟩" * progress_percent + "⬜️" * (10 - progress_percent)

@router.message(F.text == "Профиль")
async def show_profile(message: Message, pool: asyncpg.Pool):
    user_id = message.from_user.id
    
    start_date = await db.get_user_start_date(pool, user_id)
    all_courses_progress = await db.get_all_courses_progress(pool, user_id)
    
    completed_courses_count = 0
    total_modules_count = 0
    active_courses_text = []
    completed_courses_list = []

    for course in all_courses_progress:
        total_modules_count += course['modules_completed']
        if course['modules_completed'] >= 42:
            completed_courses_count += 1
            completed_courses_list.append(course)
        elif course['modules_completed'] > 0:
            progress_bar = create_progress_bar(course['modules_completed'], 42)
            active_courses_text.append(
                f"Курс: «{course['emoji']} {course['title']}»\n"
                f"Прогресс: {course['modules_completed']}/42 модулей\n[{progress_bar}]"
            )
            
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

@router.message(F.text == "📖 Завершенные курсы")
async def show_completed_courses(message: Message, pool: asyncpg.Pool):
    all_progress = await db.get_all_courses_progress(pool, message.from_user.id)
    completed_courses = [c for c in all_progress if c['modules_completed'] >= 42]

    if not completed_courses:
        await message.answer("У вас пока нет завершённых курсов.")
        return

    await message.answer(
        "Вот ваши завершенные курсы. Выберите, чтобы посмотреть итоги:",
        reply_markup=ikb.get_courses_kb(completed_courses)
    )

@router.callback_query(F.data.startswith("select_course_"))
async def view_completed_result(callback: CallbackQuery, pool: asyncpg.Pool):
    course_id = int(callback.data.split("_")[2])
    course = await db.get_course_by_id(pool, course_id)
    await callback.message.answer(f"Итоги по курсу «{course['title']}» будут здесь.")
    await callback.answer()

@router.message(F.text == "🗑️ Сбросить прогресс")
async def reset_progress_start(message: Message, pool: asyncpg.Pool):
    all_progress = await db.get_all_courses_progress(pool, message.from_user.id)
    courses_with_progress = [c for c in all_progress if c['modules_completed'] > 0]

    if not courses_with_progress:
        await message.answer("У вас нет курсов, по которым можно сбросить прогресс.")
        return

    await message.answer(
        "Прогресс по какому курсу вы хотите сбросить? Внимание: это действие необратимо.",
        reply_markup=ikb.get_reset_courses_kb(courses_with_progress)
    )

@router.callback_query(F.data.startswith("reset_course_"))
async def reset_progress_confirm(callback: CallbackQuery, state: FSMContext, pool: asyncpg.Pool):
    course_id = int(callback.data.split("_")[2])
    course = await db.get_course_by_id(pool, course_id)
    
    await state.set_state(ResetProgress.confirming_reset)
    await state.update_data(course_to_reset=course_id)
    
    await callback.message.edit_text(
        f"Вы уверены, что хотите сбросить прогресс по курсу «{course['title']}»? Все ваши достижения по нему будут удалены.",
        reply_markup=ikb.get_confirm_reset_kb()
    )

@router.callback_query(ResetProgress.confirming_reset, F.data == "confirm_reset")
async def reset_progress_execute(callback: CallbackQuery, state: FSMContext, pool: asyncpg.Pool):
    data = await state.get_data()
    course_id = data.get('course_to_reset')
    
    await db.reset_progress_for_course(pool, callback.from_user.id, course_id)
    
    await state.clear()
    await callback.message.edit_text("✅ Прогресс по курсу успешно сброшен.")

@router.callback_query(ResetProgress.confirming_reset, F.data == "cancel_reset")
async def reset_progress_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Сброс отменён.")

@router.message(F.text == "↩️ Вернуться в меню")
async def back_to_main_menu_from_profile(message: Message, pool: asyncpg.Pool):
    await message.answer("Возвращаю...", reply_markup=ReplyKeyboardRemove())
    await show_main_menu(message, message.from_user.id, pool)