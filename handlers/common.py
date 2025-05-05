from aiogram import Router, types
from aiogram.filters import Command
from keyboards.buttons import main_menu

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    text = (
        "<b>Привет!</b>\n\n"
        "Я — бот для поиска попутчиков по Одессе 🚗\n\n"
        "Ты можешь:\n"
        "— 🧍 Найти поездку как пассажир\n"
        "— 🚘 Добавить поездку как водитель\n\n"
        "Выбери действие ниже:"
    )
    await message.answer(text, reply_markup=main_menu())
from keyboards.buttons import main_menu
from aiogram.fsm.context import FSMContext

@router.message(lambda m: m.text == "⬅️ Назад")
async def back_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🔙 Возвращаемся в главное меню:", reply_markup=main_menu())
