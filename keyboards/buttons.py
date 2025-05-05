from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = [
        [KeyboardButton(text="🧍 Я пассажир")],
        [KeyboardButton(text="🚘 Я водитель")],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def back_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ Назад")]],
        resize_keyboard=True
    )

def driver_menu():
    kb = [
        [KeyboardButton(text="➕ Добавить поездку")],
        [KeyboardButton(text="🧾 Мои поездки")],
        [KeyboardButton(text="⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
