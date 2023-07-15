import logging
import re
import os
from dotenv import load_dotenv
import pytesseract as pt
from aiogram import Bot, Dispatcher, executor, types
from spoonacular import detect_food

load_dotenv()

TG_API_TOKEN = os.getenv("TG_API_TOKEN")
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot)


SAVE_DIR = 'user_menu_photos'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! пришли мне фотографию меню")


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def process_photo(message: types.Message):
    file_path = r"C:\Users\Oleg\Desktop\new_menu.txt"
    photo = message.photo[-1]
    photo_id = photo.file_id
    photo_file = await bot.get_file(photo_id)
    file_name = f"photo_{photo_id}.jpg"
    file_save_path = os.path.join(SAVE_DIR, file_name)
    await photo_file.download(file_save_path)
    text = image_translator(file_save_path)
    matched_dishes = detect_food(text)
    # matched_dishes = find_matching_dishes(text, file_path)
    await message.reply(f'ваши блюда: \n{matched_dishes}')


def image_translator(image):
    text = pt.image_to_string(image, lang='eng').lower()
    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'[^a-zA-Zа-яА-Я\s]', '', text)
    return text


def find_matching_dishes(input_string, file_path):
    matching_dishes = []
    with open(file_path, 'r') as file:
        for line in file:
            dish = line.strip()
            if dish.lower() in input_string.lower():
                matching_dishes.append(dish)
    return matching_dishes


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
