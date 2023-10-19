from aiogram import Router,  types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tools import UserState

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    kb = [
        [
            types.KeyboardButton(text="/start"),
            types.KeyboardButton(text="Инструкция"),
            types.KeyboardButton(text="Начать сначала")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Загрузите фотографию или выберете команду снизу"
    )
    await message.answer("Привет! пришли мне фотографию меню",
                         reply_markup=keyboard)
    await state.set_state(UserState.waiting_for_photo)
