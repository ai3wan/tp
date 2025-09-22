import asyncpg
from datetime import datetime

# --- Функции для пользователей ---

async def add_user(pool: asyncpg.Pool, telegram_id: int, first_name: str, username: str):
    """Добавляет пользователя, если его нет."""
    sql = """
        INSERT INTO users (telegram_id, first_name, username)
        VALUES ($1, $2, $3)
        ON CONFLICT (telegram_id) DO NOTHING;
    """
    async with pool.acquire() as conn:
        await conn.execute(sql, telegram_id, first_name, username)

async def get_user_bookmark(pool: asyncpg.Pool, telegram_id: int):
    """Получает текущую закладку пользователя (курс, день, модуль)."""
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            "SELECT current_course_id, current_day, current_module FROM users WHERE telegram_id = $1",
            telegram_id
        )

async def update_user_bookmark(pool: asyncpg.Pool, user_id: int, course_id: int, day: int, module: int):
    """Универсально обновляет закладку пользователя."""
    sql = "UPDATE users SET current_course_id = $1, current_day = $2, current_module = $3 WHERE telegram_id = $4"
    async with pool.acquire() as conn:
        await conn.execute(sql, course_id, day, module, user_id)

async def get_user_start_date(pool: asyncpg.Pool, user_id: int) -> str:
    """Возвращает дату регистрации пользователя в формате 'ДД месяца ГГГГ'."""
    async with pool.acquire() as conn:
        created_at_datetime = await conn.fetchval("SELECT created_at FROM users WHERE telegram_id = $1", user_id)
        if not created_at_datetime:
            return "неизвестно"

        months_ru = [
            "января", "февраля", "марта", "апреля", "мая", "июня",
            "июля", "августа", "сентября", "октября", "ноября", "декабря"
        ]
        
        day = created_at_datetime.day
        month = months_ru[created_at_datetime.month - 1]
        year = created_at_datetime.year
        
        return f"{day} {month} {year} года"
        
# --- Функции для курсов и прогресса ---

async def get_course_by_id(pool: asyncpg.Pool, course_id: int):
    """Получает информацию о курсе по его ID."""
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT title, emoji, description FROM courses WHERE id = $1", course_id)

async def get_all_courses(pool: asyncpg.Pool):
    """Получает список всех курсов (id, title, emoji) из базы данных."""
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT id, title, emoji FROM courses ORDER BY id")

async def get_latest_progress_for_course(pool: asyncpg.Pool, user_id: int, course_id: int):
    """Находит последний пройденный модуль для пользователя в конкретном курсе."""
    async with pool.acquire() as conn:
        db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
        if not db_user_id:
            return None

        sql = """
            SELECT day, module FROM user_progress
            WHERE user_id = $1 AND course_id = $2
            ORDER BY day DESC, module DESC
            LIMIT 1;
        """
        return await conn.fetchrow(sql, db_user_id, course_id)

async def complete_module(pool: asyncpg.Pool, user_id: int, course_id: int, day: int, module: int):
    """Отмечает модуль как пройденный в таблице user_progress."""
    async with pool.acquire() as conn:
        db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
        if not db_user_id:
            return
        sql = """
            INSERT INTO user_progress (user_id, course_id, day, module)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (user_id, course_id, day, module) DO NOTHING;
        """
        await conn.execute(sql, db_user_id, course_id, day, module)

async def advance_user_to_next_module(pool: asyncpg.Pool, telegram_id: int, current_day: int, current_module: int):
    """Передвигает закладку пользователя на следующий модуль или день."""
    next_day = current_day
    next_module = current_module + 1

    if next_module > 3:
        next_module = 1
        next_day += 1

    sql = "UPDATE users SET current_day = $1, current_module = $2 WHERE telegram_id = $3"
    async with pool.acquire() as conn:
        await conn.execute(sql, next_day, next_module, telegram_id)
    return next_day, next_module
        
async def get_all_courses_progress(pool: asyncpg.Pool, user_id: int):
    """
    Возвращает список словарей, каждый из которых содержит информацию о курсе 
    и количестве пройденных в нем модулей.
    """
    async with pool.acquire() as conn:
        db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
        if not db_user_id:
            return []

        sql = """
            SELECT c.id, c.title, c.emoji, COUNT(up.id) as modules_completed
            FROM courses c
            LEFT JOIN user_progress up ON c.id = up.course_id AND up.user_id = $1
            GROUP BY c.id, c.title, c.emoji
            ORDER BY c.id;
        """
        rows = await conn.fetch(sql, db_user_id)
        return [dict(row) for row in rows]

async def reset_progress_for_course(pool: asyncpg.Pool, user_id: int, course_id: int):
    """Удаляет ВЕСЬ прогресс пользователя по конкретному курсу."""
    async with pool.acquire() as conn:
        db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
        if not db_user_id:
            return

        sql_progress = "DELETE FROM user_progress WHERE user_id = $1 AND course_id = $2"
        sql_bookmark = "UPDATE users SET current_course_id = NULL, current_day = NULL, current_module = NULL WHERE telegram_id = $1 AND current_course_id = $2"
        async with conn.transaction():
            await conn.execute(sql_progress, db_user_id, course_id)
            await conn.execute(sql_bookmark, user_id, course_id)
        
async def get_all_completed_modules_for_course(pool: asyncpg.Pool, user_id: int, course_id: int):
    """Возвращает МНОЖЕСТВО кортежей (день, модуль) для всех пройденных модулей."""
    async with pool.acquire() as conn:
        db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
        if not db_user_id:
            return set()

        sql = "SELECT day, module FROM user_progress WHERE user_id = $1 AND course_id = $2"
        rows = await conn.fetch(sql, db_user_id, course_id)
        return {tuple(row) for row in rows}
        
async def save_assessment_result(pool: asyncpg.Pool, user_id: int, course_id: int, assessment_type: str, score: int, self_assessment: int):
    """Сохраняет результаты тестирования в базу данных."""
    async with pool.acquire() as conn:
        db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
        if not db_user_id:
            return

        sql = """
            INSERT INTO assessment_results (user_id, course_id, assessment_type, score, self_assessment_score)
            VALUES ($1, $2, $3, $4, $5);
        """
        await conn.execute(sql, db_user_id, course_id, assessment_type, score, self_assessment)
        
async def get_initial_assessment_result(pool: asyncpg.Pool, user_id: int, course_id: int):
    """Ищет результат начального тестирования для пользователя и курса."""
    async with pool.acquire() as conn:
        db_user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", user_id)
        if not db_user_id:
            return None

        sql = """
            SELECT id FROM assessment_results
            WHERE user_id = $1 AND course_id = $2 AND assessment_type = 'initial'
            LIMIT 1;
        """
        return await conn.fetchrow(sql, db_user_id, course_id)