# handlers/modules/day_1_module_2.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os

router = Router()

class Day1Module2States(StatesGroup):
    """Состояния для Дня 1, Модуля 2."""
    introduction = State()
    story_1 = State()
    story_2 = State()
    story_3 = State()
    practice_reminder = State()
    practice_video = State()
    completion = State()

def get_introduction_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для введения."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Да, интересно"), KeyboardButton(text="Расскажи")],
            [KeyboardButton(text="🏠 В основное меню")]
        ],
        resize_keyboard=True
    )

def get_story_1_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для первой части истории."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🤔 Интересно"), KeyboardButton(text="В основное меню")],
            [KeyboardButton(text="🏠 В основное меню")]
        ],
        resize_keyboard=True
    )

def get_story_2_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для второй части истории."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="😮 Неожиданно"), KeyboardButton(text="В основное меню")],
            [KeyboardButton(text="🏠 В основное меню")]
        ],
        resize_keyboard=True
    )

def get_story_3_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для третьей части истории."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌿 Сильно"), KeyboardButton(text="В основное меню")],
            [KeyboardButton(text="🏠 В основное меню")]
        ],
        resize_keyboard=True
    )

def get_practice_reminder_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для напоминания о практике."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏩ Вперёд"), KeyboardButton(text="🙌 Давай")],
            [KeyboardButton(text="🏠 В основное меню")]
        ],
        resize_keyboard=True
    )

def get_practice_video_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для видео практики."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌿 Уже лучше"), KeyboardButton(text="😌 Спокойнее")],
            [KeyboardButton(text="🏠 В основное меню")]
        ],
        resize_keyboard=True
    )

def get_completion_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для завершения модуля."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🙌 До встречи"), KeyboardButton(text="🔄 Давай повторим")],
            [KeyboardButton(text="🏠 В основное меню")]
        ],
        resize_keyboard=True
    )

@router.message(F.text == "▶️ День 1, Модуль 2")
async def start_day_1_module_2(message: Message, state: FSMContext):
    """Запускает День 1, Модуль 2."""
    await state.set_state(Day1Module2States.introduction)
    
    await message.answer(
        "✨ Знаешь, тревожность — не изобретение нашего времени. Люди сталкивались с ней тысячи лет назад и тоже искали способы справиться. Сейчас я расскажу тебе одну короткую, но очень мудрую притчу на эту тему.",
        reply_markup=get_introduction_keyboard()
    )

@router.message(Day1Module2States.introduction, F.text.in_(["Да, интересно", "Расскажи"]))
async def show_story_1(message: Message, state: FSMContext):
    """Показывает первую часть истории."""
    await state.set_state(Day1Module2States.story_1)
    
    # Отправляем картинку с первой частью истории
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
        "assets", "d1m2", "d1m2_1.jpg"
    )
    
    story_text = "Будда говорил своим ученикам:\n«Представьте себе человека, в которого попала стрела. Он испытывает сильную боль — и это естественно. Но теперь вообразите, что в того же человека попадает ещё одна стрела в то же самое место. Вторая рана причиняет куда больше страдания, чем первая»."
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption=story_text,
            reply_markup=get_story_1_keyboard()
        )
    else:
        await message.answer(
            story_text,
            reply_markup=get_story_1_keyboard()
        )

@router.message(Day1Module2States.story_1, F.text == "🤔 Интересно")
async def show_story_2(message: Message, state: FSMContext):
    """Показывает вторую часть истории."""
    await state.set_state(Day1Module2States.story_2)
    
    # Отправляем картинку со второй частью истории
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
        "assets", "d1m2", "d1m2_2.jpg"
    )
    
    story_text = "Ученики удивились: «Учитель, а зачем вторая стрела?»\nБудда ответил: «Первая стрела — это то, что даёт нам сама жизнь: болезнь, усталость, неприятные события, стресс. Это то, что нельзя полностью избежать. Но вторая стрела — это то, что мы пускаем сами. Это наши мысли, тревога, страхи и накручивание. Мы добавляем боль туда, где можно было бы ограничиться только первой стрелой»."
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption=story_text,
            reply_markup=get_story_2_keyboard()
        )
    else:
        await message.answer(
            story_text,
            reply_markup=get_story_2_keyboard()
        )

@router.message(Day1Module2States.story_2, F.text == "😮 Неожиданно")
async def show_story_3(message: Message, state: FSMContext):
    """Показывает третью часть истории."""
    await state.set_state(Day1Module2States.story_3)
    
    # Отправляем картинку с третьей частью истории
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
        "assets", "d1m2", "d1m2_3.jpg"
    )
    
    story_text = "Он пояснил: «Обычный человек чувствует обе стрелы. Первая причиняет физическую или ситуационную боль, а вторая рождается в уме — \"Почему это случилось со мной? Что будет дальше? Я не справлюсь!\". Но мудрый человек учится замечать: \"Да, боль есть, стресс есть, но я не обязан усиливать её второй стрелой\". И тогда страдание уменьшается вдвое»."
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption=story_text,
            reply_markup=get_story_3_keyboard()
        )
    else:
        await message.answer(
            story_text,
            reply_markup=get_story_3_keyboard()
        )

@router.message(Day1Module2States.story_3, F.text == "🌿 Сильно")
async def continue_after_story(message: Message, state: FSMContext):
    """Продолжает модуль после истории."""
    await state.set_state(Day1Module2States.practice_reminder)
    
    await message.answer(
        "Помнишь наше дыхание утром? 😉 Вдох на 4, выдох на 6.\nДавай сделаем ещё раз прямо сейчас — повторение закрепляет навык 💪😌",
        reply_markup=get_practice_reminder_keyboard()
    )

@router.message(Day1Module2States.practice_reminder, F.text.in_(["⏩ Вперёд", "🙌 Давай"]))
async def show_practice_video(message: Message, state: FSMContext):
    """Показывает видео практики."""
    await state.set_state(Day1Module2States.practice_video)
    
    # Отправляем видео
    import os
    from aiogram.types import FSInputFile
    
    video_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
        "assets", "practice_1.mp4"
    )
    video_file = FSInputFile(video_path)
    
    await message.answer_video(
        video=video_file,
        caption="<b>Дыхание 4–6</b>\n\nСмотри на видео: 🔽 круг сужается — вдох, 🔼 расширяется — выдох.\n⏱ Подыши так несколько минут с таймером.",
        parse_mode="HTML",
        reply_markup=get_practice_video_keyboard()
    )

@router.message(Day1Module2States.practice_video, F.text.in_(["🌿 Уже лучше", "😌 Спокойнее"]))
async def complete_module(message: Message, state: FSMContext):
    """Завершает модуль."""
    await state.set_state(Day1Module2States.completion)
    
    await message.answer(
        "📌 До встречи в следующем модуле!\nТам мы вспомним, что сегодня узнали, ещё раз повторим дыхательную практику 🌬️ и послушаем короткую медитацию для расслабления 🎧✨",
        reply_markup=get_completion_keyboard()
    )

@router.message(Day1Module2States.completion, F.text == "🙌 До встречи")
async def finish_module(message: Message, state: FSMContext):
    """Завершает модуль и переходит к следующему."""
    from handlers.course_flow import complete_module
    await state.clear()
    await complete_module(message)

@router.message(Day1Module2States.completion, F.text == "🔄 Давай повторим")
async def repeat_module(message: Message, state: FSMContext):
    """Повторяет модуль."""
    await start_day_1_module_2(message, state)

# Обработчики для кнопок навигации
@router.message(F.text == "🏠 В основное меню")
async def back_to_main_menu_from_module(message: Message, state: FSMContext):
    """Возвращает в главное меню."""
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, message.from_user.id)

# Обработчики для кнопок "В основное меню" в истории
@router.message(Day1Module2States.story_1, F.text == "В основное меню")
@router.message(Day1Module2States.story_2, F.text == "В основное меню")
@router.message(Day1Module2States.story_3, F.text == "В основное меню")
async def back_to_main_menu_from_story(message: Message, state: FSMContext):
    """Возвращает в главное меню из истории."""
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, message.from_user.id)