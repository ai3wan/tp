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
    Состояния для прохождения пульса тревожности до и после курса.
    """
    initial_assessment = State()
    final_assessment = State()
    
class ResetProgress(StatesGroup):
    """
    Состояние для подтверждения сброса прогресса.
    """
    confirming_reset = State()

class Day2Module2States(StatesGroup):
    """
    Состояния для второго дня, второго модуля.
    Притча Эзопа о луке и практика расслабления.
    """
    step_1 = State()  # Введение в притчу
    step_2 = State()  # Начало притчи - Эзоп играет с детьми
    step_3 = State()  # Эзоп берет лук
    step_4 = State()  # Мораль притчи
    step_5 = State()  # Переход к практике
    step_6 = State()  # Мышечная релаксация