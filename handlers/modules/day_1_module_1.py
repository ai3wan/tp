# handlers/modules/day_1_module_1.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class Day1Module1States(StatesGroup):
    """Состояния для Дня 1, Модуля 1."""
    introduction = State()
    practice = State()
    reflection = State()
    completion = State()

def get_day_1_module_1_keyboard() -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру для Дня 1, Модуля 1."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Понял, продолжаем")],
            [KeyboardButton(text="🔄 Повторить")],
            [KeyboardButton(text="🏠 В основное меню")]
        ],
        resize_keyboard=True
    )

@router.message(F.text == "▶️ День 1, Модуль 1")
async def start_day_1_module_1(message: Message, state: FSMContext):
    """Запускает День 1, Модуль 1."""
    await state.set_state(Day1Module1States.introduction)
    await message.answer(
        "🌅 Добро пожаловать в День 1, Модуль 1!\n\n"
        "**Тема: Понимание тревожности**\n\n"
        "Сегодня мы изучим основы работы с тревожностью. "
        "Вы узнаете, что такое тревожность, как она проявляется "
        "и какие техники помогают с ней справляться.\n\n"
        "Готовы начать?",
        reply_markup=get_day_1_module_1_keyboard()
    )

@router.message(Day1Module1States.introduction, F.text == "✅ Понял, продолжаем")
async def continue_day_1_module_1(message: Message, state: FSMContext):
    """Продолжает модуль после введения."""
    await state.set_state(Day1Module1States.practice)
    await message.answer(
        "🎯 Отлично! Теперь давайте перейдем к практике.\n\n"
        "**Практическое упражнение:**\n\n"
        "1. Найдите тихое место\n"
        "2. Сядьте удобно\n"
        "3. Закройте глаза\n"
        "4. Сделайте 3 глубоких вдоха\n\n"
        "Как вы себя чувствуете после этого упражнения?",
        reply_markup=get_day_1_module_1_keyboard()
    )

@router.message(Day1Module1States.practice, F.text == "✅ Понял, продолжаем")
async def complete_day_1_module_1(message: Message, state: FSMContext):
    """Завершает модуль."""
    await state.set_state(Day1Module1States.completion)
    await message.answer(
        "🎉 Поздравляем! Вы завершили День 1, Модуль 1.\n\n"
        "**Что вы изучили:**\n"
        "• Основы понимания тревожности\n"
        "• Простое дыхательное упражнение\n"
        "• Технику расслабления\n\n"
        "Отлично поработали! Переходим к следующему модулю?",
        reply_markup=get_day_1_module_1_keyboard()
    )

@router.message(Day1Module1States.completion, F.text == "✅ Понял, продолжаем")
async def finish_day_1_module_1(message: Message, state: FSMContext):
    """Завершает модуль и переходит к следующему."""
    from handlers.course_flow import complete_module
    await state.clear()  # Очищаем состояние модуля
    await complete_module(message)  # Вызываем функцию завершения модуля

@router.message(F.text == "🔄 Повторить")
async def repeat_day_1_module_1(message: Message, state: FSMContext):
    """Повторяет текущий модуль."""
    await start_day_1_module_1(message, state)

@router.message(F.text == "🏠 В основное меню")
async def back_to_main_menu_from_module(message: Message, state: FSMContext):
    """Возвращает в главное меню."""
    import database as db
    import keyboards.reply as kb
    
    await state.clear()
    await message.answer("Возвращаю вас в главное меню.", reply_markup=ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True))
    
    # Получаем закладку пользователя
    user_id = message.from_user.id
    bookmark = await db.get_user_bookmark(user_id)
    
    if not bookmark or not bookmark['current_course_id']:
        await message.answer("Ошибка: пользователь не найден. Попробуйте перезапустить бота командой /start")
        return
    
    # Формируем главное меню
    main_button_text = f"▶️ День {bookmark['current_day']}, Модуль {bookmark['current_module']}"
    
    main_menu_kb = kb.ReplyKeyboardMarkup(
        keyboard=[
            [kb.KeyboardButton(text=main_button_text), kb.KeyboardButton(text="📚 Выбрать модуль")],
            [kb.KeyboardButton(text="🙏 Практики"), kb.KeyboardButton(text="🙍 Профиль")]
        ],
        resize_keyboard=True
    )
    await message.answer(reply_markup=main_menu_kb)
