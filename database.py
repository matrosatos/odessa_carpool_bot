import aiosqlite
from typing import List, Tuple

DB_NAME = "carshare.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT,
                start_address TEXT NOT NULL,
                end_address TEXT NOT NULL,
                seats INTEGER,
                price TEXT,
                user_id INTEGER NOT NULL
            )
        """)
        await db.commit()

async def add_trip(
    role: str,
    date: str,
    time: str,
    start: str,
    end: str,
    seats: int,
    price: str,
    user_id: int
):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO trips (
                role, date, time, start_address,
                end_address, seats, price, user_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (role, date, time, start, end, seats, price, user_id))
        await db.commit()

async def get_trips_by_date(date: str) -> List[Tuple]:
    """
    Возвращает список поездок (id, time, start_address, end_address, price, user_id)
    для роли 'driver' на указанную дату.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT
                id,
                time,
                start_address,
                end_address,
                price,
                user_id
            FROM trips
            WHERE date = ? AND role = 'driver'
            ORDER BY time ASC
        """, (date,))
        return await cursor.fetchall()

async def get_trips_by_user(user_id: int) -> List[Tuple]:
    """
    Возвращает список поездок (id, date, time, start_address, end_address, price)
    добавленных данным водителем.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT
                id,
                date,
                time,
                start_address,
                end_address,
                price
            FROM trips
            WHERE user_id = ? AND role = 'driver'
            ORDER BY date, time
        """, (user_id,))
        return await cursor.fetchall()
