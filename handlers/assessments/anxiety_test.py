# handlers/assessments/anxiety_test.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
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

# Функция для проверки валидности ответа
def is_valid_answer(text: str) -> bool:
    """Проверяет, является ли текст валидным ответом из кнопок."""
    return text in ANSWER_SCORES

# Клавиатуры для каждого вопроса
q1_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🌤 Никогда", "🌦 Иногда, но быстро проходит", "🌧 Часто, но не мешает жить", "⛈ Почти постоянно, мешает сосредоточиться"]], resize_keyboard=True)
q2_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🌙 Легко засыпаю и сплю спокойно", "😌 Иногда долго засыпаю или просыпаюсь ночью", "😕 Засыпаю с трудом, сон поверхностный", "😣 Почти каждую ночь мучаюсь от плохого сна"]], resize_keyboard=True)
q3_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🌿 Никогда", "🍃 Иногда, но быстро отпускает", "🌾 Часто, но терпимо", "🪨 Постоянно, это мешает расслабиться"]], resize_keyboard=True)
q4_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🌞 Редко или никогда", "🌤 Иногда, но не зацикливаюсь", "🌧 Часто, и они крутятся в голове", "⛈ Почти постоянно, мешает жить"]], resize_keyboard=True)
q5_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["❌ Никогда", "🌬 Иногда, но быстро проходит", "💓 Часто при стрессе", "💢 Почти всегда, когда тревожно"]], resize_keyboard=True)
q6_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🍀 Редко", "🌿 Иногда", "🔥 Часто", "🌪 Почти всегда"]], resize_keyboard=True)
q7_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🏆 Легко", "🎈 Иногда отвлекаюсь", "🎭 Сильно отвлекаюсь", "🚫 Не могу сосредоточиться совсем"]], resize_keyboard=True)
q8_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🧘 Спокойно, ищу решение", "🙂 Немного переживаю, но быстро действую", "😰 Сильно переживаю, сложно начать действовать", "😱 Паника или ступор"]], resize_keyboard=True)
q9_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🟢 Редко", "🟡 Иногда", "🟠 Часто", "🔴 Почти всегда"]], resize_keyboard=True)
q10_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🟢 Редко или никогда", "🟡 Иногда", "🟠 Часто", "🔴 Почти всегда"]], resize_keyboard=True)
q11_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🌞 Никогда", "🌤 Иногда", "🌦 Часто", "🌪 Постоянно"]], resize_keyboard=True)
q12_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🥇 Полностью уверен(а)", "🥈 В основном уверен(а)", "🥉 Не всегда уверен(а)", "🚫 Почти не уверен(а)"]], resize_keyboard=True)
q13_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["❌ Никогда", "🌤 Иногда", "🌧 Часто", "⛈ Почти всегда"]], resize_keyboard=True)
q14_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for t in ["🟢 Редко или никогда", "🟡 Иногда", "🟠 Часто", "🔴 Почти всегда"]], resize_keyboard=True)

# Функция для обработки ответов
async def process_answer(message: Message, state: FSMContext, next_state, question_text: str, next_kb, current_kb):
    """Обрабатывает ответ пользователя и переходит к следующему вопросу."""
    if not is_valid_answer(message.text):
        await message.answer("Пожалуйста, выбери один из предложенных вариантов.", reply_markup=current_kb)
        return
    
    data = await state.get_data()
    score = data.get('score', 0) + ANSWER_SCORES.get(message.text, 0)
    await state.update_data(score=score)
    
    await state.set_state(next_state)
    await message.answer(question_text, reply_markup=next_kb)

# Точка входа для начального теста
async def start_anxiety_test(message: Message, state: FSMContext):
    """Начинает начальный пульс тревожности."""
    await state.set_state(AnxietyTest.intro)
    await message.answer(
        "Отлично! Давай определим твою отправную точку.\n\n"
        "Это поможет нам понять, как лучше всего поддержать тебя в процессе работы с тревожностью.\n\n"
        "Отвечай честно, опираясь на свои ощущения за последние 7 дней.\n\n"
        "Готов(а) начать? 💙",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Вперед! 💙")],
            [KeyboardButton(text="Пока не хочу")]
        ], resize_keyboard=True)
    )

# Обработчики для начального теста
@router.message(
    StateFilter(AnxietyTest.intro),
    F.text == "Пока не хочу"
)
async def abort_assessment(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Хорошо, можешь пройти пульс тревожности в любое время.", reply_markup=ReplyKeyboardRemove())
    await show_main_menu(message, message.from_user.id)

@router.message(
    StateFilter(AnxietyTest.intro),
    F.text == "Вперед! 💙"
)
async def q1_handler(message: Message, state: FSMContext):
    await state.set_state(AnxietyTest.q1)
    await state.update_data(score=0)
    await message.answer("1. Как часто в последнее время ты ощущаешь волнение или беспокойство без причины? 😟", reply_markup=q1_kb)

# Обработчики вопросов
@router.message(AnxietyTest.q1)
async def q1_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q2, "2. Как ты спишь? 😴", q2_kb, q1_kb)

@router.message(AnxietyTest.q2)
async def q2_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q3, "3. Бывает ли у тебя напряжение в теле (плечи, шея, челюсти) без физической причины? 💆", q3_kb, q2_kb)

@router.message(AnxietyTest.q3)
async def q3_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q4, "4. Как часто у тебя возникают тревожные мысли о будущем? 🔮", q4_kb, q3_kb)

@router.message(AnxietyTest.q4)
async def q4_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q5, "5. Замечаешь ли ты учащённое сердцебиение, дрожь или потливость, когда тревожно? ❤️‍🔥", q5_kb, q4_kb)

@router.message(AnxietyTest.q5)
async def q5_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q6, "6. Как часто ты испытываешь раздражительность или вспышки гнева без серьёзной причины? 😠", q6_kb, q5_kb)

@router.message(AnxietyTest.q6)
async def q6_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q7, "7. Можешь ли ты спокойно сосредоточиться на задаче, когда вокруг стресс? 🎯", q7_kb, q6_kb)

@router.message(AnxietyTest.q7)
async def q7_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q8, "8. Как ты реагируешь на неожиданные трудности? 🚧", q8_kb, q7_kb)

@router.message(AnxietyTest.q8)
async def q8_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q9, "9. Часто ли ты избегаешь ситуаций, которые могут вызвать стресс или волнение? 🛑", q9_kb, q8_kb)

@router.message(AnxietyTest.q9)
async def q9_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q10, "10. Чувствуешь ли ты, что тревога мешает тебе отдыхать и наслаждаться жизнью? 🌴", q10_kb, q9_kb)

@router.message(AnxietyTest.q10)
async def q10_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q11, "11. Замечаешь ли ты, что тревога влияет на твоё здоровье (головные боли, желудок, усталость)? 💊", q11_kb, q10_kb)

@router.message(AnxietyTest.q11)
async def q11_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q12, "12. Насколько ты уверен(а) в своих силах справляться с трудностями? 💪", q12_kb, q11_kb)

@router.message(AnxietyTest.q12)
async def q12_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q13, "13. Как часто у тебя бывают трудности с дыханием или ощущение, что \"не хватает воздуха\" при тревоге? 🌬", q13_kb, q12_kb)

@router.message(AnxietyTest.q13)
async def q13_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q14, "14. Как часто тебе нужна поддержка других, чтобы успокоиться? 🤝", q14_kb, q13_kb)

@router.message(AnxietyTest.q14)
async def q14_handler(message: Message, state: FSMContext):
    await process_answer(message, state, AnxietyTest.q15, "15. И последний вопрос: если оценить свою тревожность по шкале от 0 до 10, какой балл ты поставишь? 📊\nПросто отправь цифру.", None, q14_kb)
    await state.set_state(AnxietyTest.q15)

# Обработчик завершения начального теста
@router.message(AnxietyTest.q15, F.text.regexp(r'^\d+$'))
async def assessment_final(message: Message, state: FSMContext):
    self_assessment = int(message.text)
    if not (0 <= self_assessment <= 10):
        await message.answer("Пожалуйста, введи число от 0 до 10.")
        return

    data = await state.get_data()
    score = data.get('score', 0)
    
    # Получаем информацию о пользователе
    bookmark = await db.get_user_bookmark(message.from_user.id)
    course_id = bookmark['current_course_id'] if bookmark and bookmark['current_course_id'] else 1
    
    # Сохраняем результат начального теста
    await db.save_assessment_result(message.from_user.id, course_id, 'initial', score, self_assessment)
    
    await state.clear()
    await message.answer(
        f"Отлично! Мы определили отправную точку.\n\n"
        f"Твой результат: {score}/42 баллов\n"
        f"Самооценка тревожности: {self_assessment}/10\n\n"
        f"А теперь давай начнём наш первый урок!",
        reply_markup=ReplyKeyboardRemove()
    )
    await show_main_menu(message, message.from_user.id)

# Обработчик для невалидных ответов на последний вопрос
@router.message(AnxietyTest.q15)
async def invalid_q15_answer(message: Message):
    await message.answer(
        "❌ Пожалуйста, введите только цифру от 0 до 10 для оценки вашей тревожности.\n\n"
        "Например: 5"
    )