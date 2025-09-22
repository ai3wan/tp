import asyncpg
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton

import database as db
import keyboards.reply as kb
import keyboards.inline as ikb

router = Router()


async def show_main_menu(message: Message, user_id: int, pool: asyncpg.Pool):
    """Отправляет пользователю его актуальное главное меню с умной кнопкой."""
    bookmark = await db.get_user_bookmark(pool, user_id)
    
    if not bookmark or not bookmark['current_course_id']:
        courses = await db.get_all_courses(pool)
        await message.answer(
            "У вас нет активного курса. Давайте выберем один!",
            reply_markup=ikb.get_courses_kb(courses)
        )
        await message.answer("Выберите курс из списка выше:", reply_markup=ReplyKeyboardRemove())
        return

    course_id = bookmark['current_course_id']
    course_info = await db.get_course_by_id(pool, course_id)
    
    progress = await db.get_all_completed_modules_for_course(pool, user_id, course_id)
    if len(progress) >= 42:
        main_button_text = f"Курс «{course_info['emoji']} {course_info['title']}». Оценить прогресс"
    else:
        initial_assessment = await db.get_initial_assessment_result(pool, user_id, course_id)
        if not initial_assessment:
            main_button_text = f"Курс «{course_info['emoji']} {course_info['title']}». Пройти начальную оценку"
        else:
            main_button_text = f"Курс «{course_info['emoji']} {course_info['title']}». День {bookmark['current_day']}. Модуль {bookmark['current_module']}"

    main_menu_kb = kb.ReplyKeyboardMarkup(
        keyboard=[
            [kb.KeyboardButton(text=main_button_text)],
            [kb.KeyboardButton(text="Выбрать курс"), kb.KeyboardButton(text="Выбрать модуль")],
            [kb.KeyboardButton(text="Практики"), kb.KeyboardButton(text="Профиль")]
        ],
        resize_keyboard=True
    )
    await message.answer("Ваше главное меню:", reply_markup=main_menu_kb)


@router.message(F.text.startswith(("Начать «", "Курс «")))
async def start_module(message: Message, pool: asyncpg.Pool):
    user_id = message.from_user.id
    bookmark = await db.get_user_bookmark(pool, user_id)
    
    if not bookmark or not bookmark['current_course_id']:
        await show_main_menu(message, user_id, pool)
        return

    if bookmark['current_day'] > 14:
        await show_main_menu(message, user_id, pool)
        return

    course_info = await db.get_course_by_id(pool, bookmark['current_course_id'])

    await message.answer(
        f"📖 Курс «{course_info['emoji']} {course_info['title']}»\n"
        f"**День {bookmark['current_day']}, Модуль {bookmark['current_module']}**\n\n"
        f"Здесь будет текст вашего модуля...",
        parse_mode="Markdown",
        reply_markup=kb.module_navigation_kb
    )

@router.message(F.text == "🔄 Давай повторим")
async def repeat_module(message: Message, pool: asyncpg.Pool):
    await start_module(message, pool)

@router.message(F.text == "✅ Все ясно")
async def complete_module(message: Message, pool: asyncpg.Pool):
    user_id = message.from_user.id
    bookmark = await db.get_user_bookmark(pool, user_id)

    if not bookmark or not bookmark['current_course_id']:
        await show_main_menu(message, user_id, pool)
        return

    await db.complete_module(
        pool,
        user_id,
        bookmark['current_course_id'],
        bookmark['current_day'],
        bookmark['current_module']
    )
    
    current_day = bookmark['current_day']
    current_module = bookmark['current_module']
    await db.advance_user_to_next_module(pool, user_id, current_day, current_module)
    
    if current_module == 3:
        await message.answer(
            "Мы отлично поработали! ✨\n"
            "Сегодняшние практики завершены. Завтра нас ждет следующий шаг."
        )
        await show_main_menu(message, user_id, pool)
    else:
        await message.answer(
            "Отлично! Двигаемся дальше?",
            reply_markup=kb.after_module_kb
        )

@router.message(F.text == "▶️ Двигаемся дальше")
async def advance_to_next(message: Message, pool: asyncpg.Pool):
    await start_module(message, pool)

@router.message(F.text == "🏠 В основное меню")
async def back_to_main_menu(message: Message, pool: asyncpg.Pool):
    await message.answer("Возвращаю вас в главное меню.", reply_markup=ReplyKeyboardRemove())
    await show_main_menu(message, message.from_user.id, pool)