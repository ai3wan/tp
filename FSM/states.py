from aiogram.fsm.state import State, StatesGroup

class Onboarding(StatesGroup):
    """
    Класс состояний для онбординга пользователя.
    """
    q1_thoughts = State()      # Состояние для первого вопроса (мысли)
    q2_sleep = State()         # Состояние для второго вопроса (сон)
    q3_tasks = State()         # Состояние для третьего вопроса (дела)
    q4_emotions = State()      # Состояние для четвертого вопроса (эмоции)
    final = State()            # Состояние для финального сообщения
    
class CourseSelection(StatesGroup):
    """
    Состояние для выбора и подтверждения курса.
    """
    confirming_choice = State()
    
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
    
# FSM/states.py
# ...

class Assessment(StatesGroup):
    """
    Состояния для прохождения тестов до и после курса.
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