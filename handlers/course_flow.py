# handlers/course_flow.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

import database as db
import keyboards.reply as kb
import keyboards.inline as ikb # <-- ДОБАВЬТЕ ЭТУ СТРОКУ

router = Router()


# --- Вспомогательная функция для показа главного меню (УПРОЩЕННАЯ) ---
async def show_main_menu(message: Message, user_id: int):
    """Отправляет пользователю его актуальное главное меню для курса тревожности."""
    try:
        bookmark = await db.get_user_bookmark(user_id)
        
        # Если у пользователя нет активного курса, сообщаем об ошибке
        if not bookmark or not bookmark['current_course_id']:
            await message.answer("Ошибка: пользователь не найден. Попробуйте перезапустить бота командой /start")
            return
        
        course_id = bookmark['current_course_id']
        course_info = await db.get_course_by_id(course_id)
        
        # --- УПРОЩЕННАЯ ЛОГИКА ДЛЯ КУРСА ТРЕВОЖНОСТИ ---
        
        # 1. Проверяем, пройден ли курс полностью (42 модуля)
        progress = await db.get_all_completed_modules_for_course(user_id, course_id)
        if len(progress) >= 42:
            # Проверяем, есть ли финальный тест
            all_results = await db.get_all_assessment_results(user_id, course_id)
            if all_results.get('final'):
                main_button_text = "Курс завершен"
            else:
                main_button_text = "Оценить прогресс"
        else:
            # 2. Если курс не пройден, проверяем, был ли начальный пульс тревожности
            initial_assessment = await db.get_initial_assessment_result(user_id, course_id)
            if not initial_assessment:
                # 3. Если пульса не было, предлагаем его пройти
                main_button_text = "Пройти начальную оценку"
            else:
                # 4. Если пульс был, показываем текущий модуль из закладки
                main_button_text = f"▶️ День {bookmark['current_day']}, Модуль {bookmark['current_module']}"

        # --- Конец упрощенной логики ---

        main_menu_kb = kb.ReplyKeyboardMarkup(
            keyboard=[
                [kb.KeyboardButton(text=main_button_text), kb.KeyboardButton(text="📚 Выбрать модуль")],
                [kb.KeyboardButton(text="🙏 Практики"), kb.KeyboardButton(text="🙍 Профиль")]
            ],
            resize_keyboard=True
        )
        await message.answer("🪷", reply_markup=main_menu_kb)
        
    except Exception as e:
        print(f"Ошибка в show_main_menu: {e}")
        await message.answer("Произошла ошибка при загрузке меню. Попробуйте позже.")

# --- Основная логика прохождения ---

# 1. Нажатие на главную кнопку "День X, Модуль Y" или другие варианты
@router.message(F.text.regexp(r'^▶️ День \d+, Модуль \d+$'))
async def start_module(message: Message, state: FSMContext):
    user_id = message.from_user.id
    bookmark = await db.get_user_bookmark(user_id)
    
    # Проверяем, что закладка существует
    if not bookmark or not bookmark['current_day']:
        await message.answer("Ошибка: пользователь не найден. Попробуйте перезапустить бота командой /start")
        return
    
    if bookmark['current_day'] > 14:
        await message.answer(
            "🎉 Поздравляем!\n"
            "14-дневный курс по снижению тревожности завершён. Это серьёзный шаг — и твоя личная заслуга 🙌\n\n"
            "За это время удалось регулярно выполнять упражнения, знакомиться с новыми практиками и глубже понять себя. Теперь у тебя есть набор знаний и техник, которые можно использовать в любой момент. 🌿\n\n"
            "Спасибо за настойчивость и внимание к себе! Пусть спокойствие становится привычным состоянием, а тревога приходит всё реже 💫"
        )
        return

    # ПРОВЕРКА: если пользователь не прошел начальный пульс тревожности, блокируем доступ к модулям
    # Проверяем пульс для курса тревожности (ID = 1), независимо от выбранного модуля
    initial_assessment = await db.get_initial_assessment_result(user_id, 1)  # Всегда проверяем курс тревожности
    if not initial_assessment:
        await message.answer(
            "🔒 Для доступа к модулям курса необходимо сначала пройти начальную оценку.\n\n"
            "Это поможет нам лучше подстроить курс под ваши потребности и отследить ваш прогресс.\n\n"
            "Готовы пройти пульс тревожности?",
            reply_markup=kb.ReplyKeyboardMarkup(keyboard=[
                [kb.KeyboardButton(text="✅ Да, пройти пульс тревожности")],
                [kb.KeyboardButton(text="🏠 В главное меню")]
            ], resize_keyboard=True)
        )
        return

    # Попытка динамического импорта модуля
    day = bookmark['current_day']
    module = bookmark['current_module']
    module_name = f"handlers.modules.day_{day}_module_{module}"
    
    try:
        # Динамически импортируем нужный модуль
        module_handler = importlib.import_module(module_name)
        
        # Формируем имя функции для запуска модуля
        function_name = f"start_day_{day}_module_{module}"
        
        if hasattr(module_handler, function_name):
            # Запускаем модуль
            await getattr(module_handler, function_name)(message, state)
        else:
            # Если функция не найдена, показываем заглушку
            await show_module_placeholder(message, day, module)
            
    except ImportError:
        # Если модуль не найден, показываем заглушку
        await show_module_placeholder(message, day, module)

async def show_module_placeholder(message: Message, day: int, module: int):
    """Показывает заглушку для модуля, который еще не реализован."""
    course_info = await db.get_course_by_id(1)  # Курс тревожности
    
    await message.answer(
        f"📖 Курс «{course_info['emoji']} {course_info['title']}»\n"
        f"**День {day}, Модуль {module}**\n\n"
        "Здесь будет текст вашего модуля...\n\n"
        "🚧 Модуль находится в разработке. Скоро здесь появится интерактивное содержимое!",
        parse_mode="Markdown",
        reply_markup=kb.module_navigation_kb
    )

# Обработчик для кнопки "Пройти начальную оценку"
@router.message(F.text == "Пройти начальную оценку")
async def start_initial_assessment(message: Message, state: FSMContext):
    from handlers.assessments.anxiety_test import start_anxiety_test
    await start_anxiety_test(message, state)

# Обработчик для кнопки "Курс завершен"
@router.message(F.text == "Курс завершен")
async def show_course_completion(message: Message):
    user_id = message.from_user.id
    bookmark = await db.get_user_bookmark(user_id)
    course_id = bookmark['current_course_id'] if bookmark and bookmark['current_course_id'] else 1
    
    # Получаем результаты тестов
    all_results = await db.get_all_assessment_results(user_id, course_id)
    initial_score = all_results.get('initial', {}).get('score', 0)
    final_score = all_results.get('final', {}).get('score', 0)
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
    
    # Создаем reply клавиатуру для сброса прогресса
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    
    await message.answer(
        f"🎉 Поздравляем!\n"
        f"14-дневный курс по снижению тревожности завершён. Это серьёзный шаг — и твоя личная заслуга 🙌\n\n"
        f"За это время удалось регулярно выполнять упражнения, знакомиться с новыми практиками и глубже понять себя. Теперь у тебя есть набор знаний и техник, которые можно использовать в любой момент. 🌿\n\n"
        f"Спасибо за настойчивость и внимание к себе! Пусть спокойствие становится привычным состоянием, а тревога приходит всё реже 💫\n\n"
        f"📊 **Результаты сравнения**\n\n"
        f"Пульс тревожности до курса: {initial_score}/42 баллов\n"
        f"Пульс тревожности после курса: {final_score}/42 баллов\n"
        f"Разница: {difference:+d} баллов\n\n"
        f"{result_message}",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="🔄 Сбросить прогресс")],
            [KeyboardButton(text="🏠 В главное меню")]
        ], resize_keyboard=True)
    )

# Обработчик для кнопки "🔄 Сбросить прогресс"
@router.message(F.text == "🔄 Сбросить прогресс")
async def handle_reset_progress_reply(message: Message):
    """Обработчик для кнопки 'Сбросить прогресс' через reply клавиатуру."""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    await message.answer(
        "⚠️ Вы точно хотите сбросить прогресс?\n"
        "🗑️ Все данные будут удалены.",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Да ✅"), KeyboardButton(text="Нет ❌")]
        ], resize_keyboard=True)
    )

# Обработчик для кнопки "Да ✅"
@router.message(F.text == "Да ✅")
async def handle_confirm_reset_reply(message: Message):
    """Обработчик для подтверждения сброса прогресса."""
    user_id = message.from_user.id
    bookmark = await db.get_user_bookmark(user_id)
    course_id = bookmark['current_course_id'] if bookmark and bookmark['current_course_id'] else 1
    
    # Сбрасываем прогресс и оценки
    await db.reset_progress_for_course(user_id, course_id)
    await db.reset_assessment_results(user_id, course_id)
    
    # Сбрасываем закладку пользователя
    await db.reset_user_bookmark(user_id)
    
    await message.answer(
        "✅ Прогресс сброшен!\n\n"
        "📘 Для запуска курса нажмите ▶️ /start",
        reply_markup=ReplyKeyboardRemove()
    )

# Обработчик для кнопки "Нет ❌"
@router.message(F.text == "Нет ❌")
async def handle_cancel_reset_reply(message: Message):
    """Обработчик для отмены сброса прогресса."""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    await message.answer(
        "❌ Сброс отменен",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="🔄 Сбросить прогресс")],
            [KeyboardButton(text="🏠 В главное меню")]
        ], resize_keyboard=True)
    )

# Обработчик для кнопки "🏠 В главное меню"
@router.message(F.text == "🏠 В главное меню")
async def back_to_main_from_completion(message: Message):
    """Возврат в главное меню из поздравления."""
    await show_main_menu(message, message.from_user.id)

# Обработчик для кнопки "Оценить прогресс"
@router.message(F.text == "Оценить прогресс")
async def start_final_assessment(message: Message, state: FSMContext):
    from handlers.assessments.final_test import start_final_test
    await start_final_test(message, state)

# Обработчики для кнопок блокировки модулей (дублируем из menu.py для удобства)
@router.message(F.text == "✅ Да, пройти пульс тревожности")
async def start_test_from_blocked_modules_course(message: Message, state: FSMContext):
    """Пользователь согласился пройти пульс тревожности после попытки доступа к модулям."""
    from handlers.assessments.anxiety_test import start_anxiety_test
    await start_anxiety_test(message, state)

@router.message(F.text == "🏠 В главное меню")
async def back_to_main_from_blocked_modules_course(message: Message):
    """Возврат в главное меню из блокировки модулей."""
    await message.answer("Возвращаю в главное меню.", reply_markup=ReplyKeyboardRemove())
    await show_main_menu(message, message.from_user.id)

# 2. Нажатие на "Давай повторим"
@router.message(F.text == "🔄 Давай повторим")
async def repeat_module(message: Message, state: FSMContext):
    user_id = message.from_user.id
    bookmark = await db.get_user_bookmark(user_id)
    
    # Получаем информацию о последнем завершенном модуле
    last_completed = await db.get_last_completed_module(user_id, bookmark['current_course_id'])
    
    if last_completed:
        # Возвращаем закладку к последнему завершенному модулю
        await db.set_user_bookmark(user_id, bookmark['current_course_id'], last_completed['day'], last_completed['module'])
        await start_module(message, state)
    else:
        await message.answer("Ошибка: не удалось найти последний модуль для повторения.")

# 3. Нажатие на "Все ясно"
@router.message(F.text == "✅ Все ясно")
async def complete_module(message: Message):
    user_id = message.from_user.id
    bookmark = await db.get_user_bookmark(user_id)

    # 1. Записываем прогресс
    await db.complete_module(
        user_id,
        bookmark['current_course_id'],
        bookmark['current_day'],
        bookmark['current_module']
    )
    
    # 2. СРАЗУ передвигаем закладку
    current_day = bookmark['current_day']
    current_module = bookmark['current_module']
    next_day, next_module = await db.advance_user_to_next_module(user_id, current_day, current_module)
    
    # 3. Проверяем, был ли это последний модуль дня
    if current_module == 3:
        # Проверяем, завершен ли весь курс (14 дней)
        if current_day == 14:  # Именно завершение 14-го дня
            await message.answer(
                "🎉 Поздравляем!\n"
                "14-дневный курс по снижению тревожности завершён. Это серьёзный шаг — и твоя личная заслуга 🙌\n\n"
                "За это время удалось регулярно выполнять упражнения, знакомиться с новыми практиками и глубже понять себя. Теперь у тебя есть набор знаний и техник, которые можно использовать в любой момент. 🌿\n\n"
                "Спасибо за настойчивость и внимание к себе! Пусть спокойствие становится привычным состоянием, а тревога приходит всё реже 💫"
            )
            # После поздравления показываем главное меню
            await show_main_menu(message, user_id)
        else:
            await message.answer(
                "Мы отлично поработали! ✨\n"
                "Сегодняшние практики завершены. Завтра нас ждет следующий шаг."
            )
            # Если день закончен, сразу возвращаем в главное меню
            await show_main_menu(message, user_id)
    else:
        # Если это не последний модуль, показываем промежуточное меню
        await message.answer(
            "Отлично! Двигаемся дальше?",
            reply_markup=kb.after_module_kb
        )

# 4. Нажатие на "Двигаемся дальше"
@router.message(F.text == "▶️ Двигаемся дальше")
async def advance_to_next(message: Message, state: FSMContext):
    # Теперь эта кнопка просто запускает следующий модуль,
    # так как закладка уже передвинута.
    await start_module(message, state)

# 5. Нажатие на "В основное меню"
@router.message(F.text == "🏠 В основное меню")
async def back_to_main_menu(message: Message):
    """Возврат в главное меню из модуля."""
    await message.answer("Возвращаю вас в главное меню.", reply_markup=ReplyKeyboardRemove())
    await show_main_menu(message, message.from_user.id)

# Обработчики для инлайн кнопок (удалены - заменены на reply кнопки)