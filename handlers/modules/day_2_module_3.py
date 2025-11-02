# handlers/modules/day_2_module_3.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os

router = Router()

class Day2Module3States(StatesGroup):
    """Состояния для Дня 2, Модуля 3 - Вечерняя релаксация."""
    step_1 = State()  # Настройка на практику
    step_2 = State()  # Видео + результат
    step_3 = State()  # Тревога живёт в теле
    step_4 = State()  # Притча об Эзопе
    step_5 = State()  # Рефлексия дня
    step_6 = State()  # Прогресс
    step_7 = State()  # Медитация на ночь

def get_step_keyboard(step: int) -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру для конкретного шага."""
    keyboards = {
        1: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💪 Давай")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        2: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🌿 Стало спокойнее")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        3: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💡 Тревога живёт в теле")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        4: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🏹 Расслабление возвращает силу")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        5: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✅ Готово")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        6: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🙌 Хорошо")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
    }
    return keyboards.get(step, ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True))

@router.message(F.text == "▶️ День 2, Модуль 3")
async def start_day_2_module_3(message: Message, state: FSMContext):
    """Запускает День 2, Модуль 3 - Вечерняя релаксация."""
    await state.set_state(Day2Module3States.step_1)
    
    await message.answer(
        "✨ Прежде чем начать вечерний модуль, давай немного настроимся.\n\n"
        "🤸‍♀️ Вернёмся к нашей практике мышечной релаксации: поочерёдно напрягаем и отпускаем мышцы.",
        reply_markup=get_step_keyboard(1)
    )

# Шаг 1 -> Шаг 2 (Видео практики)
@router.message(Day2Module3States.step_1, F.text == "💪 Давай")
async def step_1_to_2(message: Message, state: FSMContext):
    """Переход от шага 1 к шагу 2."""
    await state.set_state(Day2Module3States.step_2)
    
    # Отправляем видео с практикой
    assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "practices")
    video_path = os.path.join(assets_path, "practice_2.mp4")
    
    if os.path.exists(video_path):
        video_file = FSInputFile(video_path)
        await message.answer_video(
            video=video_file,
            caption="Сожми кулаки, подними плечи, напряги лицо — а теперь всё отпусти.\n\n"
                    "Повтори несколько раз в течение минуты — и тело станет мягче и спокойнее 😌",
            reply_markup=get_step_keyboard(2)
        )
    else:
        await message.answer(
            "Сожми кулаки, подними плечи, напряги лицо — а теперь всё отпусти.\n\n"
            "Повтори несколько раз в течение минуты — и тело станет мягче и спокойнее 😌",
            reply_markup=get_step_keyboard(2)
        )

# Шаг 2 -> Шаг 3
@router.message(Day2Module3States.step_2, F.text == "🌿 Стало спокойнее")
async def step_2_to_3(message: Message, state: FSMContext):
    """Переход от шага 2 к шагу 3."""
    await state.set_state(Day2Module3States.step_3)
    
    await message.answer(
        "Сегодня мы говорили о том, что тревога живёт не только в голове, но и в теле.\n\n"
        "Она проявляется как зажимы, дрожь, ком в горле, тяжесть в животе.\n\n"
        "Тело реагирует быстрее, чем разум — и именно через тело мы можем вернуть себе спокойствие.\n\n"
        "Практика «сжать — отпустить» помогает мозгу понять, что опасности нет.\n\n"
        "Так мы разрываем круг тревоги и постепенно учим тело расслабляться.",
        reply_markup=get_step_keyboard(3)
    )

# Шаг 3 -> Шаг 4
@router.message(Day2Module3States.step_3, F.text == "💡 Тревога живёт в теле")
async def step_3_to_4(message: Message, state: FSMContext):
    """Переход от шага 3 к шагу 4."""
    await state.set_state(Day2Module3States.step_4)
    
    await message.answer(
        "📖 Помнишь притчу об Эзопе и луке?\n\n"
        "Он говорил: если держать тетиву постоянно натянутой, она теряет силу.\n\n"
        "Так и с человеком — без отдыха даже сильные устают.\n\n"
        "Сегодняшняя практика — это и есть способ немного «ослабить тетиву» и вернуть телу гибкость.",
        reply_markup=get_step_keyboard(4)
    )

# Шаг 4 -> Шаг 5 (Рефлексия)
@router.message(Day2Module3States.step_4, F.text == "🏹 Расслабление возвращает силу")
async def step_4_to_5(message: Message, state: FSMContext):
    """Переход от шага 4 к шагу 5."""
    await state.set_state(Day2Module3States.step_5)
    
    # Отправляем картинку с текстом
    assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d2m3")
    image_path = os.path.join(assets_path, "d2m3_1.jpg")
    
    text = (
        "✍️ А теперь давай сделаем маленькую остановку.\n\n"
        "Вспомни весь сегодняшний день и задай себе вопрос:\n\n"
        "👉 «Когда я замечал тревогу в теле?»\n\n"
        "Вспомни, как она проявлялась: напряжённые плечи, сжатая челюсть, тяжесть в животе.\n\n"
        "Удалось ли тебе применить практику релаксации в эти моменты? Что изменилось?\n\n"
        "Выбери удобный способ, чтобы зафиксировать это:\n\n"
        "📓 в своём дневнике,\n"
        "💬 можешь написать сюда,\n"
        "🎤 или даже записать голосом — как тебе комфортнее."
    )
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption=text,
            reply_markup=get_step_keyboard(5)
        )
    else:
        await message.answer(
            text=text,
            reply_markup=get_step_keyboard(5)
        )

# Шаг 5 -> Шаг 6 (Прогресс)
@router.message(Day2Module3States.step_5)
async def step_5_to_6(message: Message, state: FSMContext):
    """Переход от шага 5 к шагу 6 - принимаем любой текст/голос."""
    await state.set_state(Day2Module3States.step_6)
    
    await message.answer(
        "🌟 Мы отлично двигаемся! Каждый день ты добавляешь по одному простому, но важному инструменту к своей «аптечке спокойствия».\n\n"
        "Напоминаю: к любому модулю всегда можно вернуться через меню «Выбрать модуль» 📖✨",
        reply_markup=get_step_keyboard(6)
    )

# Шаг 6 -> Шаг 7 (Медитация)
@router.message(Day2Module3States.step_6, F.text == "🙌 Хорошо")
async def step_6_to_7(message: Message, state: FSMContext):
    """Переход от шага 6 к шагу 7 - медитация."""
    await state.set_state(Day2Module3States.step_7)
    
    # Отправляем аудио с медитацией
    assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "meditations")
    audio_path = os.path.join(assets_path, "meditation_1.mp3")
    
    text = (
        "🌙 День подходит к концу. Самое время позволить телу отпустить всё лишнее.\n\n"
        "🎧 Медитация «Тепло в теле» поможет расслабиться, восстановить силы и настроиться на спокойный, глубокий сон.\n\n"
        "Устройся удобно, закрой глаза и позволь теплу разлиться по всему телу 😌"
    )
    
    if os.path.exists(audio_path):
        audio_file = FSInputFile(audio_path)
        await message.answer_audio(
            audio=audio_file,
            caption=text
        )
    else:
        await message.answer(text=text)
    
    # Завершаем модуль автоматически после отправки медитации
    import database as db
    
    # Сохраняем прогресс
    user_id = message.from_user.id
    await db.complete_module(user_id, course_id=1, day=2, module=3)
    
    # Обновляем закладку на следующий день
    await db.update_user_bookmark(user_id, course_id=1, day=3, module=1)
    
    # Показываем главное меню
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, user_id)

# Обработчики для кнопки "В основное меню" для каждого состояния
@router.message(Day2Module3States.step_1, F.text == "🏠 В основное меню")
@router.message(Day2Module3States.step_2, F.text == "🏠 В основное меню")
@router.message(Day2Module3States.step_3, F.text == "🏠 В основное меню")
@router.message(Day2Module3States.step_4, F.text == "🏠 В основное меню")
@router.message(Day2Module3States.step_5, F.text == "🏠 В основное меню")
@router.message(Day2Module3States.step_6, F.text == "🏠 В основное меню")
@router.message(Day2Module3States.step_7, F.text == "🏠 В основное меню")
async def back_to_main_menu_from_module(message: Message, state: FSMContext):
    """Возвращает в главное меню."""
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, message.from_user.id)

