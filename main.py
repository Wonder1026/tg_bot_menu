import logging
import os
import asyncio
import tempfile

from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import F, types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from spoonacular import detect_dishes, get_single_item
from tools import image_translator
from googletrans import Translator
from tools import UserState

load_dotenv()

TG_API_TOKEN = os.getenv("TG_API_TOKEN")

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(TG_API_TOKEN)

translator = Translator()

language = 'eng'


class MyCallback(CallbackData, prefix='my'):
    dish: str
    action: bool


class LangCallback(CallbackData, prefix='lg'):
    lang: str
    act: bool


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    kb = [
        [
            types.KeyboardButton(text="/start"),
            types.KeyboardButton(text="Инструкция"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Загрузите фотографию или выберете команду снизу"
    )

    inline_keyboard = []
    languages = ['rus', 'eng', 'deu']
    for lang in languages:
        button = types.InlineKeyboardButton(text=lang,
                                            callback_data=LangCallback(lang=lang, act=True).pack())
        inline_keyboard.append([button])

    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await message.answer("выберите язык меню", reply_markup=reply_markup)


@dp.message(UserState.waiting_for_photo, F.photo)
async def photo_handler(message: types.Message, state: FSMContext, bot):
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, f"{message.photo[-1].file_id}.jpg")
    await bot.download(
        message.photo[-1],
        destination=temp_file_path
    )
    global language
    await state.update_data(photo_path=temp_file_path)
    text = image_translator(temp_file_path, lg=language)

    if text:
        eng_text = translator.translate(text, dest='en')

    matched_dishes = []
    if text:
        matched_dishes = detect_dishes(eng_text.text)


    inline_keyboard = []
    if matched_dishes:
        for dish in matched_dishes:
            new_dish = translator.translate(dish, dest='ru')
            button = types.InlineKeyboardButton(text=new_dish.text,
                                                callback_data=MyCallback(dish=dish, action=True).pack())
            inline_keyboard.append([button])
        reply_markup = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        await message.answer("Выберите блюдо из меню:", reply_markup=reply_markup)
    else:
        await message.answer("К сожалению, не удалось обнаружить блюдо. Попробуйте прислать другую фотографию")


@dp.message(UserState.waiting_for_photo)
async def not_photo_handler(message: types.Message, state: FSMContext):
    await message.answer("пришлите фотографию меню или выберите команду из menu")


@dp.callback_query(MyCallback.filter(F.action == True))
async def my_callback_foo(query: CallbackQuery, callback_data: MyCallback):
    items = get_single_item(callback_data.dish)
    photo_url = items[1]
    ing = ', '.join(items[0])

    try:
        trans = translator.translate(ing, dest='ru')
        await bot.send_photo(chat_id=query.message.chat.id, photo=photo_url)
        await query.message.answer(f'Ингредиенты: {trans.text.lower()}')

    except:
        await query.message.answer('Произошла ошибка при выполнении запроса')


@dp.callback_query(LangCallback.filter(F.act == True))
async def lang_callback(query: CallbackQuery, callback_data: LangCallback, state: FSMContext):
    global language
    language = callback_data.lang
    await query.message.answer("пришлите мне фотографию меню")
    await state.set_state(UserState.waiting_for_photo)


async def main():
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    asyncio.run(main())
