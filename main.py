import logging
import os
import asyncio
import tempfile

from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
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


class MyCallback(CallbackData, prefix='my'):
    dish: str
    action: bool


@dp.message(Command("start"))
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


@dp.message(UserState.waiting_for_photo, F.photo)
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
    matched_dishes = detect_dishes(eng_text.text)
    # formatted_dishes = [f"[{dish}](tg://msg?text={dish})" for dish in matched_dishes]
    # formatted_message = ', '.join(formatted_dishes)

    inline_keyboard = []

    for dish in matched_dishes:
        button = types.InlineKeyboardButton(text=dish,
                                            callback_data=MyCallback(dish=dish, action=True).pack())
        inline_keyboard.append([button])
    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await message.answer("Выберите блюдо из меню:", reply_markup=reply_markup)


@dp.message(UserState.waiting_for_photo)
async def not_photo_handler(message: types.Message, state: FSMContext):
    if message.text == 'Инструкция':
        await message.answer(
            """
            Инструкция:
- Загрузите изображение вашего меню
- Бот обработает фотографию и вернет список блюд
- Выберите блюдо, которое вас интересует и нажмите на него или отправьте цифру, соответствующую нужному блюду
- Бот вернет вам подробную информацию о выбранном блюде
            """)
    await message.answer("not photo handler")



# @dp.callback_query(MyCallback.filter(F.action == True))
@dp.callback_query(MyCallback.filter(F.action == True))
async def my_callback_foo(query: CallbackQuery, callback_data: MyCallback):
    items = get_single_item(callback_data.dish)
    photo_url = items['image_url']
    print(photo_url)
    await bot.send_photo(chat_id=query.message.chat.id, photo=photo_url)

    # photo = InputFile(callback_data.photo_url)
    # await query.message.send_photo(chat_id, photo)
    # get_dish(callback_data.dish)
    # await query.message.answer('asdffdsafdsa')


async def main():
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    asyncio.run(main())

