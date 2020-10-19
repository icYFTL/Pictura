from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from core import msg

def collect_new_pack() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(msg['collect_new_pack_button'])
            ],
            [
                KeyboardButton(msg['cancel_button'])
            ]
        ],
        resize_keyboard=True
    )