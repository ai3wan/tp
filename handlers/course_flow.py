# handlers/course_flow.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

import database as db
import keyboards.reply as kb
import keyboards.inline as ikb # <-- ДОБАВЬТЕ ЭТУ СТРОКУ

router = Router()


# --- Вспомогательная функция для показа главного меню (УПРОЩЕННАЯ) ---
async def show_main_menu(message: Message, user_id: int):
    """Отправляет пользователю его актуальное главное меню для курса тревожности."""
    bookmark = await db.get_user_bookmark(user_id)
    
    # Если у пользователя нет активного курса, устанавливаем курс тревожности (ID = 1)
    if not bookmark or not bookmark['current_course_id']:
        await db.update_user_bookmark(user_id, 1, 1, 1)
        bookmark = await db.get_user_bookmark(user_id)
    
    course_id = bookmark['current_course_id']
    course_info = await db.get_course_by_id(course_id)
    
    # --- УПРОЩЕННАЯ ЛОГИКА ДЛЯ КУРСА ТРЕВОЖНОСТИ ---
    
    # 1. Проверяем, пройден ли курс полностью (42 модуля)
    progress = await db.get_all_completed_modules_for_course(user_id, course_id)
    if len(progress) >= 42:
        main_button_text = f"Курс «{course_info['emoji']} {course_info['title']}». Оценить прогресс"
    else:
        # 2. Если курс не пройден, проверяем, был ли начальный тест
        initial_assessment = await db.get_initial_assessment_result(user_id, course_id)
        if not initial_assessment:
            # 3. Если теста не было, предлагаем его пройти
            main_button_text = f"Курс «{course_info['emoji']} {course_info['title']}». Пройти начальную оценку"
        else:
            # 4. Если тест был, показываем текущий модуль из закладки
            main_button_text = f"Курс «{course_info['emoji']} {course_info['title']}». День {bookmark['current_day']}. Модуль {bookmark['current_module']}"

    # --- Конец упрощенной логики ---

    main_menu_kb = kb.ReplyKeyboardMarkup(
        keyboard=[
            [kb.KeyboardButton(text=main_button_text)],
            [kb.KeyboardButton(text="Выбрать модуль")],
            [kb.KeyboardButton(text="Практики"), kb.KeyboardButton(text="Профиль")]
        ],
        resize_keyboard=True
    )
    await message.answer("Ваше главное меню:", reply_markup=main_menu_kb)

# --- Основная логика прохождения ---

# 1. Нажатие на главную кнопку "Начать/Продолжить курс"
@router.message(F.text.startswith(("Начать «", "Курс «")))
async def start_module(message: Message):
    user_id = message.from_user.id
    bookmark = await db.get_user_bookmark(user_id)
    
    if bookmark['current_day'] > 14:
        await show_main_menu(message, user_id)
        return

    course_info = await db.get_course_by_id(bookmark['current_course_id'])

    await message.answer(
        f"📖 Курс «{course_info['emoji']} {course_info['title']}»\n"
        f"**День {bookmark['current_day']}, Модуль {bookmark['current_module']}**\n\n"
        f"Здесь будет текст вашего модуля...",
        parse_mode="Markdown",
        reply_markup=kb.module_navigation_kb
    )

# 2. Нажатие на "Давай повторим"
@router.message(F.text == "🔄 Давай повторим")
async def repeat_module(message: Message):
    await start_module(message)

# 3. Нажатие на "Все ясно"
@router.message(F.text == "✅ Все ясно")
async def complete_module(message: Message):
    user_id = message.from_user.id
    bookmark = await db.get_user_bookmark(user_id)

    # 1. Записываем прогресс
    await db.complete_module(
        user_id,
        bookmark['current_course_id'],
        bookmark['current_day'],
        bookmark['current_module']
    )
    
    # 2. СРАЗУ передвигаем закладку
    current_day = bookmark['current_day']
    current_module = bookmark['current_module']
    await db.advance_user_to_next_module(user_id, current_day, current_module)
    
    # 3. Проверяем, был ли это последний модуль дня
    if current_module == 3:
        await message.answer(
            "Мы отлично поработали! ✨\n"
            "Сегодняшние практики завершены. Завтра нас ждет следующий шаг."
        )
        # Если день закончен, сразу возвращаем в главное меню
        await show_main_menu(message, user_id)
    else:
        # Если это не последний модуль, показываем промежуточное меню
        await message.answer(
            "Отлично! Двигаемся дальше?",
            reply_markup=kb.after_module_kb
        )

# 4. Нажатие на "Двигаемся дальше"
@router.message(F.text == "▶️ Двигаемся дальше")
async def advance_to_next(message: Message):
    # Теперь эта кнопка просто запускает следующий модуль,
    # так как закладка уже передвинута.
    await start_module(message)

# 5. Нажатие на "В основное меню"
@router.message(F.text == "🏠 В основное меню")
async def back_to_main_menu(message: Message):
    # Эта кнопка также просто показывает главное меню.
    # Закладка уже обновлена, поэтому меню будет правильным.
    await message.answer("Возвращаю вас в главное меню.", reply_markup=ReplyKeyboardRemove())
    await show_main_menu(message, message.from_user.id)