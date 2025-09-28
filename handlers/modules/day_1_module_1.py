# handlers/modules/day_1_module_1.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class Day1Module1States(StatesGroup):
    """Состояния для Дня 1, Модуля 1 - интерактивный диалог."""
    step_1 = State()  # Приветствие
    step_2 = State()  # Тревога как сигнализация
    step_3 = State()  # Мозг и защита
    step_4 = State()  # Пример с собеседованием
    step_5 = State()  # Тревога не слабость
    step_6 = State()  # Перебарщивает тревога
    step_7 = State()  # Дружить с тревогой
    step_8 = State()  # Дыхание как инструмент
    step_9 = State()  # Дыхание и тревога
    step_10 = State()  # Практика дыхания
    step_11 = State()  # Результат практики
    step_12 = State()  # Вывод
    step_13 = State()  # Видео практики
    step_14 = State()  # Мотивация

def get_step_keyboard(step: int) -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру для конкретного шага диалога."""
    keyboards = {
        1: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👍 Да, поехали"), KeyboardButton(text="У всех бывает тревога")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        2: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🚨 Тревога как сигнализация"), KeyboardButton(text="О как интересно")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        3: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="😮 Ясно"), KeyboardButton(text="Опасность, где её нет")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        4: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="😅 Было такое"), KeyboardButton(text="Сердце бьётся быстрее")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        5: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👍 Я понял"), KeyboardButton(text="Тревога — не слабость")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        6: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Перебарщивает тревога 😄"), KeyboardButton(text="Ага, понял")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        7: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Дружить с тревогой 🤔"), KeyboardButton(text="Отлично!")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        8: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Дыхание — инструмент"), KeyboardButton(text="🙌 Звучит просто")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        9: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔁 Замедлить дыхание"), KeyboardButton(text="Понял 👍")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        10: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Вдох 4 — выдох 6"), KeyboardButton(text="Да, давай")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        11: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="😊 Немного спокойнее"), KeyboardButton(text="Становится спокойнее")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        12: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👍 Ясно"), KeyboardButton(text="Тревога — просто сигнал")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        13: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="😊 Стало спокойнее"), KeyboardButton(text="🤔 Нужно ещё потренироваться")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        14: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🌟 Супер"), KeyboardButton(text="🌬 Буду практиковать")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        )
    }
    return keyboards.get(step, ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True))

@router.message(F.text == "▶️ День 1, Модуль 1")
async def start_day_1_module_1(message: Message, state: FSMContext):
    """Запускает День 1, Модуль 1 - интерактивный диалог."""
    await state.set_state(Day1Module1States.step_1)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_1.png")
    image_file = FSInputFile(image_path)
    
    await message.answer_photo(
        photo=image_file,
        caption="Привет 👋 Сегодня мы начинаем наш курс. Первое, что важно понять: тревога — это часть жизни каждого человека. Она бывает у всех, даже у самых уверенных людей. Готов узнать, как с ней обращаться?",
        reply_markup=get_step_keyboard(1)
    )

# Шаг 1 -> Шаг 2
@router.message(Day1Module1States.step_1, F.text.in_(["👍 Да, поехали", "У всех бывает тревога"]))
async def step_1_to_2(message: Message, state: FSMContext):
    """Переход от шага 1 к шагу 2."""
    await state.set_state(Day1Module1States.step_2)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_2.png")
    image_file = FSInputFile(image_path)
    
    await message.answer_photo(
        photo=image_file,
        caption="Звучит странно, но тревога — не враг 😌 Она работает как сигнализация: громкая, навязчивая, но с одной целью — предупредить. Иногда эта «сигналка» срабатывает даже тогда, когда опасности нет.",
        reply_markup=get_step_keyboard(2)
    )

# Шаг 2 -> Шаг 3
@router.message(Day1Module1States.step_2, F.text.in_(["🚨 Тревога как сигнализация", "О как интересно"]))
async def step_2_to_3(message: Message, state: FSMContext):
    """Переход от шага 2 к шагу 3."""
    await state.set_state(Day1Module1States.step_3)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_3.png")
    image_file = FSInputFile(image_path)
    
    await message.answer_photo(
        photo=image_file,
        caption="Наш мозг создан, чтобы защищать нас 🧠 Он оценивает мир вокруг и ищет угрозы. Но иногда он видит опасность там, где её на самом деле нет — например, перед выступлением или важным разговором.",
        reply_markup=get_step_keyboard(3)
    )

# Шаг 3 -> Шаг 4
@router.message(Day1Module1States.step_3, F.text.in_(["😮 Ясно", "Опасность, где её нет"]))
async def step_3_to_4(message: Message, state: FSMContext):
    """Переход от шага 3 к шагу 4."""
    await state.set_state(Day1Module1States.step_4)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_4.png")
    image_file = FSInputFile(image_path)
    
    await message.answer_photo(
        photo=image_file,
        caption="Представь ситуацию: завтра собеседование. Всё идёт нормально, но сердце начинает биться быстрее ❤️‍🔥 ладони потеют, мысли скачут. Это не потому, что что-то плохое случилось — так тело готовит тебя к «битве».",
        reply_markup=get_step_keyboard(4)
    )

# Шаг 4 -> Шаг 5
@router.message(Day1Module1States.step_4, F.text.in_(["😅 Было такое", "Сердце бьётся быстрее"]))
async def step_4_to_5(message: Message, state: FSMContext):
    """Переход от шага 4 к шагу 5."""
    await state.set_state(Day1Module1States.step_5)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_5.png")
    image_file = FSInputFile(image_path)
    
    await message.answer_photo(
        photo=image_file,
        caption="И вот главный момент 👉 тревога — это не признак слабости. Это просто сигнал: «Внимание, может быть что-то важное». Она пытается мобилизовать силы, даже если ситуация не такая уж и опасная.",
        reply_markup=get_step_keyboard(5)
    )

# Шаг 5 -> Шаг 6
@router.message(Day1Module1States.step_5, F.text.in_(["👍 Я понял", "Тревога — не слабость"]))
async def step_5_to_6(message: Message, state: FSMContext):
    """Переход от шага 5 к шагу 6."""
    await state.set_state(Day1Module1States.step_6)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_6.png")
    image_file = FSInputFile(image_path)
    
    await message.answer_photo(
        photo=image_file,
        caption="Проблема в том, что тревога часто перебарщивает 🙃 Она включает режим «всё горит», когда достаточно было бы маленькой лампочки. Поэтому важно учиться регулировать её громкость.",
        reply_markup=get_step_keyboard(6)
    )

# Шаг 6 -> Шаг 7
@router.message(Day1Module1States.step_6, F.text.in_(["Перебарщивает тревога 😄", "Ага, понял"]))
async def step_6_to_7(message: Message, state: FSMContext):
    """Переход от шага 6 к шагу 7."""
    await state.set_state(Day1Module1States.step_7)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_7.png")
    image_file = FSInputFile(image_path)
    
    await message.answer_photo(
        photo=image_file,
        caption="И это хорошая новость 😊 Мы можем научиться дружить с тревогой. Не подавлять её, не гнать прочь, а относиться как к сигналу, который можно приглушить и направить в нужное русло.",
        reply_markup=get_step_keyboard(7)
    )

# Шаг 7 -> Шаг 8
@router.message(Day1Module1States.step_7, F.text.in_(["Дружить с тревогой 🤔", "Отлично!"]))
async def step_7_to_8(message: Message, state: FSMContext):
    """Переход от шага 7 к шагу 8."""
    await state.set_state(Day1Module1States.step_8)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_8.png")
    image_file = FSInputFile(image_path)
    
    await message.answer_photo(
        photo=image_file,
        caption="Первый способ регулировать тревогу — дыхание 🌬️ Это самый простой инструмент, который всегда с тобой. Через дыхание мы можем успокоить нервную систему и вернуть контроль над состоянием.",
        reply_markup=get_step_keyboard(8)
    )

# Шаг 8 -> Шаг 9
@router.message(Day1Module1States.step_8, F.text.in_(["Дыхание — инструмент", "🙌 Звучит просто"]))
async def step_8_to_9(message: Message, state: FSMContext):
    """Переход от шага 8 к шагу 9."""
    await state.set_state(Day1Module1States.step_9)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_9.png")
    image_file = FSInputFile(image_path)
    
    await message.answer_photo(
        photo=image_file,
        caption="Заметь: когда ты тревожишься, дыхание становится быстрым и поверхностным. Это запускает цепочку «больше кислорода → быстрее сердце → сильнее тревога». Если дыхание замедлить, тревога снижается 🔇",
        reply_markup=get_step_keyboard(9)
    )

# Шаг 9 -> Шаг 10
@router.message(Day1Module1States.step_9, F.text.in_(["🔁 Замедлить дыхание", "Понял 👍"]))
async def step_9_to_10(message: Message, state: FSMContext):
    """Переход от шага 9 к шагу 10."""
    await state.set_state(Day1Module1States.step_10)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_10.png")
    image_file = FSInputFile(image_path)
    
    await message.answer_photo(
        photo=image_file,
        caption="Попробуем прямо сейчас 👌 Сделай вдох на 4 секунды, а выдох — на 6. Повтори два круга. Считай в уме или по пальцам — это помогает держать ритм.",
        reply_markup=get_step_keyboard(10)
    )

# Шаг 10 -> Шаг 11
@router.message(Day1Module1States.step_10, F.text.in_(["Вдох 4 — выдох 6", "Да, давай"]))
async def step_10_to_11(message: Message, state: FSMContext):
    """Переход от шага 10 к шагу 11."""
    await state.set_state(Day1Module1States.step_11)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_11.png")
    image_file = FSInputFile(image_path)
    
    await message.answer_photo(
        photo=image_file,
        caption="Хорошо 👏 Обрати внимание: после этих нескольких дыханий тело чуть расслабляется, мысли становятся спокойнее. Это простой, но мощный способ «снизить громкость» тревоги.",
        reply_markup=get_step_keyboard(11)
    )

# Шаг 11 -> Шаг 12
@router.message(Day1Module1States.step_11, F.text.in_(["😊 Немного спокойнее", "Становится спокойнее"]))
async def step_11_to_12(message: Message, state: FSMContext):
    """Переход от шага 11 к шагу 12."""
    await state.set_state(Day1Module1States.step_12)
    await message.answer(
        "Итак, вывод: тревога сама по себе не опасна, она лишь сигнал. Но у тебя есть инструмент — дыхание. Ты можешь использовать его всегда, когда тревога слишком настойчива.",
        reply_markup=get_step_keyboard(12)
    )

# Шаг 12 -> Шаг 13
@router.message(Day1Module1States.step_12, F.text.in_(["👍 Ясно", "Тревога — просто сигнал"]))
async def step_12_to_13(message: Message, state: FSMContext):
    """Переход от шага 12 к шагу 13."""
    await state.set_state(Day1Module1States.step_13)
    
    # Отправляем видео с текстом
    import os
    from aiogram.types import FSInputFile
    
    video_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "practice_1.mp4")
    video_file = FSInputFile(video_path)
    
    await message.answer_video(
        video=video_file,
        caption="🧘 Первая практика курса — дыхание 4–6.\nСмотри на видео: 🔽 круг сужается — вдох, 🔼 расширяется — выдох.\n⏱ Подыши так несколько минут с таймером.",
        reply_markup=get_step_keyboard(13)
    )

# Шаг 13 -> Шаг 14
@router.message(Day1Module1States.step_13, F.text.in_(["😊 Стало спокойнее", "🤔 Нужно ещё потренироваться"]))
async def step_13_to_14(message: Message, state: FSMContext):
    """Переход от шага 13 к шагу 14."""
    await state.set_state(Day1Module1States.step_14)
    await message.answer(
        "Сегодня мы ещё дважды вернёмся к этой практике: 🌞 днём и 🌙 вечером.\nЧем чаще будешь пробовать, тем привычнее станет регулировать своё состояние ⚖️✨",
        reply_markup=get_step_keyboard(14)
    )

# Шаг 14 -> Завершение модуля
@router.message(Day1Module1States.step_14, F.text.in_(["🌟 Супер", "🌬 Буду практиковать"]))
async def complete_day_1_module_1(message: Message, state: FSMContext):
    """Завершает модуль и переходит к следующему."""
    from handlers.course_flow import complete_module
    await state.clear()  # Очищаем состояние модуля
    await complete_module(message)  # Вызываем функцию завершения модуля

# Обработчики для кнопок навигации
@router.message(F.text == "🔄 Давай повторим")
async def repeat_day_1_module_1(message: Message, state: FSMContext):
    """Повторяет текущий модуль."""
    await start_day_1_module_1(message, state)

@router.message(F.text == "🏠 В основное меню")
async def back_to_main_menu_from_module(message: Message, state: FSMContext):
    """Возвращает в главное меню."""
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, message.from_user.id)