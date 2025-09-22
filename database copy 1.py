# database.py

import asyncpg
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
    sql = "UPDATE users SET current_course_id = $1, current_day = $2, current_module = $3 WHERE telegram_id = $4"
    try:
        await conn.execute(sql, course_id, day, module, user_id)
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