import asyncpg
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

import database as db
import keyboards.inline as ikb
import keyboards.reply as rkb
from FSM.states import Onboarding, CourseSelection
from handlers.course_flow import show_main_menu

router = Router()

@router.message(Onboarding.final, F.text.in_({"🙌 Да, хочу выбрать курс", "🤔 Хочу посмотреть, что есть"}))
async def show_courses_list_onboarding(message: Message, state: FSMContext, pool: asyncpg.Pool):
    await state.clear()
    courses = await db.get_all_courses(pool)
    await message.answer(
        "Отлично! Вот наши курсы. Выбери тот, что откликается тебе больше всего.",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer("Выбери курс:", reply_markup=ikb.get_courses_kb(courses))

@router.callback_query(F.data.startswith("select_course_"))
async def course_selected_preview(callback: CallbackQuery, state: FSMContext, pool: asyncpg.Pool):
    course_id = int(callback.data.split("_")[2])
    
    course = await db.get_course_by_id(pool, course_id)
    if not course:
        await callback.answer("Курс не найден.", show_alert=True)
        return

    await state.set_state(CourseSelection.confirming_choice)
    await state.update_data(course_id=course_id)

    await callback.message.answer(
        f"**{course['emoji']} {course['title']}**\n\n{course['description']}",
        parse_mode="Markdown",
        reply_markup=rkb.course_confirmation_kb
    )
    await callback.answer()
    await callback.message.delete()

@router.message(CourseSelection.confirming_choice, F.text == "✅ Отлично, мне подходит")
async def confirm_course_selection(message: Message, state: FSMContext, pool: asyncpg.Pool):
    data = await state.get_data()
    course_id = data.get('course_id')
    user_id = message.from_user.id
    
    latest_progress = await db.get_latest_progress_for_course(pool, user_id, course_id)
    next_day, next_module = 1, 1
    if latest_progress:
        last_day, last_module = latest_progress['day'], latest_progress['module']
        next_day, next_module = last_day, last_module + 1
        if next_module > 3:
            next_module = 1
            next_day += 1

    await db.update_user_bookmark(pool, user_id, course_id, next_day, next_module)
    await state.clear()
    
    await show_main_menu(message, user_id, pool)

@router.message(CourseSelection.confirming_choice, F.text == "↩️ Вернуться к выбору курса")
async def back_to_course_list(message: Message, state: FSMContext, pool: asyncpg.Pool):
    await state.clear()
    courses = await db.get_all_courses(pool)
    await message.answer("Хорошо, вот снова список всех курсов:", reply_markup=ikb.get_courses_kb(courses))
    await message.answer("Выберите другой курс:", reply_markup=ReplyKeyboardRemove())

@router.message(CourseSelection.confirming_choice, F.text == "🤔 Узнать подробнее")
async def learn_more_stub(message: Message):
    await message.answer("Этот диалог находится в разработке 🚧")

@router.message(F.text == "Выбрать курс")
async def change_course(message: Message, pool: asyncpg.Pool):
    courses = await db.get_all_courses(pool)
    await message.answer("Какой курс вы хотите продолжить или начать?", reply_markup=ikb.get_courses_kb(courses))

@router.message(F.text == "Выбрать модуль")
async def select_module_entry(message: Message, pool: asyncpg.Pool):
    user_id = message.from_user.id
    bookmark = await db.get_user_bookmark(pool, user_id)
    if not bookmark or not bookmark['current_course_id']:
        await message.answer("Сначала выберите курс, чтобы просматривать модули.")
        return
    progress = await db.get_all_completed_modules_for_course(pool, user_id, bookmark['current_course_id'])
    days_kb = ikb.get_days_keyboard(bookmark['current_day'], progress)
    await message.answer("Выберите день для просмотра модулей:", reply_markup=days_kb)

@router.callback_query(F.data.startswith("select_day_"))
async def day_selected(callback: CallbackQuery, pool: asyncpg.Pool):
    selected_day = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    
    bookmark = await db.get_user_bookmark(pool, user_id)
    progress = await db.get_all_completed_modules_for_course(pool, user_id, bookmark['current_course_id'])

    modules_kb = ikb.get_modules_keyboard(selected_day, bookmark, progress)
    await callback.message.edit_text(f"Выбран день {selected_day}. Выберите модуль:", reply_markup=modules_kb)
    await callback.answer()
    
@router.callback_query(F.data.startswith("select_module_"))
async def module_selected(callback: CallbackQuery, pool: asyncpg.Pool):
    parts = callback.data.split("_")
    day, module = int(parts[2]), int(parts[3])
    user_id = callback.from_user.id
    
    bookmark = await db.get_user_bookmark(pool, user_id)
    course_id = bookmark['current_course_id']
    
    await db.update_user_bookmark(pool, user_id, course_id, day, module)

    await callback.message.delete()
    await callback.answer(f"Перехожу к модулю {day}.{module}...")
    
    course_info = await db.get_course_by_id(pool, course_id)
    await callback.message.answer(
        f"📖 Курс «{course_info['emoji']} {course_info['title']}»\n"
        f"**День {day}, Модуль {module}**\n\n"
        f"Здесь будет текст вашего модуля...",
        parse_mode="Markdown",
        reply_markup=rkb.module_navigation_kb
    )

@router.callback_query(F.data.in_({"day_locked", "module_locked"}))
async def locked_button_pressed(callback: CallbackQuery):
    await callback.answer("Этот раздел еще недоступен. Пройдите предыдущие уроки.", show_alert=True)

@router.message(F.text.in_({"Практики"}))
async def menu_stubs(message: Message):
    await message.answer("Этот раздел находится в разработке 🚧")