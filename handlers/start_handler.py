from aiogram import Router,  types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tools import UserState

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Привет! пришли мне фотографию меню",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.waiting_for_photo)
