# handlers/modules/day_1_module_2.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class Day1Module2States(StatesGroup):
    """Состояния для Дня 1, Модуля 2."""
    introduction = State()
    practice = State()
    reflection = State()
    completion = State()

def get_day_1_module_2_keyboard() -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру для Дня 1, Модуля 2."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Понял, продолжаем")],
            [KeyboardButton(text="🔄 Повторить")],
            [KeyboardButton(text="🏠 В основное меню")]
        ],
        resize_keyboard=True
    )

@router.message(F.text == "▶️ День 1, Модуль 2")
async def start_day_1_module_2(message: Message, state: FSMContext):
    """Запускает День 1, Модуль 2."""
    await state.set_state(Day1Module2States.introduction)
    await message.answer(
        "🌱 Добро пожаловать в День 1, Модуль 2!\n\n"
        "**Тема: Техники дыхания**\n\n"
        "В этом модуле мы изучим различные техники дыхания, "
        "которые помогают быстро успокоиться в стрессовых ситуациях.\n\n"
        "Готовы начать?",
        reply_markup=get_day_1_module_2_keyboard()
    )

@router.message(Day1Module2States.introduction, F.text == "✅ Понял, продолжаем")
async def continue_day_1_module_2(message: Message, state: FSMContext):
    """Продолжает модуль после введения."""
    await state.set_state(Day1Module2States.practice)
    await message.answer(
        "🎯 Отлично! Теперь давайте изучим технику \"4-7-8\".\n\n"
        "**Техника дыхания 4-7-8:**\n\n"
        "1. Вдохните через нос на 4 счета\n"
        "2. Задержите дыхание на 7 счетов\n"
        "3. Выдохните через рот на 8 счетов\n\n"
        "Попробуйте выполнить это упражнение прямо сейчас!",
        reply_markup=get_day_1_module_2_keyboard()
    )

@router.message(Day1Module2States.practice, F.text == "✅ Понял, продолжаем")
async def complete_day_1_module_2(message: Message, state: FSMContext):
    """Завершает модуль."""
    await state.set_state(Day1Module2States.completion)
    await message.answer(
        "🎉 Поздравляем! Вы завершили День 1, Модуль 2.\n\n"
        "**Что вы изучили:**\n"
        "• Технику дыхания 4-7-8\n"
        "• Как использовать дыхание для успокоения\n"
        "• Практические навыки релаксации\n\n"
        "Отлично поработали! Переходим к следующему модулю?",
        reply_markup=get_day_1_module_2_keyboard()
    )

@router.message(F.text == "🔄 Повторить")
async def repeat_day_1_module_2(message: Message, state: FSMContext):
    """Повторяет текущий модуль."""
    await start_day_1_module_2(message, state)

@router.message(F.text == "🏠 В основное меню")
async def back_to_main_menu_from_module(message: Message, state: FSMContext):
    """Возвращает в главное меню."""
    from handlers.course_flow import show_main_menu
    await state.clear()
    await message.answer("Возвращаю вас в главное меню.", reply_markup=ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True))
    await show_main_menu(message, message.from_user.id)
