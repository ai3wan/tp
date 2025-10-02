"""
Обработчики для второго дня, второго модуля.
Притча Эзопа о луке и практика расслабления.
"""

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from FSM.states import Day2Module2States

router = Router()

def get_step_keyboard(step: int) -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру для конкретного шага."""
    keyboards = {
        1: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📖 Хочу услышать")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        2: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🤔 Почему нет?")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        3: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🏹 Лук нужен отдых")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        4: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🌿 Расслабление возвращает силы")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        5: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✅ Готов попробовать")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        6: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🌿 Стало легче")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        )
    }
    return keyboards.get(step, ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True))

@router.message(F.text == "▶️ День 2, Модуль 2")
async def start_day_2_module_2(message: Message, state: FSMContext):
    """Запускает второй день, второй модуль."""
    await state.set_state(Day2Module2States.step_1)
    
    await message.answer(
        "✨ Иногда простые истории передают важные истины лучше любых объяснений.\n"
        "Сейчас я расскажу притчу, которая напоминает: даже мудрости нужен отдых, а постоянное напряжение только разрушает.",
        reply_markup=get_step_keyboard(1)
    )

# Шаг 1 -> Шаг 2
@router.message(Day2Module2States.step_1, F.text == "📖 Хочу услышать")
async def step_1_to_2(message: Message, state: FSMContext):
    """Переход от шага 1 к шагу 2."""
    await state.set_state(Day2Module2States.step_2)
    
    await message.answer(
        "📖 Говорят, однажды Эзоп отдыхал и играл с детьми.\n"
        "Прохожий увидел это и с усмешкой спросил:\n"
        "— Разве подобает мудрому человеку тратить время так несерьёзно?",
        reply_markup=get_step_keyboard(2)
    )

# Шаг 2 -> Шаг 3
@router.message(Day2Module2States.step_2, F.text == "🤔 Почему нет?")
async def step_2_to_3(message: Message, state: FSMContext):
    """Переход от шага 2 к шагу 3."""
    await state.set_state(Day2Module2States.step_3)
    
    await message.answer(
        "Эзоп взял в руки лук и сказал:\n"
        "— Если держать его всё время натянутым, он быстро потеряет силу и сломается. Но если давать ему отдых, он будет служить долго и стрелять метко.",
        reply_markup=get_step_keyboard(3)
    )

# Шаг 3 -> Шаг 4
@router.message(Day2Module2States.step_3, F.text == "🏹 Лук нужен отдых")
async def step_3_to_4(message: Message, state: FSMContext):
    """Переход от шага 3 к шагу 4."""
    await state.set_state(Day2Module2States.step_4)
    
    await message.answer(
        "И добавил:\n"
        "— Так и с человеком. Если жить в постоянном напряжении, тревога лишь растёт. Но стоит позволить себе расслабиться — и силы возвращаются.",
        reply_markup=get_step_keyboard(4)
    )

# Шаг 4 -> Шаг 5
@router.message(Day2Module2States.step_4, F.text == "🌿 Расслабление возвращает силы")
async def step_4_to_5(message: Message, state: FSMContext):
    """Переход от шага 4 к шагу 5."""
    await state.set_state(Day2Module2States.step_5)
    
    await message.answer(
        "🌬️ А теперь давай не только запомним эту мудрость, но и применим её.\n"
        "Мы снова вернёмся к нашей практике расслабления — простой, но действенной.\n"
        "Немного дыхания и телесного отпускания помогут прочувствовать то, о чём говорил Эзоп.",
        reply_markup=get_step_keyboard(5)
    )

# Шаг 5 -> Шаг 6
@router.message(Day2Module2States.step_5, F.text == "✅ Готов попробовать")
async def step_5_to_6(message: Message, state: FSMContext):
    """Переход от шага 5 к шагу 6."""
    await state.set_state(Day2Module2States.step_6)
    
    # Отправляем видео с практикой (если файл существует)
    import os
    from aiogram.types import FSInputFile
    
    video_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "practices", "practice_2.mp4")
    
    caption_text = (
        "**Мышечная релаксация**\n\n"
        "Сожми ✊ кулаки на пару секунд — и отпусти.\n"
        "Подними 💪 плечи к ушам — задержи и расслабь вниз.\n"
        "Сожми 🙂 лицо (челюсти, брови) — а потом полностью отпусти.\n\n"
        "⏱ Повтори цикл 2–3 раза и обрати внимание, как тело становится мягче и спокойнее."
    )

    if os.path.exists(video_path):
        video_file = FSInputFile(video_path)
        await message.answer_video(
            video=video_file,
            caption=caption_text,
            parse_mode="Markdown",
            reply_markup=get_step_keyboard(6)
        )
    else:
        await message.answer(
            text=caption_text,
            parse_mode="Markdown",
            reply_markup=get_step_keyboard(6)
        )

# Шаг 6 -> Завершение модуля
@router.message(Day2Module2States.step_6, F.text == "🌿 Стало легче")
async def complete_day_2_module_2(message: Message, state: FSMContext):
    """Завершает второй день, второй модуль."""
    import database as db
    
    # Отправляем завершающее сообщение
    await message.answer(
        "📌 До встречи вечером в следующем модуле!\n"
        "Мы вспомним, что узнали сегодня, ещё раз повторим практику и послушаем короткую медитацию про расслабление и отпускание тревоги."
    )
    
    # Обновляем закладку пользователя на следующий модуль
    user_id = message.from_user.id
    await db.update_user_bookmark(user_id, course_id=1, day=2, module=3)
    
    # Показываем главное меню с обновленным прогрессом
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, user_id)

# Обработчики для кнопки "В основное меню" для каждого состояния второго дня, второго модуля
@router.message(Day2Module2States.step_1, F.text == "🏠 В основное меню")
@router.message(Day2Module2States.step_2, F.text == "🏠 В основное меню")
@router.message(Day2Module2States.step_3, F.text == "🏠 В основное меню")
@router.message(Day2Module2States.step_4, F.text == "🏠 В основное меню")
@router.message(Day2Module2States.step_5, F.text == "🏠 В основное меню")
@router.message(Day2Module2States.step_6, F.text == "🏠 В основное меню")
async def back_to_main_menu(message: Message, state: FSMContext):
    """Возвращает в главное меню из любого состояния второго дня, второго модуля."""
    from handlers.course_flow import show_main_menu
    await state.clear()
    user_id = message.from_user.id
    await show_main_menu(message, user_id)
