from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- Онбординг ---
onboarding_start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Давай попробуем")],
        [KeyboardButton(text="🙂 Поехали")]
    ],
    resize_keyboard=True
)

onboarding_q1_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌀 О, это про меня")],
        [KeyboardButton(text="🤔 Иногда, но не всегда")],
        [KeyboardButton(text="😌 Я мастер спокойствия")]
    ],
    resize_keyboard=True
)

onboarding_q2_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌙 Я и под шум холодильника засну")],
        [KeyboardButton(text="🦉 Ворочаюсь, как сова")],
        [KeyboardButton(text="🛌 Сон? Где-то я его теряю по пути")]
    ],
    resize_keyboard=True
)

onboarding_q3_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎯 Бросаюсь в бой и разлетаюсь в разные стороны")],
        [KeyboardButton(text="😵‍💫 Сижу и листаю соцсети")],
        [KeyboardButton(text="🤷‍♂️ Берусь за что-то простое и медленно раскачиваюсь")]
    ],
    resize_keyboard=True
)

onboarding_q4_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎢 Да, это прям про меня")],
        [KeyboardButton(text="😐 Почти не замечаю за собой")],
        [KeyboardButton(text="🫣 Иногда прям шторм внутри")]
    ],
    resize_keyboard=True
)

onboarding_final_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Да, давай пройдем тест")],
        [KeyboardButton(text="🤔 Сначала расскажи про курс")]
    ],
    resize_keyboard=True
)

# --- Главное меню ---
def get_main_menu_kb(course_title: str, emoji: str) -> ReplyKeyboardMarkup:
    """Создает клавиатуру главного меню с динамической кнопкой курса."""
    main_button_text = f"Начать «{emoji} {course_title}»"
    
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=main_button_text)],
            [
                KeyboardButton(text="Выбрать курс"),
                KeyboardButton(text="Выбрать модуль")
            ],
            [
                KeyboardButton(text="Практики"),
                KeyboardButton(text="Профиль")
            ]
        ],
        resize_keyboard=True
    )
    
module_navigation_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Все ясно")],
        [KeyboardButton(text="🔄 Давай повторим")]
    ],
    resize_keyboard=True
)

after_module_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="▶️ Двигаемся дальше")],
        [KeyboardButton(text="🏠 В основное меню")]
    ],
    resize_keyboard=True
)

# --- Подтверждение выбора курса ---
course_confirmation_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Отлично, мне подходит")],
        [KeyboardButton(text="🤔 Узнать подробнее")],
        [KeyboardButton(text="↩️ Вернуться к выбору курса")]
    ],
    resize_keyboard=True
)

# --- Оценка состояния ---
initial_assessment_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🚀 Давай начнем!")]],
    resize_keyboard=True
)

final_assessment_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Сравнить с начальным состоянием")]],
    resize_keyboard=True
)

# --- Профиль ---
profile_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📖 Завершенные курсы")],
        [KeyboardButton(text="🗑️ Сбросить прогресс")],
        [KeyboardButton(text="↩️ Вернуться в меню")]
    ],
    resize_keyboard=True
)