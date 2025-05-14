from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧍 Я пасажир")],
            [KeyboardButton(text="🚘 Я водій")]
        ],
        resize_keyboard=True
    )

def passenger_date_menu(today: str, tomorrow: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"📅 Сьогодні — {today}")],
            [KeyboardButton(text=f"📆 Завтра — {tomorrow}")],
            [KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="❌ Відміна")],
            [KeyboardButton(text="🏠 Головне меню")]
        ],
        resize_keyboard=True
    )

def trips_result_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔁 Оновити")],
            [KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="❌ Відміна")],
            [KeyboardButton(text="🏠 Головне меню")]
        ],
        resize_keyboard=True
    )

def driver_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Додати поїздку")],
            [KeyboardButton(text="🧾 Мої поїздки")],
            [KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="🏠 Головне меню")]
        ],
        resize_keyboard=True
    )

def driver_date_menu(today: str, tomorrow: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"📅 Сьогодні — {today}")],
            [KeyboardButton(text=f"📆 Завтра — {tomorrow}")],
            [KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="❌ Відміна")],
            [KeyboardButton(text="🏠 Головне меню")]
        ],
        resize_keyboard=True
    )

def cancel_back_home_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="❌ Відміна")],
            [KeyboardButton(text="🏠 Головне меню")]
        ],
        resize_keyboard=True
    )
