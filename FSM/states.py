from aiogram.fsm.state import State, StatesGroup

class Onboarding(StatesGroup):
    """
    Класс состояний для онбординга пользователя.
    """
    q1_thoughts = State()      # Состояние для первого вопроса (мысли)
    q2_sleep = State()         # Состояние для второго вопроса (сон)
    q3_tasks = State()         # Состояние для третьего вопроса (дела)
    q4_emotions = State()      # Состояние для четвертого вопроса (эмоции)
    
class Assessment(StatesGroup):
    """
    Состояния для прохождения тестов до и после курса.
    """
    initial_assessment = State()
    final_assessment = State()
    
class ResetProgress(StatesGroup):
    """
    Состояние для подтверждения сброса прогресса.
    """
    confirming_reset = State()