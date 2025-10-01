# handlers/assessments/anxiety_test.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import database as db
from handlers.course_flow import show_main_menu

# Отдельный роутер для начального теста
router = Router()

# FSM-группа для начального теста
class AnxietyTest(StatesGroup):
    intro = State()
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    q9 = State()
    q10 = State()
    q11 = State()
    q12 = State()
    q13 = State()
    q14 = State()
    q15 = State()

# Словарь для подсчета баллов
ANSWER_SCORES = {
    # 0 баллов
    "🌤 Никогда": 0, "🌙 Легко засыпаю и сплю спокойно": 0, "🌿 Никогда": 0, "🌞 Редко или никогда": 0, "❌ Никогда": 0, "🍀 Редко": 0, "🏆 Легко": 0, "🧘 Спокойно, ищу решение": 0, "🟢 Редко или никогда": 0, "🟢 Редко": 0, "🌞 Никогда": 0, "🥇 Полностью уверен(а)": 0,
    # 1 балл
    "🌦 Иногда, но быстро проходит": 1, "😌 Иногда долго засыпаю или просыпаюсь ночью": 1, "🍃 Иногда, но быстро отпускает": 1, "🌤 Иногда, но не зацикливаюсь": 1, "🌬 Иногда, но быстро проходит": 1, "🌿 Иногда": 1, "🎈 Иногда отвлекаюсь": 1, "🙂 Немного переживаю, но быстро действую": 1, "🟡 Иногда": 1, "🌤 Иногда": 1, "🥈 В основном уверен(а)": 1, "🍃 Иногда": 1,
    # 2 балла
    "🌧 Часто, но не мешает жить": 2, "😕 Засыпаю с трудом, сон поверхностный": 2, "🌾 Часто, но терпимо": 2, "🌧 Часто, и они крутятся в голове": 2, "💓 Часто при стрессе": 2, "🔥 Часто": 2, "🎭 Сильно отвлекаюсь": 2, "😰 Сильно переживаю, сложно начать действовать": 2, "🟠 Часто": 2, "🌦 Часто": 2, "🥉 Не всегда уверен(а)": 2, "🌾 Часто": 2, "🌧 Часто": 2,
    # 3 балла
    "⛈ Почти постоянно, мешает сосредоточиться": 3, "😣 Почти каждую ночь мучаюсь от плохого сна": 3, "🪨 Постоянно, это мешает расслабиться": 3, "⛈ Почти постоянно, мешает жить": 3, "💢 Почти всегда, когда тревожно": 3, "🌪 Почти всегда": 3, "🚫 Не могу сосредоточиться совсем": 3, "😱 Паника или ступор": 3, "🔴 Почти всегда": 3, "🌪 Постоянно": 3, "🪨 Почти всегда": 3, "🚫 Почти не уверен(а)": 3, "⛈ Почти всегда": 3
}

# Инлайн клавиатуры для каждого вопроса
def get_q1_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌤 Никогда", callback_data="ans_🌤 Никогда")],
        [InlineKeyboardButton(text="🌦 Иногда, но быстро проходит", callback_data="ans_🌦 Иногда, но быстро проходит")],
        [InlineKeyboardButton(text="🌧 Часто, но не мешает жить", callback_data="ans_🌧 Часто, но не мешает жить")],
        [InlineKeyboardButton(text="⛈ Почти постоянно, мешает сосредоточиться", callback_data="ans_⛈ Почти постоянно, мешает сосредоточиться")]
    ])

def get_q2_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌙 Легко засыпаю и сплю спокойно", callback_data="ans_🌙 Легко засыпаю и сплю спокойно")],
        [InlineKeyboardButton(text="😌 Иногда долго засыпаю или просыпаюсь ночью", callback_data="ans_😌 Иногда долго засыпаю или просыпаюсь ночью")],
        [InlineKeyboardButton(text="😕 Засыпаю с трудом, сон поверхностный", callback_data="ans_😕 Засыпаю с трудом, сон поверхностный")],
        [InlineKeyboardButton(text="😣 Почти каждую ночь мучаюсь от плохого сна", callback_data="ans_😣 Почти каждую ночь мучаюсь от плохого сна")]
    ])

def get_q3_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌿 Никогда", callback_data="ans_🌿 Никогда")],
        [InlineKeyboardButton(text="🍃 Иногда, но быстро отпускает", callback_data="ans_🍃 Иногда, но быстро отпускает")],
        [InlineKeyboardButton(text="🌾 Часто, но терпимо", callback_data="ans_🌾 Часто, но терпимо")],
        [InlineKeyboardButton(text="🪨 Постоянно, это мешает расслабиться", callback_data="ans_🪨 Постоянно, это мешает расслабиться")]
    ])

def get_q4_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌞 Редко или никогда", callback_data="ans_🌞 Редко или никогда")],
        [InlineKeyboardButton(text="🌤 Иногда, но не зацикливаюсь", callback_data="ans_🌤 Иногда, но не зацикливаюсь")],
        [InlineKeyboardButton(text="🌧 Часто, и они крутятся в голове", callback_data="ans_🌧 Часто, и они крутятся в голове")],
        [InlineKeyboardButton(text="⛈ Почти постоянно, мешает жить", callback_data="ans_⛈ Почти постоянно, мешает жить")]
    ])

def get_q5_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Никогда", callback_data="ans_❌ Никогда")],
        [InlineKeyboardButton(text="🌬 Иногда, но быстро проходит", callback_data="ans_🌬 Иногда, но быстро проходит")],
        [InlineKeyboardButton(text="💓 Часто при стрессе", callback_data="ans_💓 Часто при стрессе")],
        [InlineKeyboardButton(text="💢 Почти всегда, когда тревожно", callback_data="ans_💢 Почти всегда, когда тревожно")]
    ])

def get_q6_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍀 Редко", callback_data="ans_🍀 Редко")],
        [InlineKeyboardButton(text="🌿 Иногда", callback_data="ans_🌿 Иногда")],
        [InlineKeyboardButton(text="🔥 Часто", callback_data="ans_🔥 Часто")],
        [InlineKeyboardButton(text="🌪 Почти всегда", callback_data="ans_🌪 Почти всегда")]
    ])

def get_q7_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 Легко", callback_data="ans_🏆 Легко")],
        [InlineKeyboardButton(text="🎈 Иногда отвлекаюсь", callback_data="ans_🎈 Иногда отвлекаюсь")],
        [InlineKeyboardButton(text="🎭 Сильно отвлекаюсь", callback_data="ans_🎭 Сильно отвлекаюсь")],
        [InlineKeyboardButton(text="🚫 Не могу сосредоточиться совсем", callback_data="ans_🚫 Не могу сосредоточиться совсем")]
    ])

def get_q8_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧘 Спокойно, ищу решение", callback_data="ans_🧘 Спокойно, ищу решение")],
        [InlineKeyboardButton(text="🙂 Немного переживаю, но быстро действую", callback_data="ans_🙂 Немного переживаю, но быстро действую")],
        [InlineKeyboardButton(text="😰 Сильно переживаю, сложно начать действовать", callback_data="ans_😰 Сильно переживаю, сложно начать действовать")],
        [InlineKeyboardButton(text="😱 Паника или ступор", callback_data="ans_😱 Паника или ступор")]
    ])

def get_q9_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Редко", callback_data="ans_🟢 Редко")],
        [InlineKeyboardButton(text="🟡 Иногда", callback_data="ans_🟡 Иногда")],
        [InlineKeyboardButton(text="🟠 Часто", callback_data="ans_🟠 Часто")],
        [InlineKeyboardButton(text="🔴 Почти всегда", callback_data="ans_🔴 Почти всегда")]
    ])

def get_q10_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Редко или никогда", callback_data="ans_🟢 Редко или никогда")],
        [InlineKeyboardButton(text="🟡 Иногда", callback_data="ans_🟡 Иногда")],
        [InlineKeyboardButton(text="🟠 Часто", callback_data="ans_🟠 Часто")],
        [InlineKeyboardButton(text="🔴 Почти всегда", callback_data="ans_🔴 Почти всегда")]
    ])

def get_q11_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌞 Никогда", callback_data="ans_🌞 Никогда")],
        [InlineKeyboardButton(text="🌤 Иногда", callback_data="ans_🌤 Иногда")],
        [InlineKeyboardButton(text="🌦 Часто", callback_data="ans_🌦 Часто")],
        [InlineKeyboardButton(text="🌪 Постоянно", callback_data="ans_🌪 Постоянно")]
    ])

def get_q12_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🥇 Полностью уверен(а)", callback_data="ans_🥇 Полностью уверен(а)")],
        [InlineKeyboardButton(text="🥈 В основном уверен(а)", callback_data="ans_🥈 В основном уверен(а)")],
        [InlineKeyboardButton(text="🥉 Не всегда уверен(а)", callback_data="ans_🥉 Не всегда уверен(а)")],
        [InlineKeyboardButton(text="🚫 Почти не уверен(а)", callback_data="ans_🚫 Почти не уверен(а)")]
    ])

def get_q13_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Никогда", callback_data="ans_❌ Никогда")],
        [InlineKeyboardButton(text="🌤 Иногда", callback_data="ans_🌤 Иногда")],
        [InlineKeyboardButton(text="🌧 Часто", callback_data="ans_🌧 Часто")],
        [InlineKeyboardButton(text="⛈ Почти всегда", callback_data="ans_⛈ Почти всегда")]
    ])

def get_q14_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Редко или никогда", callback_data="ans_🟢 Редко или никогда")],
        [InlineKeyboardButton(text="🟡 Иногда", callback_data="ans_🟡 Иногда")],
        [InlineKeyboardButton(text="🟠 Часто", callback_data="ans_🟠 Часто")],
        [InlineKeyboardButton(text="🔴 Почти всегда", callback_data="ans_🔴 Почти всегда")]
    ])

# Функция для обработки ответов
async def process_answer(callback: CallbackQuery, state: FSMContext, next_state, question_text: str, next_kb_func):
    """Обрабатывает ответ пользователя и переходит к следующему вопросу."""
    answer_text = callback.data.replace("ans_", "")
    score = ANSWER_SCORES.get(answer_text, 0)
    
    data = await state.get_data()
    total_score = data.get('score', 0) + score
    await state.update_data(score=total_score)
    
    await callback.answer()
    await callback.message.edit_text(question_text, reply_markup=next_kb_func())

# Точка входа для начального теста
async def start_anxiety_test(message: Message, state: FSMContext):
    """Начинает начальный пульс тревожности."""
    await state.set_state(AnxietyTest.intro)
    await message.answer(
        "Отлично! Давай определим твою отправную точку.\n\n"
        "Это поможет нам понять, как лучше всего поддержать тебя в процессе работы с тревожностью.\n\n"
        "Отвечай честно, опираясь на свои ощущения за последние 7 дней.\n\n"
        "Готов(а) начать? 💙",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Вперед! 💙", callback_data="start_test")],
            [InlineKeyboardButton(text="Пока не хочу", callback_data="abort_test")]
        ])
    )

# Обработчики для начального теста
@router.callback_query(F.data == "abort_test")
async def abort_assessment(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Хорошо, можешь пройти пульс тревожности в любое время.")
    await show_main_menu(callback.message, callback.from_user.id)

@router.callback_query(F.data == "start_test")
async def q1_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AnxietyTest.q1)
    await state.update_data(score=0)
    await callback.answer()
    await callback.message.edit_text(
        "Как часто в последнее время ты ощущаешь волнение или беспокойство без причины? 😟", 
        reply_markup=get_q1_keyboard()
    )

# Обработчики вопросов
@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q1)
async def q1_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q2, "Как ты спишь? 😴", get_q2_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q2)
async def q2_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q3, "Бывает ли у тебя напряжение в теле (плечи, шея, челюсти) без физической причины? 💆", get_q3_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q3)
async def q3_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q4, "Как часто у тебя возникают тревожные мысли о будущем? 🔮", get_q4_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q4)
async def q4_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q5, "Замечаешь ли ты учащённое сердцебиение, дрожь или потливость, когда тревожно? ❤️‍🔥", get_q5_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q5)
async def q5_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q6, "Как часто ты испытываешь раздражительность или вспышки гнева без серьёзной причины? 😠", get_q6_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q6)
async def q6_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q7, "Можешь ли ты спокойно сосредоточиться на задаче, когда вокруг стресс? 🎯", get_q7_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q7)
async def q7_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q8, "Как ты реагируешь на неожиданные трудности? 🚧", get_q8_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q8)
async def q8_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q9, "Часто ли ты избегаешь ситуаций, которые могут вызвать стресс или волнение? 🛑", get_q9_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q9)
async def q9_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q10, "Чувствуешь ли ты, что тревога мешает тебе отдыхать и наслаждаться жизнью? 🌴", get_q10_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q10)
async def q10_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q11, "Замечаешь ли ты, что тревога влияет на твоё здоровье (головные боли, желудок, усталость)? 💊", get_q11_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q11)
async def q11_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q12, "Насколько ты уверен(а) в своих силах справляться с трудностями? 💪", get_q12_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q12)
async def q12_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q13, "Как часто у тебя бывают трудности с дыханием или ощущение, что \"не хватает воздуха\" при тревоге? 🌬", get_q13_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q13)
async def q13_answer(callback: CallbackQuery, state: FSMContext):
    await process_answer(callback, state, AnxietyTest.q14, "Как часто тебе нужна поддержка других, чтобы успокоиться? 🤝", get_q14_keyboard)

@router.callback_query(F.data.startswith("ans_"), AnxietyTest.q14)
async def q14_answer(callback: CallbackQuery, state: FSMContext):
    answer_text = callback.data.replace("ans_", "")
    score = ANSWER_SCORES.get(answer_text, 0)
    
    data = await callback.message.bot.get_chat(callback.message.chat.id)
    total_score = data.get('score', 0) + score
    
    await state.set_state(AnxietyTest.q15)
    await callback.answer()
    await callback.message.edit_text(
        "И последний вопрос: если оценить свою тревожность по шкале от 0 до 10, какой балл ты поставишь? 📊\nПросто отправь цифру.",
        reply_markup=None
    )

# Обработчик последнего вопроса (числовой ответ)
@router.message(AnxietyTest.q15)
async def q15_answer(message: Message, state: FSMContext):
    try:
        user_score = int(message.text)
        if 0 <= user_score <= 10:
            data = await state.get_data()
            total_score = data.get('score', 0) + user_score
            
            # Сохраняем результат теста
            await db.save_test_result(message.from_user.id, "anxiety_test", total_score)
            
            # Определяем уровень тревожности
            if total_score <= 10:
                level = "Низкий"
                description = "Ты хорошо справляешься со стрессом! Курс поможет тебе ещё больше укрепить эти навыки."
            elif total_score <= 20:
                level = "Умеренный"
                description = "У тебя есть некоторые моменты тревожности, но в целом ты управляешь ситуацией. Курс поможет тебе чувствовать себя ещё увереннее."
            elif total_score <= 30:
                level = "Высокий"
                description = "Ты часто испытываешь тревогу, но это не означает, что ты не можешь с этим справиться. Курс даст тебе конкретные инструменты для работы с тревожностью."
            else:
                level = "Очень высокий"
                description = "Ты проходишь сложный период, и это нормально. Курс поможет тебе постепенно научиться справляться с тревогой и вернуть спокойствие."
            
    await message.answer(
                f"📊 Твой результат: {total_score} баллов\n"
                f"Уровень тревожности: {level}\n\n"
                f"{description}\n\n"
                f"Готов(а) начать курс? 🚀"
            )
            
            await state.clear()
            await show_main_menu(message, message.from_user.id)
            
        else:
            await message.answer("Пожалуйста, введи число от 0 до 10.")
    except ValueError:
        await message.answer("Пожалуйста, введи корректное число от 0 до 10.")