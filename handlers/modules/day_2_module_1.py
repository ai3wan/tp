# handlers/modules/day_2_module_1.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class Day2Module1States(StatesGroup):
    """Состояния для Дня 2, Модуля 1."""
    step_1 = State()  # Тревога в теле
    step_2 = State()  # Тело реагирует быстрее
    step_3 = State()  # Маскировка тревоги
    step_4 = State()  # Связь мыслей и тела
    step_5 = State()  # Прогрессивная релаксация
    step_6 = State()  # Практика кулаков
    step_7 = State()  # Практика плеч
    step_8 = State()  # Практика лица
    step_9 = State()  # Общее состояние
    step_10 = State()  # Доступность практики
    step_11 = State()  # Цель практики

def get_step_keyboard(step: int) -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру для конкретного шага диалога."""
    keyboards = {
        1: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💡 Тревога живёт в теле")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        2: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="⚡ Сначала реагирует тело")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        3: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🤸 Тревога — это зажимы")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        4: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔄 Круг тревоги")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        5: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🙌 Давай попробуем")],
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
        9: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔉 Тревога тише")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        10: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🚍 Можно делать везде")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        ),
        11: ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💪 Тренирую навык")],
                [KeyboardButton(text="🏠 В основное меню")]
            ],
            resize_keyboard=True
        )
    }
    return keyboards.get(step, ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True))

@router.message(F.text == "▶️ День 2, Модуль 1")
async def start_day_2_module_1(message: Message, state: FSMContext):
    """Запускает второй день, первый модуль."""
    await state.set_state(Day2Module1States.step_1)
    
    # Отправляем изображение с текстом (если файл существует)
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d2m1", "d2m1_1.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="👥 Сегодня речь пойдёт о том, что тревога живёт не только в голове, но и в теле.\n"
                    "Многие замечают: ком в горле, дрожь в руках, напряжённые плечи. Это не случайность.\n\n"
                    "<blockquote expandable>Когда мозг включает режим тревоги, активируется симпатическая нервная система. Она как «педаль газа» — сердце начинает биться чаще, дыхание ускоряется, мышцы напрягаются, готовясь к действию. Даже если действовать не требуется.\n\n"
                    "У наших предков это было жизненно важно: услышав шорох в кустах, тело напрягалось, готовясь к бегству. В современном мире угрозы чаще не физические, а социальные или воображаемые. Но тело реагирует так, будто впереди тигр.\n\n"
                    "Поэтому тревога ощущается телесно: затекшие плечи, сжатая челюсть, дрожь, холодок в животе. Это не болезнь, а естественная реакция организма, только немного неуместная в повседневности.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(1)
        )
    else:
        await message.answer(
            "👥 Сегодня речь пойдёт о том, что тревога живёт не только в голове, но и в теле.\n"
            "Многие замечают: ком в горле, дрожь в руках, напряжённые плечи. Это не случайность.\n\n"
            "<blockquote expandable>Когда мозг включает режим тревоги, активируется симпатическая нервная система. Она как «педаль газа» — сердце начинает биться чаще, дыхание ускоряется, мышцы напрягаются, готовясь к действию. Даже если действовать не требуется.\n\n"
            "У наших предков это было жизненно важно: услышав шорох в кустах, тело напрягалось, готовясь к бегству. В современном мире угрозы чаще не физические, а социальные или воображаемые. Но тело реагирует так, будто впереди тигр.\n\n"
            "Поэтому тревога ощущается телесно: затекшие плечи, сжатая челюсть, дрожь, холодок в животе. Это не болезнь, а естественная реакция организма, только немного неуместная в повседневности.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(1)
        )

# Шаг 1 -> Шаг 2
@router.message(Day2Module1States.step_1, F.text == "💡 Тревога живёт в теле")
async def step_1_to_2(message: Message, state: FSMContext):
    """Переход от шага 1 к шагу 2."""
    await state.set_state(Day2Module1States.step_2)
    
    # Отправляем изображение с текстом (если файл существует)
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d2m1", "d2m1_2.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="При тревоге тело реагирует быстрее, чем разум.\n"
                    "Сначала приходит телесный отклик — и лишь потом появляется мысль: «Кажется, я волнуюсь».\n\n"
                    "<blockquote expandable>Это связано с амигдалой — маленькой частью мозга, отвечающей за страх. Она работает быстрее сознания. Это как пожарная сигнализация: сначала орёт, а потом уже можно разбираться, где возгорание.\n\n"
                    "Сначала учащается сердцебиение, перехватывает дыхание, напрягаются мышцы. И только спустя секунду разум фиксирует: «Наверное, это тревога». Поэтому ощущение похоже на телесную бурю.\n\n"
                    "Такой порядок — эволюционная защита. Если бы древний человек сначала думал, а потом напрягал мышцы, он не успел бы убежать. Сегодня этот механизм часто мешает, потому что сигнал включается без реальной угрозы.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(2)
        )
    else:
        await message.answer(
            "При тревоге тело реагирует быстрее, чем разум.\n"
            "Сначала приходит телесный отклик — и лишь потом появляется мысль: «Кажется, я волнуюсь».\n\n"
            "<blockquote expandable>Это связано с амигдалой — маленькой частью мозга, отвечающей за страх. Она работает быстрее сознания. Это как пожарная сигнализация: сначала орёт, а потом уже можно разбираться, где возгорание.\n\n"
            "Сначала учащается сердцебиение, перехватывает дыхание, напрягаются мышцы. И только спустя секунду разум фиксирует: «Наверное, это тревога». Поэтому ощущение похоже на телесную бурю.\n\n"
            "Такой порядок — эволюционная защита. Если бы древний человек сначала думал, а потом напрягал мышцы, он не успел бы убежать. Сегодня этот механизм часто мешает, потому что сигнал включается без реальной угрозы.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(2)
        )

# Шаг 2 -> Шаг 3
@router.message(Day2Module1States.step_2, F.text == "⚡ Сначала реагирует тело")
async def step_2_to_3(message: Message, state: FSMContext):
    """Переход от шага 2 к шагу 3."""
    await state.set_state(Day2Module1States.step_3)
    
    # Отправляем изображение с текстом (если файл существует)
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d2m1", "d2m1_3.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="Иногда тревога маскируется: внешне всё спокойно, а тело уже сжалось.\n"
                    "Плечи подняты, кулаки напряжены, челюсти стиснуты.\n\n"
                    "<blockquote expandable>Это называется соматизацией — тревога выражается через телесные ощущения. Человек может не осознавать волнение, но тело хранит зажимы.\n\n"
                    "Самые «любимые» зоны тревоги — плечи и шея. Они поднимаются, словно защищают шею. Часто напрягаются челюсти, которые «сжимают зубы» от стресса. А ещё живот, где появляется тяжесть или спазм.\n\n"
                    "Хорошая новость в том, что, расслабив эти зоны, можно отправить в мозг сигнал: «опасности нет». Связь идёт в обе стороны — напряжение усиливает тревогу, а расслабление её гасит.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(3)
        )
    else:
        await message.answer(
            "Иногда тревога маскируется: внешне всё спокойно, а тело уже сжалось.\n"
            "Плечи подняты, кулаки напряжены, челюсти стиснуты.\n\n"
            "<blockquote expandable>Это называется соматизацией — тревога выражается через телесные ощущения. Человек может не осознавать волнение, но тело хранит зажимы.\n\n"
            "Самые «любимые» зоны тревоги — плечи и шея. Они поднимаются, словно защищают шею. Часто напрягаются челюсти, которые «сжимают зубы» от стресса. А ещё живот, где появляется тяжесть или спазм.\n\n"
            "Хорошая новость в том, что, расслабив эти зоны, можно отправить в мозг сигнал: «опасности нет». Связь идёт в обе стороны — напряжение усиливает тревогу, а расслабление её гасит.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(3)
        )

# Шаг 3 -> Шаг 4
@router.message(Day2Module1States.step_3, F.text == "🤸 Тревога — это зажимы")
async def step_3_to_4(message: Message, state: FSMContext):
    """Переход от шага 3 к шагу 4."""
    await state.set_state(Day2Module1States.step_4)
    
    # Отправляем изображение с текстом (если файл существует)
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d2m1", "d2m1_4.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="Мысли и тело связаны как два зеркала.\n"
                    "Напряжённые мысли делают мышцы жёсткими, а жёсткие мышцы усиливают тревожные мысли.\n\n"
                    "<blockquote expandable>Так формируется порочный круг: тревожная мысль вызывает напряжение в плечах → тело ощущает дискомфорт → мозг думает «тревога усиливается». И так по кругу.\n\n"
                    "Но работает и обратная связь: если расслабить тело, постепенно успокаиваются мысли. Это как повернуть ручку громкости на радио — сигнал становится тише.\n\n"
                    "Исследования показывают: телесные практики напрямую влияют на мозг. Даже простое расслабление челюстей или несколько медленных выдохов способны снизить активность амигдалы.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(4)
        )
    else:
        await message.answer(
            "Мысли и тело связаны как два зеркала.\n"
            "Напряжённые мысли делают мышцы жёсткими, а жёсткие мышцы усиливают тревожные мысли.\n\n"
            "<blockquote expandable>Так формируется порочный круг: тревожная мысль вызывает напряжение в плечах → тело ощущает дискомфорт → мозг думает «тревога усиливается». И так по кругу.\n\n"
            "Но работает и обратная связь: если расслабить тело, постепенно успокаиваются мысли. Это как повернуть ручку громкости на радио — сигнал становится тише.\n\n"
            "Исследования показывают: телесные практики напрямую влияют на мозг. Даже простое расслабление челюстей или несколько медленных выдохов способны снизить активность амигдалы.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(4)
        )

# Шаг 4 -> Шаг 5
@router.message(Day2Module1States.step_4, F.text == "🔄 Круг тревоги")
async def step_4_to_5(message: Message, state: FSMContext):
    """Переход от шага 4 к шагу 5."""
    await state.set_state(Day2Module1States.step_5)
    
    await message.answer(
        "Разорвать этот круг помогает практика под названием «прогрессивная мышечная релаксация».\n\n"
        "<blockquote expandable>Её разработал врач Эдмунд Джекобсон ещё в 1920-х. Он заметил: поочерёдное напряжение и расслабление мышц снижает уровень тревожности. Тело словно учится отпускать зажимы.\n\n"
        "Суть проста: напрячь конкретную группу мышц, удержать несколько секунд, а потом отпустить. Контраст делает расслабление ярче и заметнее.\n\n"
        "Мозг фиксирует: «мышцы мягкие — опасности нет». Со временем этот паттерн закрепляется, и организм переключается быстрее.</blockquote>",
        parse_mode="HTML",
        reply_markup=get_step_keyboard(5)
    )

# Шаг 5 -> Шаг 6
@router.message(Day2Module1States.step_5, F.text == "🙌 Давай попробуем")
async def step_5_to_6(message: Message, state: FSMContext):
    """Переход от шага 5 к шагу 6."""
    await state.set_state(Day2Module1States.step_6)
    
    # Отправляем видео с практикой (если файл существует)
    import os
    from aiogram.types import FSInputFile
    
    video_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "practices", "practice_2.mp4")
    
    if os.path.exists(video_path):
        video_file = FSInputFile(video_path)
        await message.answer_video(
            video=video_file,
            caption="Сейчас попробуем простую практику — поочерёдно напрягать и расслаблять разные части тела (кулаки, плечи, лицо). Это поможет почувствовать разницу между напряжением и покоем.\n\n"
                    "<blockquote expandable>Начнём с кулаков.\n"
                    "Сожми их как можно сильнее, почувствуй напряжение. Подержи пару секунд. Теперь отпусти. Заметь, как мышцы становятся мягкими.\n"
                    "Когда напряжение уходит, в мозг идёт сигнал: «опасности нет». Это снижает общий уровень тревоги.\n\n"
                    "Теперь перейдём к плечам.\n"
                    "Подними их к ушам, сильно напряги и задержи. А потом резко отпусти вниз.\n"
                    "Плечи — склад эмоций. Они автоматически поднимаются, словно защищают шею. Когда их расслабить, тревога снижается, словно с плеч сбросили невидимый рюкзак.\n\n"
                    "И напоследок — лицо.\n"
                    "Сожми челюсти, нахмурь брови, задержи. А потом отпусти и расслабь всё лицо.\n"
                    "Лицо тесно связано с эмоциями: напряжённые челюсти усиливают тревогу, а мягкое выражение даёт мозгу сигнал «всё в порядке».\n\n"
                    "Теперь сделай пару спокойных вдохов и выдохов. Обрати внимание: тело стало мягче, а дыхание спокойнее.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(6)
        )
    else:
        await message.answer(
            "Сейчас попробуем простую практику — поочерёдно напрягать и расслаблять разные части тела (кулаки, плечи, лицо). Это поможет почувствовать разницу между напряжением и покоем.\n\n"
            "<blockquote expandable>Начнём с кулаков.\n"
            "Сожми их как можно сильнее, почувствуй напряжение. Подержи пару секунд. Теперь отпусти. Заметь, как мышцы становятся мягкими.\n"
            "Когда напряжение уходит, в мозг идёт сигнал: «опасности нет». Это снижает общий уровень тревоги.\n\n"
            "Теперь перейдём к плечам.\n"
            "Подними их к ушам, сильно напряги и задержи. А потом резко отпусти вниз.\n"
            "Плечи — склад эмоций. Они автоматически поднимаются, словно защищают шею. Когда их расслабить, тревога снижается, словно с плеч сбросили невидимый рюкзак.\n\n"
            "И напоследок — лицо.\n"
            "Сожми челюсти, нахмурь брови, задержи. А потом отпусти и расслабь всё лицо.\n"
            "Лицо тесно связано с эмоциями: напряжённые челюсти усиливают тревогу, а мягкое выражение даёт мозгу сигнал «всё в порядке».\n\n"
            "Теперь сделай пару спокойных вдохов и выдохов. Обрати внимание: тело стало мягче, а дыхание спокойнее.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(6)
        )

# Шаг 6 -> Шаг 7 (первая кнопка)
@router.message(Day2Module1States.step_6, F.text == "✊ Кулаки расслаблены")
async def step_6_to_7(message: Message, state: FSMContext):
    """Переход от шага 6 к шагу 7."""
    await state.set_state(Day2Module1States.step_7)
    
    await message.answer(
        "Следующая остановка — плечи. Здесь тревога любит прятаться.",
        reply_markup=get_step_keyboard(7)
    )

# Шаг 7 -> Шаг 8 (вторая кнопка)
@router.message(Day2Module1States.step_7, F.text == "🎒 Напряжение сброшено")
async def step_7_to_8(message: Message, state: FSMContext):
    """Переход от шага 7 к шагу 8."""
    await state.set_state(Day2Module1States.step_8)
    
    await message.answer(
        "И наконец — лицо. Попробуй заметить и отпустить напряжение здесь.",
        reply_markup=get_step_keyboard(8)
    )

# Шаг 8 -> Шаг 9 (третья кнопка)
@router.message(Day2Module1States.step_8, F.text == "🙂 Лицо расслаблено")
async def step_8_to_9(message: Message, state: FSMContext):
    """Переход от шага 8 к шагу 9."""
    await state.set_state(Day2Module1States.step_9)
    
    await message.answer(
        "Теперь важно заметить общее состояние.\n"
        "После упражнений дыхание ровнее, тело мягче.\n\n"
        "<blockquote expandable>Прогрессивная релаксация работает как переключатель. Мышцы напрягаются и отпускаются, нервная система фиксирует контраст и быстрее переключается в режим покоя.\n\n"
        "Это репетиция: «опасность — безопасность». Чем чаще повторяется цикл, тем быстрее тело учится включать режим спокойствия.\n\n"
        "Со временем тревога уходит быстрее, а тело реже застревает в напряжении.</blockquote>",
        parse_mode="HTML",
        reply_markup=get_step_keyboard(9)
    )

# Шаг 9 -> Шаг 10
@router.message(Day2Module1States.step_9, F.text == "🔉 Тревога тише")
async def step_9_to_10(message: Message, state: FSMContext):
    """Переход от шага 9 к шагу 10."""
    await state.set_state(Day2Module1States.step_10)
    
    # Отправляем изображение с текстом (если файл существует)
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d2m1", "d2m1_7.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="Практика проста и доступна.\n"
                    "Её можно использовать в любой момент.\n\n"
                    "<blockquote expandable>Перед сном дома, во время паузы на работе, в транспорте — никаких условий не нужно, только внимание.\n\n"
                    "Регулярное использование помогает быстрее восстанавливаться после стрессов. Уровень кортизола снижается, тело легче отпускает напряжение.\n\n"
                    "Так формируется новый шаблон: вместо привычного зажима в ответ на тревогу возникает привычка расслабляться.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(10)
        )
    else:
        await message.answer(
            "Практика проста и доступна.\n"
            "Её можно использовать в любой момент.\n\n"
            "<blockquote expandable>Перед сном дома, во время паузы на работе, в транспорте — никаких условий не нужно, только внимание.\n\n"
            "Регулярное использование помогает быстрее восстанавливаться после стрессов. Уровень кортизола снижается, тело легче отпускает напряжение.\n\n"
            "Так формируется новый шаблон: вместо привычного зажима в ответ на тревогу возникает привычка расслабляться.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(10)
        )

# Шаг 10 -> Шаг 11
@router.message(Day2Module1States.step_10, F.text == "🚍 Можно делать везде")
async def step_10_to_11(message: Message, state: FSMContext):
    """Переход от шага 10 к шагу 11."""
    await state.set_state(Day2Module1States.step_11)
    
    # Отправляем изображение с текстом (если файл существует)
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d2m1", "d2m1_8.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="Важно помнить: цель не убрать тревогу навсегда.\n"
                    "Задача — научиться управлять её уровнем.\n\n"
                    "<blockquote expandable>Тревога — часть биологии. Но навык регулировки работает как тренировка в спортзале: каждое упражнение укрепляет «мышцу спокойствия».\n\n"
                    "Сначала результат заметен слегка, но с регулярной практикой привычка становится устойчивой.\n\n"
                    "Лучше по 2 минуты ежедневно, чем долго и редко. Постепенность эффективнее силы.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(11)
        )
    else:
        await message.answer(
            "Важно помнить: цель не убрать тревогу навсегда.\n"
            "Задача — научиться управлять её уровнем.\n\n"
            "<blockquote expandable>Тревога — часть биологии. Но навык регулировки работает как тренировка в спортзале: каждое упражнение укрепляет «мышцу спокойствия».\n\n"
            "Сначала результат заметен слегка, но с регулярной практикой привычка становится устойчивой.\n\n"
            "Лучше по 2 минуты ежедневно, чем долго и редко. Постепенность эффективнее силы.</blockquote>",
            parse_mode="HTML",
            reply_markup=get_step_keyboard(11)
        )

# Шаг 11 -> Завершение модуля
@router.message(Day2Module1States.step_11, F.text == "💪 Тренирую навык")
async def complete_day_2_module_1(message: Message, state: FSMContext):
    """Завершает второй день, первый модуль."""
    import database as db
    
    # Отправляем завершающее сообщение с изображением (если файл существует)
    import os
    from aiogram.types import FSInputFile
    
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "d2m1", "d2m1_9.jpg")
    
    if os.path.exists(image_path):
        image_file = FSInputFile(image_path)
        await message.answer_photo(
            photo=image_file,
            caption="Сегодня стало понятно: тревога живёт не только в голове, но и в теле.\n"
                    "И появился второй инструмент — прогрессивная мышечная релаксация.\n\n"
                    "<blockquote expandable>Теперь есть два приёма: дыхание и работа с мышцами. Это как маленькая «аптечка спокойствия».\n\n"
                    "Лучше всего работает сочетание: дыхание замедляет ритм, а релаксация снимает телесные зажимы. Вместе они дают больше эффекта.\n\n"
                    "Каждый такой шаг — вклад в привычку спокойствия. Формируется личный набор техник, которыми можно пользоваться в любых обстоятельствах.</blockquote>",
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "Сегодня стало понятно: тревога живёт не только в голове, но и в теле.\n"
            "И появился второй инструмент — прогрессивная мышечная релаксация.\n\n"
            "<blockquote expandable>Теперь есть два приёма: дыхание и работа с мышцами. Это как маленькая «аптечка спокойствия».\n\n"
            "Лучше всего работает сочетание: дыхание замедляет ритм, а релаксация снимает телесные зажимы. Вместе они дают больше эффекта.\n\n"
            "Каждый такой шаг — вклад в привычку спокойствия. Формируется личный набор техник, которыми можно пользоваться в любых обстоятельствах.</blockquote>",
            parse_mode="HTML"
        )
    
    # Обновляем закладку пользователя на следующий модуль
    user_id = message.from_user.id
    await db.update_user_bookmark(user_id, course_id=1, day=2, module=2)
    
    # Показываем главное меню с обновленным прогрессом
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, user_id)

# Обработчики для кнопки "В основное меню" для каждого состояния второго дня, первого модуля
@router.message(Day2Module1States.step_1, F.text == "🏠 В основное меню")
@router.message(Day2Module1States.step_2, F.text == "🏠 В основное меню")
@router.message(Day2Module1States.step_3, F.text == "🏠 В основное меню")
@router.message(Day2Module1States.step_4, F.text == "🏠 В основное меню")
@router.message(Day2Module1States.step_5, F.text == "🏠 В основное меню")
@router.message(Day2Module1States.step_6, F.text == "🏠 В основное меню")
@router.message(Day2Module1States.step_7, F.text == "🏠 В основное меню")
@router.message(Day2Module1States.step_8, F.text == "🏠 В основное меню")
@router.message(Day2Module1States.step_9, F.text == "🏠 В основное меню")
@router.message(Day2Module1States.step_10, F.text == "🏠 В основное меню")
@router.message(Day2Module1States.step_11, F.text == "🏠 В основное меню")
async def back_to_main_menu_from_module(message: Message, state: FSMContext):
    """Возвращает в главное меню."""
    from handlers.course_flow import show_main_menu
    await state.clear()
    await show_main_menu(message, message.from_user.id)
