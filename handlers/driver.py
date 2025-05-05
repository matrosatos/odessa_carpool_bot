from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.buttons import driver_menu, back_menu
from database.db import add_ride, get_rides_by_driver, delete_ride_by_id
from datetime import datetime

router = Router()

class DriverStates(StatesGroup):
    from_addr = State()
    to_addr = State()
    date = State()
    time = State()
    seats = State()
    price = State()

# 🔘 Кнопка "Удалить"
def delete_button(ride_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🗑 Удалить",
                callback_data=f"delete:{ride_id}"
            )]
        ]
    )

# 🚘 Главное меню водителя
@router.message(lambda m: m.text == "🚘 Я водитель")
async def driver_menu_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=driver_menu())

# ➕ Добавить поездку — шаг 1
@router.message(lambda m: m.text == "➕ Добавить поездку")
async def driver_start(message: types.Message, state: FSMContext):
    await message.answer("Введите <b>улицу отправления</b>:")
    await state.set_state(DriverStates.from_addr)

@router.message(DriverStates.from_addr)
async def input_from(message: types.Message, state: FSMContext):
    await state.update_data(from_addr=message.text)
    await message.answer("Введите <b>улицу назначения</b>:")
    await state.set_state(DriverStates.to_addr)

@router.message(DriverStates.to_addr)
async def input_to(message: types.Message, state: FSMContext):
    await state.update_data(to_addr=message.text)
    await message.answer("Введите <b>дату поездки</b> (ДД.ММ.ГГГГ):")
    await state.set_state(DriverStates.date)

@router.message(DriverStates.date)
async def input_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Введите <b>время</b> (например, 14:30):")
    await state.set_state(DriverStates.time)

@router.message(DriverStates.time)
async def input_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("Сколько <b>свободных мест</b>?")
    await state.set_state(DriverStates.seats)

@router.message(DriverStates.seats)
async def input_seats(message: types.Message, state: FSMContext):
    await state.update_data(seats=message.text)
    await message.answer("Укажите <b>стоимость</b> за одного пассажира (грн):")
    await state.set_state(DriverStates.price)

@router.message(DriverStates.price)
async def input_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        date_obj = datetime.strptime(data["date"], "%d.%m.%Y").date()
    except ValueError:
        await message.answer("❗ Неверный формат даты. Используй ДД.ММ.ГГГГ")
        return

    await add_ride(
        driver_id=message.from_user.id,
        driver_user_id=message.from_user.id,
        driver_username=message.from_user.username or "неизвестно",
        from_addr=data["from_addr"],
        to_addr=data["to_addr"],
        date_str=date_obj.strftime("%Y-%m-%d"),
        time_str=data["time"],
        seats=int(data["seats"]),
        price=int(message.text),
    )

    await message.answer("🚘 Поездка добавлена! Спасибо!", reply_markup=driver_menu())
    await state.clear()

# 🧾 Мои поездки
@router.message(lambda m: m.text == "🧾 Мои поездки")
async def show_my_rides(message: types.Message):
    rides = await get_rides_by_driver(message.from_user.id)
    if not rides:
        await message.answer("У вас пока нет добавленных поездок.")
        return

    for ride in rides:
        text = (
            f"🆔 <b>{ride['id']}</b>\n"
            f"🚘 {ride['from_addr']} → {ride['to_addr']}\n"
            f"📅 {ride['date']} ⏰ {ride['time']}\n"
            f"💺 Мест: {ride['seats']} | 💰 {ride['price']} грн"
        )
        await message.answer(
            text=text,
            reply_markup=delete_button(ride['id'])
        )

# 🗑 Обработчик нажатия "Удалить"
@router.callback_query(lambda c: c.data.startswith("delete:"))
async def delete_ride_callback(callback: types.CallbackQuery):
    ride_id = int(callback.data.split(":")[1])
    await delete_ride_by_id(ride_id, callback.from_user.id)
    await callback.answer("Поездка удалена.")
    await callback.message.edit_text("❌ Поездка удалена.")
