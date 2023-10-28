import re
import pytesseract as pt
from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    """
        Класс, определяющий состояния пользователя для управления диалогом с ботом.

        Состояния:
            waiting_for_photo: Ожидание фотографии от пользователя.
            waiting_for_language: Ожидание выбора языка пользователем.
            waiting_for_dish: Ожидание выбора блюда пользователем.
    """
    waiting_for_photo = State()
    waiting_for_dish = State()


def image_translator(image):
    text = pt.image_to_string(image).lower()
    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'[^a-zA-Zа-яА-Я\s]', '', text)
    return text





