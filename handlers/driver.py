from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime, timedelta

from keyboards.buttons import (
    driver_menu,
    driver_date_menu,
    cancel_back_home_menu
)
from database import get_trips_by_user, add_trip

router = Router()

# ─── МЕНЮ ВОДІЯ ───────────────────────────────────────

@router.message(F.text == "🚘 Я водій")
async def driver_menu_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🔧 Меню водія:", reply_markup=driver_menu())

# ─── МОЇ ПОЇЗДКИ ───────────────────────────────────────

@router.message(F.text == "🧾 Мої поїздки")
async def my_trips(message: Message):
    trips = await get_trips_by_user(message.from_user.id)
    if not trips:
        await message.answer("У вас ще немає збережених поїздок.", reply_markup=driver_menu())
    else:
        result = "\n\n".join([
            f"🗓 {date} ⏰ {time}\n{start} → {end}\n💰 {price}₴"
            for _, date, time, start, end, price in trips
        ])
        await message.answer(f"<b>Ваші поїздки:</b>\n\n{result}", reply_markup=driver_menu())

# ─── FSM СТАНИ ДЛЯ ДОДАВАННЯ ПОЇЗДКИ ─────────────────

class DriverStates(StatesGroup):
    choosing_date = State()
    input_time = State()
    input_start = State()
    input_end = State()
    choosing_seats = State()
    input_price = State()

# ─── ДОДАТИ ПОЇЗДКУ ────────────────────────────────────

@router.message(F.text == "➕ Додати поїздку")
async def add_trip_start(message: Message, state: FSMContext):
    today = datetime.now().strftime("%d.%m.%Y")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
    await state.set_state(DriverStates.choosing_date)
    await message.answer(
        "🗓 Оберіть дату поїздки:",
        reply_markup=driver_date_menu(today, tomorrow)
    )

@router.message(DriverStates.choosing_date)
async def choose_date(message: Message, state: FSMContext):
    text = message.text
    if "Сьогодні" in text:
        date = datetime.now().strftime("%Y-%m-%d")
    elif "Завтра" in text:
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    elif text in ["⬅️ Назад", "❌ Відміна", "🏠 Головне меню"]:
        await state.clear()
        await message.answer("🚪 Скасовано / Повернення до меню", reply_markup=driver_menu())
        return
    else:
        await message.answer("❌ Будь ласка, оберіть дату з кнопок.", reply_markup=driver_date_menu(
            datetime.now().strftime("%d.%m.%Y"),
            (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
        ))
        return

    await state.update_data(date=date)
    await state.set_state(DriverStates.input_time)
    await message.answer("⏰ Введіть час поїздки (наприклад, 14:30):", reply_markup=cancel_back_home_menu())

@router.message(DriverStates.input_time)
async def input_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(DriverStates.input_start)
    await message.answer("📍 Звідки виїжджаєте?", reply_markup=cancel_back_home_menu())

@router.message(DriverStates.input_start)
async def input_end(message: Message, state: FSMContext):
    await state.update_data(start=message.text)
    await state.set_state(DriverStates.input_end)
    await message.answer("📍 Куди їдете?", reply_markup=cancel_back_home_menu())

@router.message(DriverStates.input_end)
async def input_seats(message: Message, state: FSMContext):
    await state.update_data(end=message.text)
    await state.set_state(DriverStates.choosing_seats)
    await message.answer("🚗 Скільки вільних місць?", reply_markup=cancel_back_home_menu())

@router.message(DriverStates.choosing_seats)
async def input_price(message: Message, state: FSMContext):
    await state.update_data(seats=message.text)
    await state.set_state(DriverStates.input_price)
    await message.answer("💰 Вкажіть ціну за поїздку (наприклад, 100):", reply_markup=cancel_back_home_menu())

@router.message(DriverStates.input_price)
async def save_trip(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()

    await add_trip(
        role="driver",
        date=data["date"],
        time=data["time"],
        start=data["start"],
        end=data["end"],
        seats=int(data["seats"]),
        price=data["price"],
        user_id=message.from_user.id
    )
    await state.clear()
    await message.answer("✅ Поїздку збережено!", reply_markup=driver_menu())