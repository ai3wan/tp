import asyncpg
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import database as db
from handlers.course_flow import show_main_menu
from FSM.states import AnxietyTest

# 1. Отдельный роутер для этого теста
router = Router()


# 3. Словарь для подсчета баллов
# Ключ - текст ответа, значение - балл
ANSWER_SCORES = {
    # 0 баллов
    "🌤 Никогда": 0, "🌙 Легко засыпаю и сплю спокойно": 0, "🌿 Никогда": 0, "🌞 Редко или никогда": 0, "❌ Никогда": 0, "🍀 Редко": 0, "🏆 Легко": 0, "🧘 Спокойно, ищу решение": 0, "🟢 Редко или никогда": 0, "🌞 Никогда": 0, "🥇 Полностью уверен(а)": 0,
    # 1 балл
    "🌦 Иногда, но быстро проходит": 1, "😌 Иногда долго засыпаю или просыпаюсь ночью": 1, "🍃 Иногда, но быстро отпускает": 1, "🌤 Иногда, но не зацикливаюсь": 1, "🌬 Иногда, но быстро проходит": 1, "🌿 Иногда": 1, "🎈 Иногда отвлекаюсь": 1, "🙂 Немного переживаю, но быстро действую": 1, "🟡 Иногда": 1, "🌤 Иногда": 1, "🥈 В основном уверен(а)": 1,
    # 2 балла
    "🌧 Часто, но не мешает жить": 2, "😕 Засыпаю с трудом, сон поверхностный": 2, "🌾 Часто, но терпимо": 2, "🌧 Часто, и они крутятся в голове": 2, "💓 Часто при стрессе": 2, "🔥 Часто": 2, "🎭 Сильно отвлекаюсь": 2, "😰 Сильно переживаю, сложно начать действовать": 2, "🟠 Часто": 2, "🌦 Часто": 2, "🥉 Не всегда уверен(а)": 2,
    # 3 балла
    "⛈ Почти постоянно, мешает сосредоточиться": 3, "😣 Почти каждую ночь мучаюсь от плохого сна": 3, "🪨 Постоянно, это мешает расслабиться": 3, "⛈ Почти постоянно, мешает жить": 3, "💢 Почти всегда, когда тревожно": 3, "🌪 Почти всегда": 3, "🚫 Не могу сосредоточиться совсем": 3, "😱 Паника или ступор": 3, "🔴 Почти всегда": 3, "🌪 Постоянно": 3, "🪨 Почти всегда": 3, "🚫 Почти не уверен(а)": 3
}

# 4. Клавиатуры для каждого вопроса
q1_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🌤 Никогда", "🌦 Иногда, но быстро проходит", "🌧 Часто, но не мешает жить", "⛈ Почти постоянно, мешает сосредоточиться"]], resize_keyboard=True)
q2_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🌙 Легко засыпаю и сплю спокойно", "😌 Иногда долго засыпаю или просыпаюсь ночью", "😕 Засыпаю с трудом, сон поверхностный", "😣 Почти каждую ночь мучаюсь от плохого сна"]], resize_keyboard=True)
q3_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🌿 Никогда", "🍃 Иногда, но быстро отпускает", "🌾 Часто, но терпимо", "🪨 Постоянно, это мешает расслабиться"]], resize_keyboard=True)
q4_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🌞 Редко или никогда", "🌤 Иногда, но не зацикливаюсь", "🌧 Часто, и они крутятся в голове", "⛈ Почти постоянно, мешает жить"]], resize_keyboard=True)
q5_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["❌ Никогда", "🌬 Иногда, но быстро проходит", "💓 Часто при стрессе", "💢 Почти всегда, когда тревожно"]], resize_keyboard=True)
q6_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🍀 Редко", "🌿 Иногда", "🔥 Часто", "🌪 Почти всегда"]], resize_keyboard=True)
q7_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🏆 Легко", "🎈 Иногда отвлекаюсь", "🎭 Сильно отвлекаюсь", "🚫 Не могу сосредоточиться совсем"]], resize_keyboard=True)
q8_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🧘 Спокойно, ищу решение", "🙂 Немного переживаю, но быстро действую", "😰 Сильно переживаю, сложно начать действовать", "😱 Паника или ступор"]], resize_keyboard=True)
q9_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🟢 Редко", "🟡 Иногда", "🟠 Часто", "🔴 Почти всегда"]], resize_keyboard=True)
q10_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🌞 Никогда", "🌤 Иногда", "🌦 Часто", "🌪 Постоянно"]], resize_keyboard=True)
q11_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🌿 Никогда", "🍃 Иногда", "🌾 Часто", "🪨 Почти всегда"]], resize_keyboard=True)
q12_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🥇 Полностью уверен(а)", "🥈 В основном уверен(а)", "🥉 Не всегда уверен(а)", "🚫 Почти не уверен(а)"]], resize_keyboard=True)
q13_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["❌ Никогда", "🌤 Иногда", "🌧 Часто", "⛈ Почти всегда"]], resize_keyboard=True)
q14_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🟢 Редко или никогда", "🟡 Иногда", "🟠 Часто", "🔴 Почти всегда"]], resize_keyboard=True)

# 5. Точка входа, которую будет вызывать наш диспетчер
async def start_anxiety_test(message: Message, state: FSMContext):
    """Начинает начальный тест на тревожность."""
    await state.set_state(AnxietyTest.intro)
    # Сохраняем в FSM, какой тип теста мы проходим
    await state.update_data(test_type='initial')
    await message.answer(
        "Этот короткий опрос поможет понять, какой у тебя сейчас уровень тревожности.\n"
        "Он займёт всего 3–4 минуты и даст отправную точку — чтобы после курса ты увидишь свой прогресс.\n\n"
        "**📌 Как проходить тест**\n\n"
        "Отвечай честно, опираясь на свои чувства за последние 7 дней.\n"
        "Здесь нет правильных или неправильных ответов — это про тебя и твои ощущения.\n"
        "После курса мы повторим тест и сравним результаты.\n\n"
        "Начнем? 💙",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Вперед! 💙")],
            [KeyboardButton(text="Пока не хочу")]
        ], resize_keyboard=True)
    )
    
async def start_anxiety_final_test(message: Message, state: FSMContext):
    """Начинает ФИНАЛЬНЫЙ тест на тревожность."""
    # Используем тот же самый стейт
    await state.set_state(AnxietyTest.intro)
    # Но в FSM сохраняем другой тип теста
    await state.update_data(test_type='final')
    await message.answer(
        "Поздравляем с завершением основной части курса! 🥳\n\n"
        "Теперь давай повторим тот же опрос, чтобы наглядно увидеть твой прогресс.\n\n"
        "Отвечай так же честно, опираясь на свои ощущения за последние 7 дней.\n\n"
        "Готов(а) увидеть результат своей работы? 💙",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Вперед! 💙")],
            [KeyboardButton(text="Пока не хочу")]
        ], resize_keyboard=True)
    )

# 6. Цепочка обработчиков для опросника
# Теперь фильтр работает только на один стейт
@router.message(AnxietyTest.intro, F.text == "Пока не хочу")
async def abort_assessment(message: Message, state: FSMContext, pool: asyncpg.Pool):
    await state.clear()
    await message.answer("Хорошо, можешь пройти тест в любое время.", reply_markup=ReplyKeyboardRemove())
    await show_main_menu(message, message.from_user.id, pool)

# Фильтр также работает только на один стейт
@router.message(AnxietyTest.intro, F.text == "Вперед! 💙")
async def q1_handler(message: Message, state: FSMContext):
    await state.set_state(AnxietyTest.q1)
    await state.update_data(score=0)
    await message.answer("1. Как часто в последнее время ты ощущаешь волнение или беспокойство без причины? 😟", reply_markup=q1_kb)

# Универсальная функция для обработки ответов, чтобы не дублировать код
async def process_answer(message: Message, state: FSMContext, next_state: State, question_text: str, keyboard: ReplyKeyboardMarkup):
    data = await state.get_data()
    score = data.get('score', 0) + ANSWER_SCORES.get(message.text, 0)
    await state.update_data(score=score)
    await state.set_state(next_state)
    await message.answer(question_text, reply_markup=keyboard)

@router.message(AnxietyTest.q1)
async def q2_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q2, "2. Как ты спишь? 😴", q2_kb)

@router.message(AnxietyTest.q2)
async def q3_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q3, "3. Бывает ли у тебя напряжение в теле (плечи, шея, челюсти) без физической причины? 💆", q3_kb)

@router.message(AnxietyTest.q3)
async def q4_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q4, "4. Как часто у тебя возникают тревожные мысли о будущем? 🔮", q4_kb)

@router.message(AnxietyTest.q4)
async def q5_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q5, "5. Замечаешь ли ты учащённое сердцебиение, дрожь или потливость, когда тревожно? ❤️‍🔥", q5_kb)

@router.message(AnxietyTest.q5)
async def q6_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q6, "6. Как часто ты испытываешь раздражительность или вспышки гнева без серьёзной причины? 😠", q6_kb)

@router.message(AnxietyTest.q6)
async def q7_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q7, "7. Можешь ли ты спокойно сосредоточиться на задаче, когда вокруг стресс? 🎯", q7_kb)

@router.message(AnxietyTest.q7)
async def q8_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q8, "8. Как ты реагируешь на неожиданные трудности? 🚧", q8_kb)

@router.message(AnxietyTest.q8)
async def q9_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q9, "9. Часто ли ты избегаешь ситуаций, которые могут вызвать стресс или волнение? 🛑", q9_kb)

@router.message(AnxietyTest.q9)
async def q10_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q10, "10. Чувствуешь ли ты, что тревога мешает тебе отдыхать и наслаждаться жизнью? 🌴", q10_kb)

@router.message(AnxietyTest.q10)
async def q11_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q11, "11. Замечаешь ли ты, что тревога влияет на твоё здоровье (головные боли, желудок, усталость)? 💊", q11_kb)

@router.message(AnxietyTest.q11)
async def q12_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q12, "12. Насколько ты уверен(а) в своих силах справляться с трудностями? 💪", q12_kb)

@router.message(AnxietyTest.q12)
async def q13_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q13, "13. Как часто у тебя бывают трудности с дыханием или ощущение, что “не хватает воздуха” при тревоге? 🌬", q13_kb)

@router.message(AnxietyTest.q13)
async def q14_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q14, "14. Как часто тебе нужна поддержка других, чтобы успокоиться? 🤝", q14_kb)

@router.message(AnxietyTest.q14)
async def q15_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    score = data.get('score', 0) + ANSWER_SCORES.get(message.text, 0)
    await state.update_data(score=score)
    await state.set_state(AnxietyTest.q15)
    await message.answer(
        "15. И последний вопрос: если оценить свою тревожность по шкале от 0 до 10, какой балл ты поставишь? 📊\nПросто отправь цифру.",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(AnxietyTest.q15, F.text.regexp(r'^\d+$'))
async def assessment_final(message: Message, state: FSMContext, pool: asyncpg.Pool):
    self_assessment = int(message.text)
    if not (0 <= self_assessment <= 10):
        await message.answer("Пожалуйста, введи число от 0 до 10.")
        return

    data = await state.get_data()
    score = data.get('score', 0)
    # Получаем тип теста, по умолчанию 'initial', если вдруг что-то пошло не так
    test_type = data.get('test_type', 'initial')

    result_text = ""
    if 0 <= score <= 13:
        result_text = "🟢 **Низкий уровень тревожности.**\nТвои реакции на стресс в пределах нормы. Этот курс поможет тебе закрепить полезные привычки и станет отличной профилактикой."
    elif 14 <= score <= 26:
        result_text = "🟡 **Средний уровень тревожности.**\nТы замечаешь, что тревога влияет на твою жизнь. Этот курс идеально подходит, чтобы научиться техникам расслабления и контроля над мыслями, которые помогут тебе почувствовать себя лучше."
    else:
        result_text = "🔴 **Высокий уровень тревожности.**\nТревога доставляет тебе значительный дискомфорт. Практики из этого курса дадут тебе рабочие инструменты для снижения её уровня. Помни, что при высокой тревожности также очень полезна консультация со специалистом."

    bookmark = await db.get_user_bookmark(pool, message.from_user.id)
    # Используем test_type для сохранения правильного типа результата
    await db.save_assessment_result(
        pool=pool,
        user_id=message.from_user.id,
        course_id=bookmark['current_course_id'],
        assessment_type=test_type,
        score=score,
        self_assessment=self_assessment
    )

    await message.answer(f"Спасибо за честные ответы! Твой результат:\n\n{result_text}")

    # Завершаем FSM
    await state.clear()

    # В зависимости от типа теста, показываем разное сообщение
    if test_type == 'initial':
        # Для начального теста - сбрасываем прогресс на начало и зовем на первый урок
        await db.update_user_bookmark(pool, message.from_user.id, bookmark['current_course_id'], 1, 1)
        await message.answer("Отлично! Мы определили отправную точку. А теперь давай начнём наш первый урок!")
    else: # final
        # Для финального теста - просто поздравляем
        await message.answer("Поздравляем с прохождением финальной оценки! Надеемся, курс был для тебя полезен. 💙")

    # В любом случае показываем главное меню
    await show_main_menu(message, message.from_user.id, pool)


# --- Обработчик для некорректных ответов в тесте ---
# Он должен быть последним, чтобы не перехватывать правильные ответы
@router.message(
    StateFilter(
        AnxietyTest.q1, AnxietyTest.q2, AnxietyTest.q3, AnxietyTest.q4,
        AnxietyTest.q5, AnxietyTest.q6, AnxietyTest.q7, AnxietyTest.q8,
        AnxietyTest.q9, AnxietyTest.q10, AnxietyTest.q11, AnxietyTest.q12,
        AnxietyTest.q13, AnxietyTest.q14
    )
)
async def incorrect_test_answer(message: Message):
    """Ловит любой текст, который не попал в хендлеры выше."""
    await message.answer("Пожалуйста, выберите один из вариантов ответа, используя кнопки.")