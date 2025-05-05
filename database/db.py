import aiosqlite
from config import DB_PATH
from datetime import date

# Создание таблицы
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS rides (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_id INTEGER,
                driver_user_id INTEGER,
                driver_username TEXT,
                from_addr TEXT,
                to_addr TEXT,
                date TEXT,
                time TEXT,
                seats INTEGER,
                price INTEGER
            )
        """)
        await db.commit()

# Добавление поездки
async def add_ride(driver_id, driver_user_id, driver_username, from_addr, to_addr, date_str, time_str, seats, price):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO rides (driver_id, driver_user_id, driver_username, from_addr, to_addr, date, time, seats, price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (driver_id, driver_user_id, driver_username, from_addr, to_addr, date_str, time_str, seats, price))
        await db.commit()

# Поиск поездок по дате
async def get_rides_by_date(date_obj: date):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM rides WHERE date = ?", (date_obj.strftime("%Y-%m-%d"),))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_rides_by_driver(driver_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM rides WHERE driver_id = ?", (driver_id,))
        return [dict(row) for row in await cursor.fetchall()]

async def delete_ride_by_id(ride_id: int, driver_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM rides WHERE id = ? AND driver_id = ?",
            (ride_id, driver_id)
        )
        await db.commit()
