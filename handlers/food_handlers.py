import os
import tempfile

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, ReplyKeyboardRemove
from spoonacular import detect_food

from tools import image_translator
from tools import UserState

from googletrans import Translator


translator = Translator()
router = Router()

@router.message(UserState.waiting_for_photo, F.photo)
async def photo_handler(message: types.Message, state: FSMContext, bot):
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, f"{message.photo[-1].file_id}.jpg")
    await bot.download(
        message.photo[-1],
        destination=temp_file_path
    )

    await state.update_data(photo_path=temp_file_path)
    text = image_translator(temp_file_path)
    eng_text = translator.translate(text, dest='en')
    matched_dishes = detect_food(eng_text.text)
    print(matched_dishes)
    await message.reply(f'Ваши блюда: \n{matched_dishes}')
    await state.clear()

@router.message(UserState.waiting_for_photo)
async def not_photo_handler(message: types.Message, state: FSMContext):
    # keyboard = types.ReplyKeyboardMarkup()
    # start_button = types.KeyboardButton(text="/start")
    # keyboard.add(start_button)
    # await message.answer("Пришли мне фотографию меню или Нажми кнопку /start, чтобы начать сначала.",
    await message.answer("Пришли мне фотографию меню или Нажми кнопку /start, чтобы начать сначала.")
    #                      reply_markup=keyboard)

