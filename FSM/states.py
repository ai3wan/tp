from aiogram.fsm.state import State, StatesGroup

class Onboarding(StatesGroup):
    """
    Состояния для онбординга (знакомства) с пользователем.
    """
    q1_thoughts = State()
    q2_sleep = State()
    q3_tasks = State()
    q4_emotions = State()
    final = State()

class CourseSelection(StatesGroup):
    """
    Состояния для выбора и подтверждения курса.
    """
    confirming_choice = State()

class AnxietyTest(StatesGroup):
    """
    Состояния для прохождения теста на тревожность (начального и финального).
    """
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

class ResetProgress(StatesGroup):
    """
    Состояние для подтверждения сброса прогресса.
    """
    confirming_reset = State()