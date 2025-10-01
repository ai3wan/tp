# handlers/assessments/final_test.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import database as db
from handlers.course_flow import show_main_menu

# Отдельный роутер для финального теста
router = Router()

# FSM-группа для финального теста
class FinalTest(StatesGroup):
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

# Словарь для подсчета баллов (копируем из anxiety_test.py)
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

# Клавиатуры для каждого вопроса (копируем из anxiety_test.py)
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

# Точка входа для финального теста
async def start_final_test(message: Message, state: FSMContext):
    """Начинает финальный тест."""
    await state.set_state(FinalTest.intro)
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

# Обработчики для финального теста
@router.message(
    StateFilter(FinalTest.intro),
    F.text == "Пока не хочу"
)
async def abort_final_test(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Хорошо, можешь пройти финальный пульс тревожности в любое время.", reply_markup=ReplyKeyboardRemove())
    await show_main_menu(message, message.from_user.id)

@router.message(
    StateFilter(FinalTest.intro),
    F.text == "Вперед! 💙"
)
async def start_final_questions(message: Message, state: FSMContext):
    await state.set_state(FinalTest.q1)
    await message.answer(
        "Как часто у тебя бывают тревожные мысли, которые сложно остановить? 🤔",
        reply_markup=q1_kb
    )

# Обработчики вопросов
@router.message(FinalTest.q1)
async def final_q1(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q2, "Как ты спишь? 😴", q2_kb, q1_kb)

@router.message(FinalTest.q2)
async def final_q2(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q3, "Бывает ли у тебя напряжение в теле (плечи, шея, челюсти) без физической причины? 💆", q3_kb, q2_kb)

@router.message(FinalTest.q3)
async def final_q3(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q4, "Как часто у тебя возникают тревожные мысли о будущем? 🔮", q4_kb, q3_kb)

@router.message(FinalTest.q4)
async def final_q4(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q5, "Замечаешь ли ты учащённое сердцебиение, дрожь или потливость, когда тревожно? ❤️‍🔥", q5_kb, q4_kb)

@router.message(FinalTest.q5)
async def final_q5(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q6, "Как часто ты испытываешь раздражительность или вспышки гнева без серьёзной причины? 😠", q6_kb, q5_kb)

@router.message(FinalTest.q6)
async def final_q6(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q7, "Можешь ли ты спокойно сосредоточиться на задаче, когда вокруг стресс? 🎯", q7_kb, q6_kb)

@router.message(FinalTest.q7)
async def final_q7(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q8, "Как ты реагируешь на неожиданные трудности? 🚧", q8_kb, q7_kb)

@router.message(FinalTest.q8)
async def final_q8(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q9, "Часто ли ты избегаешь ситуаций, которые могут вызвать стресс или волнение? 🛑", q9_kb, q8_kb)

@router.message(FinalTest.q9)
async def final_q9(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q10, "Чувствуешь ли ты, что тревога мешает тебе отдыхать и наслаждаться жизнью? 🌴", q10_kb, q9_kb)

@router.message(FinalTest.q10)
async def final_q10(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q11, "Замечаешь ли ты, что тревога влияет на твоё здоровье (головные боли, желудок, усталость)? 💊", q11_kb, q10_kb)

@router.message(FinalTest.q11)
async def final_q11(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q12, "Насколько ты уверен(а) в своих силах справляться с трудностями? 💪", q12_kb, q11_kb)

@router.message(FinalTest.q12)
async def final_q12(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q13, "Как часто у тебя бывают трудности с дыханием или ощущение, что \"не хватает воздуха\" при тревоге? 🌬", q13_kb, q12_kb)

@router.message(FinalTest.q13)
async def final_q13(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q14, "Как часто тебе нужна поддержка других, чтобы успокоиться? 🤝", q14_kb, q13_kb)

@router.message(FinalTest.q14)
async def final_q14(message: Message, state: FSMContext):
    await process_answer(message, state, FinalTest.q15, "Оцени свою общую тревожность за последнюю неделю по шкале от 0 до 10, где 0 — совсем не тревожно, а 10 — очень тревожно.", None, q14_kb)
    await state.set_state(FinalTest.q15)

# Обработчик завершения финального теста
@router.message(FinalTest.q15, F.text.regexp(r'^\d+$'))
async def final_test_complete(message: Message, state: FSMContext):
    self_assessment = int(message.text)
    if not (0 <= self_assessment <= 10):
        await message.answer("Пожалуйста, введи число от 0 до 10.")
        return

    data = await state.get_data()
    final_score = data.get('score', 0)

    # Получаем результат начального теста для сравнения
    bookmark = await db.get_user_bookmark(message.from_user.id)
    course_id = bookmark['current_course_id'] if bookmark and bookmark['current_course_id'] else 1
    
    # Получаем результаты всех тестов
    all_results = await db.get_all_assessment_results(message.from_user.id, course_id)
    initial_score = all_results.get('initial', {}).get('score', 0)
    
    # Сохраняем результат финального теста
    await db.save_assessment_result(message.from_user.id, course_id, 'final', final_score, self_assessment)
    
    # Вычисляем разницу
    difference = final_score - initial_score
    
    # Определяем сообщение на основе разницы
    if difference <= -10:
        result_message = "✨ Отличный результат! Тревожность снизилась заметно. Продолжай использовать практики — они уже приносят плоды."
    elif -9 <= difference <= -4:
        result_message = "💫 Есть положительный сдвиг. Регулярная практика поможет закрепить результат и усилить эффект."
    elif -3 <= difference <= 3:
        result_message = "🌿 Значимых изменений пока нет. Продолжение практик или повторное прохождение курса может помочь."
    elif 4 <= difference <= 9:
        result_message = "⚖️ Уровень тревожности немного вырос. Попробуй вернуться к практикам или пройти курс заново, чтобы поддержать баланс."
    else:  # difference >= 10
        result_message = "❤️ Видно, что тревожность усилилась. Попробуй ещё раз использовать практики, а если тревога мешает повседневной жизни — стоит обратиться к специалисту."
    
    await message.answer(
        f"📊 **Результаты сравнения**\n\n"
        f"Пульс тревожности до курса: {initial_score}/42 баллов\n"
        f"Пульс тревожности после курса: {final_score}/42 баллов\n"
        f"Разница: {difference:+d} баллов\n\n"
        f"{result_message}"
    )
    
    await state.clear()
    await show_main_menu(message, message.from_user.id)

# Обработчик для невалидных ответов на последний вопрос
@router.message(FinalTest.q15)
async def invalid_final_q15_answer(message: Message):
    await message.answer(
        "❌ Пожалуйста, введите только цифру от 0 до 10 для оценки вашей тревожности.\n\n"
        "Например: 5"
    )

