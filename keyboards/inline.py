from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_courses_kb(courses: list) -> InlineKeyboardMarkup:
    """Создает инлайн-клавиатуру со списком курсов."""
    buttons = []
    for course in courses:
        # course - это кортеж (id, title, emoji)
        button = InlineKeyboardButton(
            text=f"{course[2]} {course[1]}",
            callback_data=f"select_course_{course[0]}" # Например, select_course_1
        )
        buttons.append([button]) # Каждая кнопка на новой строке
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_days_keyboard(current_day: int, progress: set) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с 14 днями курса, отмечая их статусы.
    `progress` - это множество пройденных модулей {(день, модуль), ...}
    """
    buttons = []
    # Определяем, какие дни полностью пройдены (все 3 модуля)
    completed_days = set()
    day_counts = {}
    for day, module in progress:
        day_counts[day] = day_counts.get(day, 0) + 1
    for day, count in day_counts.items():
        if count == 3:
            completed_days.add(day)
            
    # Самый высокий полностью пройденный день
    last_completed_day = max(completed_days) if completed_days else 0

    for day in range(1, 15):
        status_icon = ""
        callback_data = f"select_day_{day}"

        if day == current_day:
            status_icon = "📍" # Текущий
        elif day in completed_days:
            status_icon = "✅" # Пройден
        elif day <= max(last_completed_day + 1, current_day):
            status_icon = "▶️" # Доступный (до текущего дня включительно или до последнего пройденного + 1)
        else:
            status_icon = "🔒" # Недоступен
            callback_data = "day_locked"

        buttons.append(InlineKeyboardButton(text=f"{status_icon} День {day}", callback_data=callback_data))

    # Создаем клавиатуру с 2 столбцами
    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_modules_keyboard(selected_day: int, bookmark, progress: set) -> InlineKeyboardMarkup:
    """Создает клавиатуру с 3 модулями для выбранного дня."""
    buttons = []
    current_day, current_module = bookmark['current_day'], bookmark['current_module']
    
    # Определяем, какие дни полностью пройдены (все 3 модуля)
    completed_days = set()
    day_counts = {}
    for day, module in progress:
        day_counts[day] = day_counts.get(day, 0) + 1
    for day, count in day_counts.items():
        if count == 3:
            completed_days.add(day)
    
    # Самый высокий полностью пройденный день
    last_completed_day = max(completed_days) if completed_days else 0

    for module in range(1, 4):
        status_icon = ""
        callback_data = f"select_module_{selected_day}_{module}"

        is_completed = (selected_day, module) in progress
        is_current = (selected_day == current_day and module == current_module)
        
        # Определяем доступность модуля
        # Модуль доступен, если:
        # 1. Он пройден
        # 2. Он текущий
        # 3. Предыдущий модуль в этом дне пройден
        # 4. Выбранный день доступен (до текущего дня включительно или до последнего пройденного + 1)
        is_day_accessible = selected_day <= max(last_completed_day + 1, current_day)
        is_unlocked = False
        
        if is_day_accessible:
            if module == 1 or (selected_day, module - 1) in progress:
                is_unlocked = True

        if is_current:
            status_icon = "📍"
        elif is_completed:
            status_icon = "✅"
        elif is_unlocked:
            status_icon = "▶️"
        else:
            status_icon = "🔒"
            callback_data = "module_locked"

        buttons.append(InlineKeyboardButton(text=f"{status_icon} Модуль {module}", callback_data=callback_data))

    return InlineKeyboardMarkup(inline_keyboard=[buttons])
    
def get_reset_courses_kb(courses: list) -> InlineKeyboardMarkup:
    """Создает инлайн-клавиатуру со списком курсов для сброса."""
    buttons = []
    for course in courses:
        button = InlineKeyboardButton(
            text=f"{course['emoji']} {course['title']}",
            callback_data=f"reset_course_{course['id']}" # Другой callback_data!
        )
        buttons.append([button])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_confirm_reset_kb() -> InlineKeyboardMarkup:
    """Создает клавиатуру подтверждения сброса."""
    buttons = [
        InlineKeyboardButton(text="✅ Да, сбрасываем", callback_data="confirm_reset"),
        InlineKeyboardButton(text="❌ Нет, не нужно", callback_data="cancel_reset")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])