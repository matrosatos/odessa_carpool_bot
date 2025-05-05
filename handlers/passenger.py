from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import get_rides_by_date
from keyboards.buttons import back_menu
from datetime import datetime

router = Router()

class PassengerStates(StatesGroup):
    waiting_for_date = State()

def write_to_driver_button(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="✉️ Написать водителю",
                url=f"https://t.me/user?id={user_id}"
            )]
        ]
    )

@router.message(lambda m: m.text == "🧍 Я пассажир")
async def passenger_start(message: types.Message, state: FSMContext):
    await message.answer("Введите дату поездки в формате <b>ДД.ММ.ГГГГ</b>:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(PassengerStates.waiting_for_date)

@router.message(PassengerStates.waiting_for_date)
async def passenger_date_input(message: types.Message, state: FSMContext):
    try:
        date_obj = datetime.strptime(message.text, "%d.%m.%Y").date()
    except ValueError:
        await message.answer("❗ Неверный формат даты. Попробуйте снова: <b>ДД.ММ.ГГГГ</b>")
        return

    rides = await get_rides_by_date(date_obj)

    if not rides:
        await message.answer("😔 На эту дату нет доступных поездок.", reply_markup=back_menu())
    else:
        for ride in rides:
            text = (
                f"🚘 <b>{ride['from_addr']}</b> → <b>{ride['to_addr']}</b>\n"
                f"🕒 {ride['time']}, 💺 мест: {ride['seats']}, 💰 {ride['price']} грн\n"
            )
            await message.answer(
                text=text,
                reply_markup=write_to_driver_button(ride['driver_user_id'])
            )

    await state.clear()
