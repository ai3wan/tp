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
    step_11 = State()  # Видео практики
    step_12 = State()  # Результат практики
    step_13 = State()  # Вывод и завершение

def get_step_keyboard(step: int) -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру для конкретного шага диалога."""
    keyboards = {
        1: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👍 Да, поехали")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        2: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🚨 Тревога как сигнализация")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        3: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👀 Опасность, где её нет")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        4: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="😅 Было такое")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        5: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💪 Тревога — не слабость")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        6: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🙃 Перебарщивает тревога")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        7: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🤔 Дружить с тревогой")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        8: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🌬️ Дыхание — инструмент")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        9: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔁 Замедлить дыхание")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        10: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="⏱️ Вдох 4 — выдох 6")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        11: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="😊 Стало спокойнее")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        12: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🌿 Лучше")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        13: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="⚖️ Тревога — просто сигнал")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        # Клавиатура для step_14 убрана, так как состояние больше не используется
    }
    return keyboards.get(step, ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True))

@router.message(F.text == "▶️ День 1, Модуль 1")
async def start_day_1_module_1(message: Message, state: FSMContext):
    """Запускает День 1, Модуль 1 - интерактивный диалог."""
    await state.set_state(Day1Module1States.step_1)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_1.jpg")
    image_file = FSInputFile(image_path)
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """Тревога — это как встроенный датчик дыма в доме. Он реагирует, когда что-то может пойти не так. Иногда сигнал слишком громкий или срабатывает не вовремя, но сам факт того, что он есть, — это благо. Представь себе дом без сигнализации — было бы опасно.

Нейробиологи объясняют тревогу через работу амигдалы — участка мозга, который первым «поднимает тревогу». Даже у самых уверенных людей амигдала активна, просто у них лучше развита способность её «успокаивать» с помощью префронтальной коры — той части мозга, которая отвечает за логику и контроль. Именно эту способность мы и будем тренировать."""
    
    main_text = "Привет 👋 Сегодня мы начинаем наш курс. Первое, что важно понять: тревога — это часть жизни каждого человека. Она бывает у всех, даже у самых уверенных людей. Готов узнать, как с ней обращаться?"
    
    full_caption = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    await message.answer_photo(
        photo=image_file,
        caption=full_caption,
        parse_mode="HTML",
        reply_markup=get_step_keyboard(1)
    )

# Шаг 1 -> Шаг 2
@router.message(Day1Module1States.step_1, F.text == "👍 Да, поехали")
async def step_1_to_2(message: Message, state: FSMContext):
    """Переход от шага 1 к шагу 2."""
    await state.set_state(Day1Module1States.step_2)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_2.jpg")
    image_file = FSInputFile(image_path)
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """Если рассматривать мозг как «центр управления полётами», то тревога — это радар. Он ловит малейшие сигналы об опасности и сообщает: «Внимание! Готовься к действию». Проблема в том, что этот радар не умеет отличать «птицу» от «ракеты» — и тревога включается даже тогда, когда угрозы нет.

Это объясняется тем, что эволюция «настроила» нас на избыточную осторожность. Наши предки, которые чаще тревожились и быстрее реагировали, имели больше шансов выжить. Поэтому современный мозг унаследовал эту гиперчувствительность. Хорошая новость в том, что сейчас мы можем её осознанно регулировать — у древнего человека такой возможности не было."""
    
    main_text = "Звучит странно, но тревога — не враг 😌 Она работает как сигнализация: громкая, навязчивая, но с одной целью — предупредить. Иногда эта «сигналка» срабатывает даже тогда, когда опасности нет."
    
    full_caption = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    await message.answer_photo(
        photo=image_file,
        caption=full_caption,
        parse_mode="HTML",
        reply_markup=get_step_keyboard(2)
    )

# Шаг 2 -> Шаг 3
@router.message(Day1Module1States.step_2, F.text == "🚨 Тревога как сигнализация")
async def step_2_to_3(message: Message, state: FSMContext):
    """Переход от шага 2 к шагу 3."""
    await state.set_state(Day1Module1States.step_3)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_3.jpg")
    image_file = FSInputFile(image_path)
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """Психологи называют это «ложными срабатываниями тревожной системы». В реальности социальные ситуации, вроде экзамена или знакомства с новым человеком, не несут физической угрозы. Но мозг воспринимает их как «опасность для статуса» — а для древнего человека потеря одобрения племени могла быть равна изгнанию, то есть угрозе жизни.

Поэтому реакция организма на презентацию перед коллегами может напоминать реакцию на встречу с медведем: учащённое сердцебиение, напряжённые мышцы, скачущие мысли. Научившись понимать природу этой реакции, мы можем перестать воспринимать её как «сбой» и начать использовать в свою пользу: например, энергия тревоги может помочь собраться и выступить ярко."""
    
    main_text = "Наш мозг создан, чтобы защищать нас 🧠 Он оценивает мир вокруг и ищет угрозы. Но иногда он видит опасность там, где её на самом деле нет — например, перед выступлением или важным разговором."
    
    full_caption = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    await message.answer_photo(
        photo=image_file,
        caption=full_caption,
        parse_mode="HTML",
        reply_markup=get_step_keyboard(3)
    )

# Шаг 3 -> Шаг 4
@router.message(Day1Module1States.step_3, F.text == "👀 Опасность, где её нет")
async def step_3_to_4(message: Message, state: FSMContext):
    """Переход от шага 3 к шагу 4."""
    await state.set_state(Day1Module1States.step_4)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_4.jpg")
    image_file = FSInputFile(image_path)
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """То, что ты чувствуешь, — это классическая активация симпатической нервной системы. Она разгоняет сердце и дыхание, чтобы тело получило больше энергии. Это древний механизм «бей или беги». Он задуман для физического действия, но в современном мире мы чаще остаёмся на месте и переживаем, не двигаясь.

Из-за этого возникает ощущение, что тело «сходит с ума», хотя на самом деле оно просто запасается силами. Если в этот момент подключить техники дыхания или движения, можно перенаправить энергию в нужное русло. Например, короткая разминка перед важным разговором или спокойное дыхание помогают «сбросить лишний пар»."""
    
    main_text = "Представь ситуацию: завтра собеседование. Всё идёт нормально, но сердце начинает биться быстрее ❤️‍🔥 ладони потеют, мысли скачут. Это не потому, что что-то плохое случилось — так тело готовит тебя к «битве»."
    
    full_caption = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    await message.answer_photo(
        photo=image_file,
        caption=full_caption,
        parse_mode="HTML",
        reply_markup=get_step_keyboard(4)
    )

# Шаг 4 -> Шаг 5
@router.message(Day1Module1States.step_4, F.text == "😅 Было такое")
async def step_4_to_5(message: Message, state: FSMContext):
    """Переход от шага 4 к шагу 5."""
    await state.set_state(Day1Module1States.step_5)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_5.jpg")
    image_file = FSInputFile(image_path)
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """Тревога часто воспринимается как «дефект характера», но на самом деле это базовый инструмент выживания. Она запускает гормональные и нейронные процессы, которые делают нас более внимательными и быстрыми. Это можно сравнить с предохранителем в электрической сети: он срабатывает не потому, что сеть плохая, а потому что защищает систему от перегрузки.

Современные исследования показывают: люди с повышенной тревожностью иногда даже выигрывают — у них выше чувствительность к изменениям, они лучше предугадывают риски. Важно лишь научиться управлять этим состоянием так, чтобы оно помогало, а не мешало."""
    
    main_text = "И вот главный момент 👉 тревога — это не признак слабости. Это просто сигнал: «Внимание, может быть что-то важное». Она пытается мобилизовать силы, даже если ситуация не такая уж и опасная."
    
    full_caption = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    await message.answer_photo(
        photo=image_file,
        caption=full_caption,
        parse_mode="HTML",
        reply_markup=get_step_keyboard(5)
    )

# Шаг 5 -> Шаг 6
@router.message(Day1Module1States.step_5, F.text == "💪 Тревога — не слабость")
async def step_5_to_6(message: Message, state: FSMContext):
    """Переход от шага 5 к шагу 6."""
    await state.set_state(Day1Module1States.step_6)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_6.jpg")
    image_file = FSInputFile(image_path)
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """Здесь снова играет роль амигдала — она запускает тревогу автоматически и очень громко. Но у нас есть «внутренний регулятор громкости» — префронтальная кора. Когда она активна, тревога снижается, и сигнал становится более реалистичным.

Представь себе радио, которое слишком громко играет. Вместо того чтобы ломать приёмник, достаточно повернуть ручку громкости. Навыки саморегуляции — дыхание, осознанность, переключение внимания — и есть такие «ручки», которые помогают вернуть баланс."""
    
    main_text = "Проблема в том, что тревога часто перебарщивает 🙃 Она включает режим «всё горит», когда достаточно было бы маленькой лампочки. Поэтому важно учиться регулировать её громкость."
    
    full_caption = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    await message.answer_photo(
        photo=image_file,
        caption=full_caption,
        parse_mode="HTML",
        reply_markup=get_step_keyboard(6)
    )

# Шаг 6 -> Шаг 7
@router.message(Day1Module1States.step_6, F.text == "🙃 Перебарщивает тревога")
async def step_6_to_7(message: Message, state: FSMContext):
    """Переход от шага 6 к шагу 7."""
    await state.set_state(Day1Module1States.step_7)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_7.jpg")
    image_file = FSInputFile(image_path)
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """Полностью избавиться от тревоги невозможно и не нужно — это всё равно что выдернуть сигнализацию из квартиры. Но можно научиться управлять ею так, чтобы она была помощником. Тревога подсказывает: «Здесь важно быть собранным». А мы решаем, насколько сильно реагировать.

Современная психология говорит: ключ — не в борьбе, а в принятии. Если относиться к тревоге как к гостю, которого можно пригласить за стол и выслушать, она перестаёт казаться врагом. Тогда легче переключиться с «паники» на «полезный сигнал»."""
    
    main_text = "И это хорошая новость 😊 Мы можем научиться дружить с тревогой. Не подавлять её, не гнать прочь, а относиться как к сигналу, который можно приглушить и направить в нужное русло."
    
    full_caption = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    await message.answer_photo(
        photo=image_file,
        caption=full_caption,
        parse_mode="HTML",
        reply_markup=get_step_keyboard(7)
    )

# Шаг 7 -> Шаг 8
@router.message(Day1Module1States.step_7, F.text == "🤔 Дружить с тревогой")
async def step_7_to_8(message: Message, state: FSMContext):
    """Переход от шага 7 к шагу 8."""
    await state.set_state(Day1Module1States.step_8)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_8.jpg")
    image_file = FSInputFile(image_path)
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """Когда дыхание становится медленным и глубоким, активируется парасимпатическая нервная система — та часть организма, которая отвечает за отдых и восстановление. Она как противовес тревоге: замедляет сердцебиение, снижает напряжение в мышцах, успокаивает мысли.

Учёные называют это «обратной связью тела и мозга». Мы не можем напрямую приказать амигдале «успокойся», но можем через дыхание дать сигнал: «Опасности нет, можно расслабиться». И мозг постепенно принимает этот сигнал."""
    
    main_text = "Первый способ регулировать тревогу — дыхание 🌬️ Это самый простой инструмент, который всегда с тобой. Через дыхание мы можем успокоить нервную систему и вернуть контроль над состоянием."
    
    full_caption = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    await message.answer_photo(
        photo=image_file,
        caption=full_caption,
        parse_mode="HTML",
        reply_markup=get_step_keyboard(8)
    )

# Шаг 8 -> Шаг 9
@router.message(Day1Module1States.step_8, F.text == "🌬️ Дыхание — инструмент")
async def step_8_to_9(message: Message, state: FSMContext):
    """Переход от шага 8 к шагу 9."""
    await state.set_state(Day1Module1States.step_9)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_9.jpg")
    image_file = FSInputFile(image_path)
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """Это замкнутый круг: тревога ускоряет дыхание, быстрое дыхание усиливает тревогу. Учёные называют это «физиологической петлёй». Но есть и обратная дорога: если замедлить дыхание, то цепочка разворачивается назад, и тревога начинает стихать.

Медленное дыхание работает как «тормоз» для нервной системы. Оно посылает сигнал в блуждающий нерв — важную «линию связи» между телом и мозгом. Этот нерв как переключатель переводит организм из режима тревоги в режим покоя."""
    
    main_text = "Заметь: когда ты тревожишься, дыхание становится быстрым и поверхностным. Это запускает цепочку «больше кислорода → быстрее сердце → сильнее тревога». Если дыхание замедлить, тревога снижается 🔇"
    
    full_caption = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    await message.answer_photo(
        photo=image_file,
        caption=full_caption,
        parse_mode="HTML",
        reply_markup=get_step_keyboard(9)
    )

# Шаг 9 -> Шаг 10
@router.message(Day1Module1States.step_9, F.text == "🔁 Замедлить дыхание")
async def step_9_to_10(message: Message, state: FSMContext):
    """Переход от шага 9 к шагу 10."""
    await state.set_state(Day1Module1States.step_10)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_10.jpg")
    image_file = FSInputFile(image_path)
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """Такой ритм не случайный. Более длинный выдох помогает активировать «тормозящую» систему организма. Во время выдоха сердце бьётся чуть медленнее, а мозг получает сигнал, что опасность миновала.

Эта техника используется даже в клиниках для снижения уровня тревожности. Она настолько проста, что подходит детям и взрослым, и её можно делать где угодно: на экзамене, в транспорте, перед важным звонком."""
    
    main_text = "Попробуем прямо сейчас 👌 Сделай вдох на 4 секунды, а выдох — на 6. Повтори два круга. Считай в уме или по пальцам — это помогает держать ритм."
    
    full_caption = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    await message.answer_photo(
        photo=image_file,
        caption=full_caption,
        parse_mode="HTML",
        reply_markup=get_step_keyboard(10)
    )

# Шаг 10 -> Шаг 11 (Видео практики)
@router.message(Day1Module1States.step_10, F.text == "⏱️ Вдох 4 — выдох 6")
async def step_10_to_11(message: Message, state: FSMContext):
    """Переход от шага 10 к шагу 11."""
    await state.set_state(Day1Module1States.step_11)
    
    # Отправляем видео с текстом
    import os
    from aiogram.types import FSInputFile
    
    video_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "practice_1.mp4")
    video_file = FSInputFile(video_path)
    
    await message.answer_video(
        video=video_file,
        caption="🧘 Первая практика курса — дыхание 4–6.\nСмотри на видео: 🔽 круг сужается — вдох, 🔼 расширяется — выдох.\n⏱ Подыши так несколько минут с таймером.",
        reply_markup=get_step_keyboard(11)
    )

# Шаг 11 -> Шаг 12 (Результат практики)
@router.message(Day1Module1States.step_11, F.text == "😊 Стало спокойнее")
async def step_11_to_12(message: Message, state: FSMContext):
    """Переход от шага 11 к шагу 12."""
    await state.set_state(Day1Module1States.step_12)
    
    # Отправляем картинку с текстом
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d1m1_11.jpg")
    image_file = FSInputFile(image_path)
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """То, что ты ощущаешь, связано с переключением нервной системы. Сердце замедляется, мышцы получают меньше сигналов «готовься к бою», а мозг переключается на более спокойный режим работы. Это похоже на то, как компьютер перестаёт «шуметь» и перегреваться, когда снижается нагрузка.

Учёные подтверждают: даже несколько циклов дыхания способны снизить уровень кортизола — гормона стресса. И если практиковать это регулярно, организм становится более устойчивым к будущим стрессам."""
    
    main_text = "Хорошо 👏 Обрати внимание: после этих нескольких дыханий тело чуть расслабляется, мысли становятся спокойнее. Это простой, но мощный способ «снизить громкость» тревоги."
    
    full_caption = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    await message.answer_photo(
        photo=image_file,
        caption=full_caption,
        parse_mode="HTML",
        reply_markup=get_step_keyboard(12)
    )

# Шаг 12 -> Шаг 13 (Вывод)
@router.message(Day1Module1States.step_12, F.text == "🌿 Лучше")
async def step_12_to_13(message: Message, state: FSMContext):
    """Переход от шага 12 к шагу 13."""
    await state.set_state(Day1Module1States.step_13)
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """Важно помнить: тревога — это не болезнь, а естественная реакция организма. Но у нас есть возможность влиять на её интенсивность. Дыхание — один из самых универсальных инструментов, потому что оно связано напрямую с работой мозга.

Каждый раз, когда ты используешь дыхательные практики, ты тренируешь «мышцу спокойствия» — способность управлять своим состоянием. Со временем это становится привычкой, и тревога уже не управляет тобой, а ты управляешь ею."""
    
    main_text = "Итак, вывод: тревога сама по себе не опасна, она лишь сигнал. Но у тебя есть инструмент — дыхание. Ты можешь использовать его всегда, когда тревога слишком настойчива."
    
    full_message = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    await message.answer(
        text=full_message,
        parse_mode="HTML",
        reply_markup=get_step_keyboard(13)
    )

# Шаг 13 -> Шаг 14 (Мотивация)
@router.message(Day1Module1States.step_13, F.text == "⚖️ Тревога — просто сигнал")
async def complete_day_1_module_1(message: Message, state: FSMContext):
    """Завершает первый модуль."""
    import database as db
    
    # Создаем сообщение с разворачивающейся цитатой
    quote_text = """Мозг учится через повторение. Когда мы регулярно возвращаемся к дыхательным практикам, создаются новые нейронные связи. Это как протаптывать тропинку в лесу: сначала трудно и непривычно, но потом путь становится лёгким и естественным.

Современные исследования показывают, что даже 5–10 минут регулярной практики способны изменить работу нервной системы: человек быстрее замечает тревогу и легче её снижает. Это не «разовый трюк», а навык, который постепенно становится частью тебя."""
    
    main_text = "Сегодня мы ещё дважды вернёмся к этой практике: 🌞 днём и 🌙 вечером.\nЧем чаще будешь пробовать, тем привычнее станет регулировать своё состояние ⚖️✨"
    
    full_message = f"{main_text}\n\n<blockquote expandable>{quote_text}</blockquote>"
    
    # Отправляем завершающее сообщение
    await message.answer(
        text=full_message,
        parse_mode="HTML"
    )
    
    # Обновляем закладку пользователя на следующий модуль
    user_id = message.from_user.id
    await db.update_user_bookmark(user_id, course_id=1, day=1, module=2)
    
    # Показываем главное меню с обновленным прогрессом
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, user_id)

# Функция завершения модуля перенесена в step_13_to_14

# Обработчики для кнопок навигации

# Обработчики для кнопки "В основное меню" для каждого состояния первого модуля
@router.message(Day1Module1States.step_1, F.text == "🏠 В основное меню")
@router.message(Day1Module1States.step_2, F.text == "🏠 В основное меню")
@router.message(Day1Module1States.step_3, F.text == "🏠 В основное меню")
@router.message(Day1Module1States.step_4, F.text == "🏠 В основное меню")
@router.message(Day1Module1States.step_5, F.text == "🏠 В основное меню")
@router.message(Day1Module1States.step_6, F.text == "🏠 В основное меню")
@router.message(Day1Module1States.step_7, F.text == "🏠 В основное меню")
@router.message(Day1Module1States.step_8, F.text == "🏠 В основное меню")
@router.message(Day1Module1States.step_9, F.text == "🏠 В основное меню")
@router.message(Day1Module1States.step_10, F.text == "🏠 В основное меню")
@router.message(Day1Module1States.step_11, F.text == "🏠 В основное меню")
@router.message(Day1Module1States.step_12, F.text == "🏠 В основное меню")
@router.message(Day1Module1States.step_13, F.text == "🏠 В основное меню")
# Обработчик для step_14 убран, так как состояние больше не используется
async def back_to_main_menu_from_module(message: Message, state: FSMContext):
    """Возвращает в главное меню."""
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, message.from_user.id)