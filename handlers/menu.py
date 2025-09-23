# handlers/menu.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

import database as db
import keyboards.inline as ikb
import keyboards.reply as rkb
from FSM.states import Onboarding
from handlers.course_flow import show_main_menu

router = Router()

# --- Логика онбординга (упрощенная) ---
@router.message(F.text == "✅ Да, давай пройдем тест")
async def start_test_from_onboarding(message: Message, state: FSMContext):
    """Пользователь согласился пройти тест после онбординга."""
    # Устанавливаем курс тревожности (ID = 1) как активный
    await db.update_user_bookmark(message.from_user.id, 1, 1, 1)
    
    # Запускаем тест тревожности
    from handlers.assessments.anxiety_test import start_anxiety_test
    await start_anxiety_test(message, state)

@router.message(F.text == "🤔 Сначала расскажи про курс")
async def show_course_info(message: Message):
    """Показываем информацию о курсе по тревожности."""
    await message.answer(
        "📚 **Курс «Работа с тревожностью»**\n\n"
        "Этот курс создан профессиональными психологами и включает:\n\n"
        "• **14 дней практик** — по 3 модуля в день\n"
        "• **Научно обоснованные техники** расслабления и контроля мыслей\n"
        "• **Персональный подход** — тест поможет подстроить курс под тебя\n"
        "• **Отслеживание прогресса** — увидишь, как меняется твое состояние\n\n"
        "Каждый модуль занимает 5-10 минут и содержит конкретные упражнения, которые можно применять в реальной жизни.\n\n"
        "Готов(а) начать?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="✅ Да, давай пройдем тест")],
            [KeyboardButton(text="🚀 Начать курс без теста")]
        ], resize_keyboard=True)
    )

@router.message(F.text == "🚀 Начать курс без теста")
async def start_course_without_test(message: Message):
    """Пользователь хочет начать курс без прохождения теста."""
    # Устанавливаем курс тревожности (ID = 1) как активный
    await db.update_user_bookmark(message.from_user.id, 1, 1, 1)
    
    # Показываем главное меню
    await show_main_menu(message, message.from_user.id)

# --- Старые обработчики меню (упрощенные) ---
@router.message(F.text == "📚 Выбрать модуль")
async def select_module_entry(message: Message):
    """Показывает календарь дней для выбора модуля курса тревожности."""
    user_id = message.from_user.id
    bookmark = await db.get_user_bookmark(user_id)
    
    # Устанавливаем курс тревожности, если его нет
    if not bookmark or not bookmark['current_course_id']:
        await db.update_user_bookmark(user_id, 1, 1, 1)
        bookmark = await db.get_user_bookmark(user_id)
    
    # ПРОВЕРКА: если пользователь не прошел начальный тест, блокируем доступ к модулям
    # Проверяем тест для курса тревожности (ID = 1), независимо от текущей закладки
    initial_assessment = await db.get_initial_assessment_result(user_id, 1)  # Всегда проверяем курс тревожности
    if not initial_assessment:
        await message.answer(
            "🔒 Для доступа к модулям курса необходимо сначала пройти начальную оценку.\n\n"
            "Это поможет нам лучше подстроить курс под ваши потребности и отследить ваш прогресс.\n\n"
            "Готовы пройти тест?",
            reply_markup=ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text="✅ Да, пройти тест")],
                [KeyboardButton(text="🏠 В главное меню")]
            ], resize_keyboard=True)
        )
        return
    
    progress = await db.get_all_completed_modules_for_course(user_id, bookmark['current_course_id'])
    days_kb = ikb.get_days_keyboard(bookmark['current_day'], progress)
    await message.answer("Выберите день для просмотра модулей:", reply_markup=days_kb)

# Обработчики для кнопок блокировки модулей
@router.message(F.text == "✅ Да, пройти тест")
async def start_test_from_blocked_modules(message: Message, state: FSMContext):
    """Пользователь согласился пройти тест после попытки доступа к модулям."""
    from handlers.assessments.anxiety_test import start_anxiety_test
    await start_anxiety_test(message, state)

@router.message(F.text == "🏠 В главное меню")
async def back_to_main_from_blocked_modules(message: Message):
    """Возврат в главное меню из блокировки модулей."""
    await message.answer("Возвращаю в главное меню.", reply_markup=ReplyKeyboardRemove())
    await show_main_menu(message, message.from_user.id)

@router.message(F.text == "🙏 Практики")
async def show_practices(message: Message):
    """Показывает раздел дополнительных практик."""
    await message.answer("Этот раздел находится в разработке 🚧")

# ... (остальные обработчики без изменений) ...
@router.callback_query(F.data.startswith("select_day_"))
async def day_selected(callback: CallbackQuery):
    selected_day = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    
    bookmark = await db.get_user_bookmark(user_id)
    progress = await db.get_all_completed_modules_for_course(user_id, bookmark['current_course_id'])

    modules_kb = ikb.get_modules_keyboard(selected_day, bookmark, progress)
    await callback.message.edit_text(f"Выбран день {selected_day}. Выберите модуль:", reply_markup=modules_kb)
    await callback.answer()
    
@router.callback_query(F.data.startswith("select_module_"))
async def module_selected(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    day, module = int(parts[2]), int(parts[3])
    user_id = callback.from_user.id
    
    bookmark = await db.get_user_bookmark(user_id)
    
    # Проверяем, что закладка существует
    if not bookmark:
        await callback.answer("Ошибка: закладка не найдена. Попробуйте позже.", show_alert=True)
        return
    
    course_id = bookmark['current_course_id']
    
    # Обновляем закладку пользователя
    await db.update_user_bookmark(user_id, course_id, day, module)

    await callback.message.delete()
    await callback.answer(f"Перехожу к модулю {day}.{module}...")
    
    # Получаем обновленную закладку
    updated_bookmark = await db.get_user_bookmark(user_id)
    
    # Запускаем выбранный модуль
    from handlers.course_flow import start_module
    await start_module(callback.message, state)

@router.callback_query(F.data.in_({"day_locked", "module_locked"}))
async def locked_button_pressed(callback: CallbackQuery):
    await callback.answer("Этот раздел еще недоступен. Пройдите предыдущие уроки.", show_alert=True)

@router.message(F.text.in_({"Практики"}))
async def menu_stubs(message: Message):
    await message.answer("Этот раздел находится в разработке 🚧")