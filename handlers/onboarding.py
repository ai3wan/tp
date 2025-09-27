from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import keyboards.reply as kb
from FSM.states import Onboarding

router = Router()

@router.message(Onboarding.q1_thoughts)
async def onboarding_q2(message: Message, state: FSMContext):
    await state.set_state(Onboarding.q2_sleep)
    await message.answer(
        "А как у тебя со сном? Легко засыпаешь или ворочаешься до утра?",
        reply_markup=kb.onboarding_q2_kb
    )

@router.message(Onboarding.q2_sleep)
async def onboarding_q3(message: Message, state: FSMContext):
    await state.set_state(Onboarding.q3_tasks)
    await message.answer(
        "Представь, что дел становится слишком много. Ты…",
        reply_markup=kb.onboarding_q3_kb
    )
    
@router.message(Onboarding.q3_tasks)
async def onboarding_q4(message: Message, state: FSMContext):
    await state.set_state(Onboarding.q4_emotions)
    await message.answer(
        "А бывает, что эмоции берут верх? То смеяться хочется, то злиться, то грустить без причины?",
        reply_markup=kb.onboarding_q4_kb
    )

@router.message(Onboarding.q4_emotions)
async def onboarding_final(message: Message, state: FSMContext):
    await state.clear()  # Очищаем состояние онбординга
    await message.answer(
        "💬 Знаешь, все эти состояния кажутся сложными, но они естественны — такое испытывает очень много людей...\n\n"
        "Мы создали специальный курс по работе с тревожностью, который поможет тебе научиться справляться с этими состояниями.\n\n"
        "Давай сначала пройдем короткий пульс тревожности, чтобы понять твой текущий уровень тревожности? Это поможет нам лучше подстроить курс под тебя.",
        reply_markup=kb.onboarding_final_kb
    )