import os
import tempfile

from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

import aiogram.utils.markdown as md

from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from spoonacular import detect_food
from aiogram.utils.markdown import link
from aiogram.utils.keyboard import InlineKeyboardBuilder
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

    # formatted_words = [md.hlink(word, url=f'tg://msg?text={word}') for word in matched_dishes]
    # formatted_words = [f"[{word}](tg://msg?text={word})" for word in matched_dishes]
    formatted_dishes = [f"[{dish}](tg://msg?text={dish})" for dish in matched_dishes]
    formatted_message = ', '.join(formatted_dishes)
    # text = link('VK', 'https://vk.com')
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="GitHub", url="https://github.com")
    )
    builder.row(types.InlineKeyboardButton(
        text="Оф. канал Telegram",
        url="tg://resolve?domain=telegram")
    )

    # Чтобы иметь возможность показать ID-кнопку,
    # У юзера должен быть False флаг has_private_forwards

    await message.answer(
        'Выберите ссылку',
        reply_markup=builder.as_markup(),
    )


# await message.reply('<a href="https://vk.com/id41732290">VK</a>', parse_mode="HTML")
    #
    # await message.answer(formatted_message, parse_mode=ParseMode.MARKDOWN)
    # print(matched_dishes)
    # await message.reply(f'Ваши блюда: \n{matched_dishes}')
    # await state.clear()


@router.message(UserState.waiting_for_photo)
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
    # keyboard = types.ReplyKeyboardMarkup()
    # start_button = types.KeyboardButton(text="/start")
    # keyboard.add(start_button)
    # await message.answer("Пришли мне фотографию меню или Нажми кнопку /start, чтобы начать сначала.",
    await message.answer("not photo handler")
    #                      reply_markup=keyboard)

