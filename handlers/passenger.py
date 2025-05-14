from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime, timedelta

from keyboards.buttons import passenger_date_menu, main_menu, trips_result_menu
from database import get_trips_by_date

router = Router()

class PassengerStates(StatesGroup):
    choosing_date = State()

@router.message(F.text == "🧍 Я пасажир")
async def passenger_start(message: Message, state: FSMContext):
    today = datetime.now().strftime("%d.%m.%Y")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
    await state.set_state(PassengerStates.choosing_date)
    await message.answer(
        "Оберіть дату поїздки:",
        reply_markup=passenger_date_menu(today, tomorrow)
    )

@router.message(PassengerStates.choosing_date)
async def show_trips(message: Message, state: FSMContext):
    text = message.text

    # Определяем дату
    if text.startswith("📅 Сьогодні"):
        date = datetime.now().strftime("%Y-%m-%d")
    elif text.startswith("📆 Завтра"):
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    elif text == "🔁 Оновити":
        data = await state.get_data()
        date = data.get("date")
        if not date:
            await message.answer("Спочатку оберіть дату.", reply_markup=main_menu())
            return
    elif text == "🏠 Головне меню":
        await state.clear()
        await message.answer("🏠 Ви в головному меню.", reply_markup=main_menu())
        return
    elif text in ["⬅️ Назад", "❌ Відміна"]:
        await state.clear()
        await message.answer("🚪 Скасовано.", reply_markup=main_menu())
        return
    else:
        # Неправильный ввод – предлагаем выбор снова
        today = datetime.now().strftime("%d.%m.%Y")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
        await message.answer(
            "Будь ласка, оберіть дату з кнопок.",
            reply_markup=passenger_date_menu(today, tomorrow)
        )
        return

    # Сохраняем и выводим поездки
    await state.update_data(date=date)
    trips = await get_trips_by_date(date)

    if not trips:
        await message.answer(
            "На цю дату поїздок ще немає 😕",
            reply_markup=trips_result_menu()
        )
    else:
        lines = []
        for _, time, start, end, price, user_id in trips:
            lines.append(
                f"🚗 <b>{time}</b>\n"
                f"{start} → {end}\n"
                f"💰 {price}₴\n"
                f"✉ <a href='tg://user?id={user_id}'>Написати водію</a>"
            )
        result = "\n\n".join(lines)
        await message.answer(
            f"<b>Доступні поїздки на {date}:</b>\n\n{result}",
            reply_markup=trips_result_menu()
        )

    await state.clear()
