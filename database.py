# database.py

import asyncpg
from datetime import datetime
from config import DATABASE_URL

# --- Функции для пользователей ---

async def add_user(telegram_id: int, first_name: str, username: str):
    """Добавляет пользователя, если его нет, и возвращает его ID в базе."""
    conn = await asyncpg.connect(DATABASE_URL)
    # Сначала проверяем, существует ли пользователь, чтобы получить его ID
    user_db_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", telegram_id)

    if user_db_id:
        await conn.close()
        return user_db_id

    # Если пользователя нет, добавляем его
    sql_insert = """
        INSERT INTO users (telegram_id, first_name, username)
        VALUES ($1, $2, $3)
        ON CONFLICT (telegram_id) DO NOTHING
        RETURNING id;
    """
    try:
        user_db_id = await conn.fetchval(sql_insert, telegram_id, first_name, username)
        print(f"Пользователь {telegram_id} успешно добавлен.")
        return user_db_id
    finally:
        await conn.close()

async def get_user_bookmark(telegram_id: int):
    """Получает текущую закладку пользователя (курс, день, модуль)."""
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        row = await conn.fetchrow(
            "SELECT current_course_id, current_day, current_module FROM users WHERE telegram_id = $1",
            telegram_id
        )
        return row
    finally:
        await conn.close()

# НОВАЯ функция для обновления закладки
async def update_user_bookmark(user_id: int, course_id: int, day: int, module: int):
    """Универсально обновляет закладку пользователя."""
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Сначала проверяем, существует ли пользователь
        user_exists = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
        if not user_exists:
            # Если пользователя нет, создаем его с минимальными данными
            await conn.execute(
                "INSERT INTO users (telegram_id, first_name, username) VALUES ($1, $2, $3) ON CONFLICT (telegram_id) DO NOTHING",
                user_id, "User", None
            )
        
        sql = "UPDATE users SET current_course_id = $1, current_day = $2, current_module = $3 WHERE telegram_id = $4"
        result = await conn.execute(sql, course_id, day, module, user_id)
        
        # Проверяем, что обновление прошло успешно
        if result == "UPDATE 0":
            print(f"Предупреждение: не удалось обновить закладку для пользователя {user_id}")
            
    finally:
        await conn.close()

# НОВАЯ функция для получения даты регистрации
async def get_user_start_date(user_id: int) -> str:
    """Возвращает дату регистрации пользователя в формате 'ДД месяца ГГГГ'."""
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        created_at_datetime = await conn.fetchval("SELECT created_at FROM users WHERE telegram_id = $1", user_id)
        if not created_at_datetime:
            return "неизвестно"

        # --- ИЗМЕНЕНИЯ ЗДЕСЬ ---
        # Создаем список с русскими названиями месяцев в родительном падеже
        months_ru = [
            "января", "февраля", "марта", "апреля", "мая", "июня",
            "июля", "августа", "сентября", "октября", "ноября", "декабря"
        ]
        
        # Собираем строку вручную
        day = created_at_datetime.day
        month = months_ru[created_at_datetime.month - 1] # -1, так как список с 0
        year = created_at_datetime.year
        
        return f"{day} {month} {year} года"

    finally:
        await conn.close()
        
# --- Функции для курсов и прогресса ---

async def get_course_by_id(course_id: int):
    """Получает информацию о курсе по его ID."""
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # --- ИЗМЕНЕНИЕ ЗДЕСЬ: добавляем description в запрос ---
        course = await conn.fetchrow("SELECT title, emoji, description FROM courses WHERE id = $1", course_id)
        return course
    finally:
        await conn.close()

async def get_all_courses():
    """Получает список всех курсов (id, title, emoji) из базы данных."""
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch("SELECT id, title, emoji FROM courses ORDER BY id")
        return rows
    finally:
        await conn.close()

# НОВАЯ функция для поиска последнего прогресса
async def get_latest_progress_for_course(user_id: int, course_id: int):
    """Находит последний пройденный модуль для пользователя в конкретном курсе."""
    conn = await asyncpg.connect(DATABASE_URL)
    # Нам нужен внутренний id пользователя для связи с user_progress
    db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
    if not db_user_id:
        await conn.close()
        return None
        
    sql = """
        SELECT day, module FROM user_progress
        WHERE user_id = $1 AND course_id = $2
        ORDER BY day DESC, module DESC
        LIMIT 1;
    """
    try:
        row = await conn.fetchrow(sql, db_user_id, course_id)
        return row
    finally:
        await conn.close()

async def complete_module(user_id: int, course_id: int, day: int, module: int):
    """Отмечает модуль как пройденный в таблице user_progress."""
    conn = await asyncpg.connect(DATABASE_URL)
    db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
    sql = """
        INSERT INTO user_progress (user_id, course_id, day, module)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (user_id, course_id, day, module) DO NOTHING;
    """
    try:
        await conn.execute(sql, db_user_id, course_id, day, module)
    finally:
        await conn.close()

async def advance_user_to_next_module(telegram_id: int, current_day: int, current_module: int):
    """Передвигает закладку пользователя на следующий модуль или день."""
    next_day = current_day
    next_module = current_module + 1

    if next_module > 3:
        next_module = 1
        next_day += 1

    conn = await asyncpg.connect(DATABASE_URL)
    sql = "UPDATE users SET current_day = $1, current_module = $2 WHERE telegram_id = $3"
    try:
        await conn.execute(sql, next_day, next_module, telegram_id)
        return next_day, next_module
    finally:
        await conn.close()
        
# НОВАЯ функция для получения ВСЕГО прогресса по ВСЕМ курсам
async def get_all_courses_progress(user_id: int):
    """
    Возвращает список словарей, каждый из которых содержит информацию о курсе 
    и количестве пройденных в нем модулей.
    """
    conn = await asyncpg.connect(DATABASE_URL)
    db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
    if not db_user_id:
        await conn.close()
        return []
    
    sql = """
        SELECT c.id, c.title, c.emoji, COUNT(up.id) as modules_completed
        FROM courses c
        LEFT JOIN user_progress up ON c.id = up.course_id AND up.user_id = $1
        GROUP BY c.id, c.title, c.emoji
        ORDER BY c.id;
    """
    try:
        rows = await conn.fetch(sql, db_user_id)
        return [dict(row) for row in rows]
    finally:
        await conn.close()

# НОВАЯ функция для сброса прогресса
async def reset_progress_for_course(user_id: int, course_id: int):
    """Удаляет ВЕСЬ прогресс пользователя по конкретному курсу."""
    conn = await asyncpg.connect(DATABASE_URL)
    db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
    if not db_user_id:
        await conn.close()
        return

    sql_progress = "DELETE FROM user_progress WHERE user_id = $1 AND course_id = $2"
    sql_bookmark = "UPDATE users SET current_course_id = NULL, current_day = NULL, current_module = NULL WHERE telegram_id = $1 AND current_course_id = $2"
    try:
        async with conn.transaction():
            await conn.execute(sql_progress, db_user_id, course_id)
            await conn.execute(sql_bookmark, user_id, course_id)
    finally:
        await conn.close()
        
async def get_all_completed_modules_for_course(user_id: int, course_id: int):
    """Возвращает МНОЖЕСТВО кортежей (день, модуль) для всех пройденных модулей."""
    conn = await asyncpg.connect(DATABASE_URL)
    db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
    if not db_user_id:
        await conn.close()
        return set()

    sql = "SELECT day, module FROM user_progress WHERE user_id = $1 AND course_id = $2"
    try:
        rows = await conn.fetch(sql, db_user_id, course_id)
        # Возвращаем как множество для быстрых проверок `(day, module) in progress`
        return {tuple(row) for row in rows}
    finally:
        await conn.close()
        
async def save_assessment_result(user_id: int, course_id: int, assessment_type: str, score: int, self_assessment: int):
    """Сохраняет результаты тестирования в базу данных."""
    conn = await asyncpg.connect(DATABASE_URL)
    db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
    if not db_user_id:
        await conn.close()
        return

    sql = """
        INSERT INTO assessment_results (user_id, course_id, assessment_type, score, self_assessment_score)
        VALUES ($1, $2, $3, $4, $5);
    """
    try:
        await conn.execute(sql, db_user_id, course_id, assessment_type, score, self_assessment)
    finally:
        await conn.close()
        
async def get_initial_assessment_result(user_id: int, course_id: int):
    """Ищет результат начального тестирования для пользователя и курса."""
    conn = await asyncpg.connect(DATABASE_URL)
    db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
    if not db_user_id:
        await conn.close()
        return None
        
    sql = """
        SELECT id FROM assessment_results
        WHERE user_id = $1 AND course_id = $2 AND assessment_type = 'initial'
        LIMIT 1;
    """
    try:
        # fetchrow вернет запись, если она есть, и None, если ее нет
        result = await conn.fetchrow(sql, db_user_id, course_id)
        return result
    finally:
        await conn.close()

async def get_all_assessment_results(user_id: int, course_id: int):
    """Получает все результаты тестирования для пользователя и курса."""
    conn = await asyncpg.connect(DATABASE_URL)
    db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
    if not db_user_id:
        await conn.close()
        return {}
        
    sql = """
        SELECT assessment_type, score, self_assessment_score
        FROM assessment_results
        WHERE user_id = $1 AND course_id = $2
        ORDER BY assessment_type;
    """
    try:
        rows = await conn.fetch(sql, db_user_id, course_id)
        results = {}
        for row in rows:
            results[row['assessment_type']] = {
                'score': row['score'],
                'self_assessment': row['self_assessment_score']
            }
        return results
    finally:
        await conn.close()