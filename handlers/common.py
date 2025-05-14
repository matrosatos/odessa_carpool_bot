from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.buttons import main_menu

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    print("🔥 /start вызван")
    await state.clear()
    await message.answer("👋 Вітаю! Оберіть роль:", reply_markup=main_menu())
    
@router.message(F.text == "🏠 Головне меню")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🏠 Ви в головному меню.", reply_markup=main_menu())
