# handlers/modules/day_2_module_2.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os

router = Router()

class Day2Module2States(StatesGroup):
    """Состояния для Дня 2, Модуля 2 - Притча Эзопа о луке."""
    step_1 = State()  # Вступление
    step_2 = State()  # Эзоп играет с детьми
    step_3 = State()  # Лук и отдых
    step_4 = State()  # Расслабление возвращает силы
    step_5 = State()  # Напоминание про лук - практика
    step_6 = State()  # Видео практики - кулаки
    step_7 = State()  # Плечи
    step_8 = State()  # Лицо

def get_step_keyboard(step: int) -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру для конкретного шага."""
    keyboards = {
        1: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📖 Расскажи")],
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
                [KeyboardButton(text="🏹 Луку нужен отдых")],
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
                [KeyboardButton(text="✅ Давай займемся")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        6: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✊ Кулаки расслаблены")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        7: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🎒 Напряжение сброшено")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        8: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🙂 Лицо расслаблено")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
    }
    return keyboards.get(step, ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True))

@router.message(F.text == "▶️ День 2, Модуль 2")
async def start_day_2_module_2(message: Message, state: FSMContext):
    """Запускает День 2, Модуль 2 - Притча Эзопа о луке."""
    await state.set_state(Day2Module2States.step_1)
    
    await message.answer(
        "✨ Сейчас я расскажу небольшую притчу о мудреце Эзопе — о том, почему даже сила нуждается в отдыхе.\n\n"
        "Она короткая, но в ней есть важное напоминание о том, как обращаться со своим напряжением.",
        reply_markup=get_step_keyboard(1)
    )

# Шаг 1 -> Шаг 2
@router.message(Day2Module2States.step_1, F.text == "📖 Расскажи")
async def step_1_to_2(message: Message, state: FSMContext):
    """Переход от шага 1 к шагу 2."""
    await state.set_state(Day2Module2States.step_2)
    
    # Отправляем картинку с текстом
    assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d2m2")
    image_path = os.path.join(assets_path, "d2m2_1.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="Однажды друзья заметили, что мудрец Эзоп играет с детьми и рассказывает им весёлые истории.\n\n"
                    "Кто-то из прохожих усмехнулся:\n\n"
                    "— Разве это достойное занятие для мудрого человека?",
            reply_markup=get_step_keyboard(2)
        )
    else:
        await message.answer(
            "Однажды друзья заметили, что мудрец Эзоп играет с детьми и рассказывает им весёлые истории.\n\n"
            "Кто-то из прохожих усмехнулся:\n\n"
            "— Разве это достойное занятие для мудрого человека?",
            reply_markup=get_step_keyboard(2)
        )

# Шаг 2 -> Шаг 3
@router.message(Day2Module2States.step_2, F.text == "🤔 Почему нет?")
async def step_2_to_3(message: Message, state: FSMContext):
    """Переход от шага 2 к шагу 3."""
    await state.set_state(Day2Module2States.step_3)
    
    # Отправляем картинку с текстом
    assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d2m2")
    image_path = os.path.join(assets_path, "d2m2_2.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="Эзоп взял в руки лук и сказал:\n\n"
                    "— Посмотри: если держать его всё время натянутым, он быстро потеряет силу и сломается.\n\n"
                    "Но если давать ему отдых, он будет служить долго и стрелять метко.",
            reply_markup=get_step_keyboard(3)
        )
    else:
        await message.answer(
            "Эзоп взял в руки лук и сказал:\n\n"
            "— Посмотри: если держать его всё время натянутым, он быстро потеряет силу и сломается.\n\n"
            "Но если давать ему отдых, он будет служить долго и стрелять метко.",
            reply_markup=get_step_keyboard(3)
        )

# Шаг 3 -> Шаг 4
@router.message(Day2Module2States.step_3, F.text == "🏹 Луку нужен отдых")
async def step_3_to_4(message: Message, state: FSMContext):
    """Переход от шага 3 к шагу 4."""
    await state.set_state(Day2Module2States.step_4)
    
    # Отправляем картинку с текстом
    assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d2m2")
    image_path = os.path.join(assets_path, "d2m2_3.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="— Так и с человеком, — добавил Эзоп. — Если жить в постоянном напряжении, тревога только накапливается.\n\n"
                    "Но стоит позволить себе расслабиться — и силы возвращаются.",
            reply_markup=get_step_keyboard(4)
        )
    else:
        await message.answer(
            "— Так и с человеком, — добавил Эзоп. — Если жить в постоянном напряжении, тревога только накапливается.\n\n"
            "Но стоит позволить себе расслабиться — и силы возвращаются.",
            reply_markup=get_step_keyboard(4)
        )

# Шаг 4 -> Шаг 5
@router.message(Day2Module2States.step_4, F.text == "🌿 Расслабление возвращает силы")
async def step_4_to_5(message: Message, state: FSMContext):
    """Переход от шага 4 к шагу 5."""
    await state.set_state(Day2Module2States.step_5)
    
    await message.answer(
        "🌬️ Помнишь, что говорил Эзоп про лук?\n\n"
        "Если держать тетиву всё время натянутой — она теряет силу. Так же и мы: когда тело постоянно в напряжении, тревога только растёт.\n\n"
        "Поэтому сейчас мы сделаем то, о чём говорил мудрец — натянем и отпустим.",
        reply_markup=get_step_keyboard(5)
    )

# Шаг 5 -> Шаг 6 (Видео практики)
@router.message(Day2Module2States.step_5, F.text == "✅ Давай займемся")
async def step_5_to_6(message: Message, state: FSMContext):
    """Переход от шага 5 к шагу 6 - видео практики."""
    await state.set_state(Day2Module2States.step_6)
    
    # Отправляем видео с практикой
    assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "practices")
    video_path = os.path.join(assets_path, "practice_2.mp4")
    
    if os.path.exists(video_path):
        video_file = FSInputFile(video_path)
        await message.answer_video(
            video=video_file,
            caption="Вспомним утреннюю практику «Прогрессивная мышечная релаксация»:\n\n"
                    "поочерёдно напрягаем и расслабляем разные части тела — ✊ кулаки, 💪 плечи, 🙂 лицо.",
            reply_markup=get_step_keyboard(6)
        )
    else:
        await message.answer(
            "Вспомним утреннюю практику «Прогрессивная мышечная релаксация»:\n\n"
            "поочерёдно напрягаем и расслабляем разные части тела — ✊ кулаки, 💪 плечи, 🙂 лицо.",
            reply_markup=get_step_keyboard(6)
        )

# Шаг 6 -> Шаг 7 (Плечи)
@router.message(Day2Module2States.step_6, F.text == "✊ Кулаки расслаблены")
async def step_6_to_7(message: Message, state: FSMContext):
    """Переход от шага 6 к шагу 7."""
    await state.set_state(Day2Module2States.step_7)
    
    await message.answer(
        "Следующая остановка — плечи. Здесь тревога любит прятаться.",
        reply_markup=get_step_keyboard(7)
    )

# Шаг 7 -> Шаг 8 (Лицо)
@router.message(Day2Module2States.step_7, F.text == "🎒 Напряжение сброшено")
async def step_7_to_8(message: Message, state: FSMContext):
    """Переход от шага 7 к шагу 8."""
    await state.set_state(Day2Module2States.step_8)
    
    await message.answer(
        "И наконец — лицо. Попробуй заметить и отпустить напряжение здесь.",
        reply_markup=get_step_keyboard(8)
    )

# Шаг 8 -> Завершение модуля
@router.message(Day2Module2States.step_8, F.text == "🙂 Лицо расслаблено")
async def complete_day_2_module_2(message: Message, state: FSMContext):
    """Завершает второй модуль второго дня."""
    import database as db
    
    await message.answer(
        "Это простой способ ощутить ту самую разницу между усилием и покоем, о которой говорил Эзоп.\n\n"
        "💫 Отличная работа! Помни: отдых — это не слабость, а необходимость.\n\n"
        "📌 До встречи в следующем модуле!"
    )
    
    # ИСПРАВЛЕНИЕ: Сохраняем прогресс перед обновлением закладки
    user_id = message.from_user.id
    await db.complete_module(user_id, course_id=1, day=2, module=2)
    
    # Обновляем закладку пользователя на следующий модуль
    await db.update_user_bookmark(user_id, course_id=1, day=2, module=3)
    
    # Показываем главное меню с обновленным прогрессом
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, user_id)

# Обработчики для кнопки "В основное меню" для каждого состояния
@router.message(Day2Module2States.step_1, F.text == "🏠 В основное меню")
@router.message(Day2Module2States.step_2, F.text == "🏠 В основное меню")
@router.message(Day2Module2States.step_3, F.text == "🏠 В основное меню")
@router.message(Day2Module2States.step_4, F.text == "🏠 В основное меню")
@router.message(Day2Module2States.step_5, F.text == "🏠 В основное меню")
@router.message(Day2Module2States.step_6, F.text == "🏠 В основное меню")
@router.message(Day2Module2States.step_7, F.text == "🏠 В основное меню")
@router.message(Day2Module2States.step_8, F.text == "🏠 В основное меню")
async def back_to_main_menu_from_module(message: Message, state: FSMContext):
    """Возвращает в главное меню."""
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, message.from_user.id)

