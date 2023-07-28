import logging
import re
import os

from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
import pytesseract as pt
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from spoonacular import detect_food
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

TG_API_TOKEN = os.getenv("TG_API_TOKEN")
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

logging.basicConfig(level=logging.INFO)



bot = Bot(token=TG_API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

SAVE_DIR = 'user_menu_photos'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


class UserState(StatesGroup):
    """
        Класс, определяющий состояния пользователя для управления диалогом с ботом.

        Состояния:
            waiting_for_photo: Ожидание фотографии от пользователя.
            waiting_for_language: Ожидание выбора языка пользователем.
            waiting_for_dish: Ожидание выбора блюда пользователем.
    """
    waiting_for_photo = State()
    waiting_for_language = State()
    waiting_for_dish = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply("Привет! пришли мне фотографию меню")
    await UserState.waiting_for_photo.set()


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=UserState.waiting_for_photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    photo_id = photo.file_id
    photo_file = await bot.get_file(photo_id)
    file_name = f"photo_{photo_id}.jpg"

    file_save_path = os.path.join(SAVE_DIR, file_name)
    await photo_file.download(file_save_path)
    await state.update_data(photo_path=file_save_path)
    await message.answer("Отлично! Теперь выберите язык для перевода:")
    await UserState.waiting_for_language.set()
    # text = image_translator(file_save_path, 'eng')
    # os.remove(file_save_path)
    # matched_dishes = detect_food(text)
    # await message.reply(f'ваши блюда: \n{matched_dishes}')


@dp.message_handler(state=UserState.waiting_for_language)
async def process_language(message: types.Message, state: FSMContext):
    language_choice = message.text.strip().lower()
    await state.update_data(language=language_choice)

    user_data = await state.get_data()
    photo_path = user_data.get('photo_path')
    language = user_data.get('language', 'eng')

    text = image_translator(photo_path, language)
    os.remove(photo_path)

    matched_dishes = detect_food(text)
    await message.reply(f'Ваши блюда: \n{matched_dishes}')

    await state.finish()

def image_translator(image, language='eng'):
    text = pt.image_to_string(image, lang=language).lower()
    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'[^a-zA-Zа-яА-Я\s]', '', text)
    return text


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
