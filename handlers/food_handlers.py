import os

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, ReplyKeyboardRemove
from spoonacular import detect_food
from main import bot

from tools import image_translator
from tools import UserState



router = Router()

SAVE_DIR = 'user_menu_photos'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


@router.message(UserState.waiting_for_photo, F.photo)
async def photo_handler(message: types.Message, state: FSMContext):
    await bot.download(
        message.photo[-1],
        destination=f"/tmp/{message.photo[-1].file_id}.jpg"
    )
    await state.update_data(photo_path=f"/tmp/{message.photo[-1].file_id}.jpg")
    await message.answer("Отлично! Теперь выберите язык для перевода:")
    await state.set_state(UserState.waiting_for_language)

@router.message(UserState.waiting_for_photo)
async def not_photo_handler(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup()
    start_button = types.KeyboardButton(text="/start")
    keyboard.add(start_button)
    await message.answer("Пришли мне фотографию меню или Нажми кнопку /start, чтобы начать сначала.",
                         reply_markup=keyboard)


@router.message(UserState.waiting_for_language)
async def process_language(message: Message, state: FSMContext):
    language_choice = message.text.strip().lower()
    await state.update_data(language=language_choice)

    user_data = await state.get_data()
    photo_path = user_data.get('photo_path')
    language = user_data.get('language', 'eng')

    text = image_translator(photo_path, language)
    os.remove(photo_path)

    matched_dishes = detect_food(text)
    await message.reply(f'Ваши блюда: \n{matched_dishes}')

    await state.clear()
