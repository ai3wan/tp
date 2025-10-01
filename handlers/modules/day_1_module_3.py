# handlers/modules/day_1_module_3.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os

router = Router()

class Day1Module3States(StatesGroup):
    """Состояния для Дня 1, Модуля 3."""
    step_1 = State()  # Рефлексия
    step_2 = State()  # Вспышки тревоги
    step_3 = State()  # Вечерняя рефлексия
    step_4 = State()  # Замечать тревогу
    step_5 = State()  # Больше свободы
    step_6 = State()  # Практика рефлексии
    step_7 = State()  # Дыхательная практика
    step_8 = State()  # Подведение итогов 1
    step_9 = State()  # Подведение итогов 2
    step_10 = State()  # Завершение с медитацией

def get_step_keyboard(step: int) -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру для конкретного шага диалога."""
    keyboards = {
        1: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🌿 Стало легче")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        2: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💡 Понимать тревогу важно")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        3: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="⚡ Тревога — это вспышки")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        4: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🪞 Зеркало для тревоги")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        5: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👀 Замечать тревогу раньше")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        6: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🕊️ Больше свободы")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        7: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✅ Готово")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        8: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🤔 Понятно")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        9: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🌸 Запомнил")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        10: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🙌 Отлично")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        )
    }
    return keyboards.get(step, ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True))

@router.message(F.text == "▶️ День 1, Модуль 3")
async def start_day_1_module_3(message: Message, state: FSMContext):
    """Запускает третий модуль первого дня."""
    await state.set_state(Day1Module3States.step_1)
    
    # Отправляем видео с дыхательной практикой
    video_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "practice_1.mp4")
    video_file = FSInputFile(video_path)
    
    await message.answer_video(
        video=video_file,
        caption="✨ Прежде чем начать вечерний модуль, давай немного настроимся.\n"
                "🌬️ Вернёмся к нашей практике дыхания: вдох на 4 секунды ⏱️, выдох на 6.\n"
                "Подыши так пару минут — и тело станет спокойнее 😌",
        reply_markup=get_step_keyboard(1)
    )

# Шаг 1 -> Шаг 2
@router.message(Day1Module3States.step_1, F.text == "🌿 Стало легче")
async def step_1_to_2(message: Message, state: FSMContext):
    """Переход от шага 1 к шагу 2."""
    await state.set_state(Day1Module3States.step_2)
    
    await message.answer(
        "Знаешь, когда мы просто проживаем день — тревога часто пролетает мимо сознания. Но если остановиться и вспомнить её моменты, мы начинаем лучше понимать, как она работает.",
        reply_markup=get_step_keyboard(2)
    )

# Шаг 2 -> Шаг 3
@router.message(Day1Module3States.step_2, F.text == "💡 Понимать тревогу важно")
async def step_2_to_3(message: Message, state: FSMContext):
    """Переход от шага 2 к шагу 3."""
    await state.set_state(Day1Module3States.step_3)
    
    # Отправляем картинку с сообщением (если файл существует)
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m3", "d1m3_2.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="Это и есть рефлексия ✍️ Она помогает заметить: тревога — не постоянный фон, а вспышки в определённые моменты. Когда мы их видим, становится легче с ними справляться.",
            reply_markup=get_step_keyboard(3)
        )
    else:
        await message.answer(
            "Это и есть рефлексия ✍️ Она помогает заметить: тревога — не постоянный фон, а вспышки в определённые моменты. Когда мы их видим, становится легче с ними справляться.",
            reply_markup=get_step_keyboard(3)
        )

# Шаг 3 -> Шаг 4
@router.message(Day1Module3States.step_3, F.text == "⚡ Тревога — это вспышки")
async def step_3_to_4(message: Message, state: FSMContext):
    """Переход от шага 3 к шагу 4."""
    await state.set_state(Day1Module3States.step_4)
    
    # Отправляем картинку с сообщением (если файл существует)
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m3", "d1m3_3.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="Каждый вечер мы будем уделять пару минут рефлексии ✍️ Это как маленькое зеркало — ты учишься смотреть, где именно появлялась тревога за день.",
            reply_markup=get_step_keyboard(4)
        )
    else:
        await message.answer(
            "Каждый вечер мы будем уделять пару минут рефлексии ✍️ Это как маленькое зеркало — ты учишься смотреть, где именно появлялась тревога за день.",
            reply_markup=get_step_keyboard(4)
        )

# Шаг 4 -> Шаг 5
@router.message(Day1Module3States.step_4, F.text == "🪞 Зеркало для тревоги")
async def step_4_to_5(message: Message, state: FSMContext):
    """Переход от шага 4 к шагу 5."""
    await state.set_state(Day1Module3States.step_5)
    
    await message.answer(
        "Иногда тревога сидит в мыслях 💭, иногда в теле — сжатые плечи, ком в горле. Замечая это, ты постепенно начинаешь видеть её раньше и легче переключаться.",
        reply_markup=get_step_keyboard(5)
    )

# Шаг 5 -> Шаг 6
@router.message(Day1Module3States.step_5, F.text == "👀 Замечать тревогу раньше")
async def step_5_to_6(message: Message, state: FSMContext):
    """Переход от шага 5 к шагу 6."""
    await state.set_state(Day1Module3States.step_6)
    
    # Отправляем картинку с сообщением (если файл существует)
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m3", "d1m3_6.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="Такая практика работает как тренировка. Чем чаще замечаешь, тем меньше тревога управляет тобой, и тем больше у тебя свободы.",
            reply_markup=get_step_keyboard(6)
        )
    else:
        await message.answer(
            "Такая практика работает как тренировка. Чем чаще замечаешь, тем меньше тревога управляет тобой, и тем больше у тебя свободы.",
            reply_markup=get_step_keyboard(6)
        )

# Шаг 6 -> Шаг 7
@router.message(Day1Module3States.step_6, F.text == "🕊️ Больше свободы")
async def step_6_to_7(message: Message, state: FSMContext):
    """Переход от шага 6 к шагу 7."""
    await state.set_state(Day1Module3States.step_7)
    
    # Отправляем картинку с сообщением (если файл существует)
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m3", "d1m3_7.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="✍️ А теперь давай сделаем маленькую остановку.\n"
                    "Вспомни сегодняшний день и задай себе вопрос:\n"
                    "👉 «Когда я заметил тревогу?»\n\n"
                    "Выбери удобный формат и запиши свои мысли:\n"
                    "📓 можно в личный дневник\n"
                    "💬 можно прислать мне текстом\n"
                    "🎤 или даже голосовым сообщением",
            reply_markup=get_step_keyboard(7)
        )
    else:
        await message.answer(
            "✍️ А теперь давай сделаем маленькую остановку.\n"
            "Вспомни сегодняшний день и задай себе вопрос:\n"
            "👉 «Когда я заметил тревогу?»\n\n"
            "Выбери удобный формат и запиши свои мысли:\n"
            "📓 можно в личный дневник\n"
            "💬 можно прислать мне текстом\n"
            "🎤 или даже голосовым сообщением",
            reply_markup=get_step_keyboard(7)
        )

# Шаг 7 -> Шаг 8 (принимаем любой текст или голосовое)
@router.message(Day1Module3States.step_7, F.text == "✅ Готово")
@router.message(Day1Module3States.step_7, F.text)
@router.message(Day1Module3States.step_7, F.voice)
async def step_7_to_8(message: Message, state: FSMContext):
    """Переход от шага 7 к шагу 8."""
    await state.set_state(Day1Module3States.step_8)
    
    await message.answer(
        "Сегодня мы познакомились с тревогой и увидели, что она не враг, а сигнал 🚨\n"
        "Мы разобрали, почему тело так реагирует, и что тревога иногда «перебарщивает».",
        reply_markup=get_step_keyboard(8)
    )

# Шаг 8 -> Шаг 9
@router.message(Day1Module3States.step_8, F.text == "🤔 Понятно")
async def step_8_to_9(message: Message, state: FSMContext):
    """Переход от шага 8 к шагу 9."""
    await state.set_state(Day1Module3States.step_9)
    
    await message.answer(
        "Мы попробовали дыхательную практику 🌬️ (вдох 4 — выдох 6), которая помогает снижать напряжение и возвращать спокойствие.\n"
        "А вечером потренировались замечать тревогу в мыслях и теле ✍️",
        reply_markup=get_step_keyboard(9)
    )

# Шаг 9 -> Шаг 10
@router.message(Day1Module3States.step_9, F.text == "🌸 Запомнил")
async def step_9_to_10(message: Message, state: FSMContext):
    """Переход от шага 9 к шагу 10."""
    await state.set_state(Day1Module3States.step_10)
    
    await message.answer(
        "Первый шаг сделан 💪 Ты молодец!\n"
        "И помни: к любому модулю всегда можно вернуться через меню «Выбрать модуль» 📖✨",
        reply_markup=get_step_keyboard(10)
    )

# Шаг 10 -> Завершение модуля
@router.message(Day1Module3States.step_10, F.text == "🙌 Отлично")
async def complete_day_1_module_3(message: Message, state: FSMContext):
    """Завершает третий модуль первого дня."""
    import database as db
    
    # Отправляем завершающее сообщение с медитацией (если файл существует)
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m3", "d1m3_11.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="✨ А теперь давай завершим день медитацией.\n"
                    "🎧 «Сканирование дыхания» — это короткая практика, которая поможет замедлиться, отпустить напряжение и настроиться на спокойный сон 😌🌙\n\n"
                    "Просто устройся поудобнее, закрой глаза и следи за дыханием.",
            reply_markup=get_step_keyboard(10)  # Оставляем существующую клавиатуру
        )
    else:
        await message.answer(
            "✨ А теперь давай завершим день медитацией.\n"
            "🎧 «Сканирование дыхания» — это короткая практика, которая поможет замедлиться, отпустить напряжение и настроиться на спокойный сон 😌🌙\n\n"
            "Просто устройся поудобнее, закрой глаза и следи за дыханием.",
            reply_markup=get_step_keyboard(10)  # Оставляем существующую клавиатуру
        )
    
    # Отправляем медитацию отдельным сообщением (если файл существует)
    audio_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "meditations", "meditation_1.mp3")
    
    if os.path.exists(audio_path):
        audio_file = FSInputFile(audio_path)
        await message.answer_audio(
            audio=audio_file,
            caption="🎧 Медитация «Сканирование дыхания»",
            title="Сканирование дыхания",
            performer="Тихие практики"
        )
    else:
        await message.answer("🎧 Медитация временно недоступна")
    
    # Обновляем закладку пользователя на следующий день
    user_id = message.from_user.id
    await db.update_user_bookmark(user_id, course_id=1, day=2, module=1)
    
    # Показываем главное меню с обновленным прогрессом
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, user_id)

# Обработчики для кнопки "В основное меню" для каждого состояния третьего модуля
@router.message(Day1Module3States.step_1, F.text == "🏠 В основное меню")
@router.message(Day1Module3States.step_2, F.text == "🏠 В основное меню")
@router.message(Day1Module3States.step_3, F.text == "🏠 В основное меню")
@router.message(Day1Module3States.step_4, F.text == "🏠 В основное меню")
@router.message(Day1Module3States.step_5, F.text == "🏠 В основное меню")
@router.message(Day1Module3States.step_6, F.text == "🏠 В основное меню")
@router.message(Day1Module3States.step_7, F.text == "🏠 В основное меню")
@router.message(Day1Module3States.step_8, F.text == "🏠 В основное меню")
@router.message(Day1Module3States.step_9, F.text == "🏠 В основное меню")
@router.message(Day1Module3States.step_10, F.text == "🏠 В основное меню")
async def back_to_main_menu_from_module(message: Message, state: FSMContext):
    """Возвращает в главное меню."""
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, message.from_user.id)
