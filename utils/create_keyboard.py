from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CreateKeyboard:
    def __init__(self):
        """Инициализация класса CreateKeyboard."""
        pass

    @staticmethod
    async def create_keyboard(buttons, columns=1):
        keyboard_buttons = []
        for i in range(0, len(buttons), columns):
            row = [
                types.KeyboardButton(text=button) for button in buttons[i : i + columns]
            ]
            keyboard_buttons.append(row)
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=keyboard_buttons, resize_keyboard=True
        )
        return keyboard


create_kb = CreateKeyboard()
