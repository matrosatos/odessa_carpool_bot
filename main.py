import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from database.db import init_db
from handlers import common, passenger, driver
from config import BOT_TOKEN

# Для HTTP-сервера Render
from aiohttp import web
import threading

logging.basicConfig(level=logging.INFO)

# --- Телеграм-бот ---
async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Удаляем возможный старый webhook
    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()
    dp.include_routers(
        common.router,
        passenger.router,
        driver.router,
    )

    await dp.start_polling(bot)

# --- HTTP-сервер (для Render) ---
async def handle(request):
    return web.Response(text="Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", handle)
    web.run_app(app, port=port)

# --- Запуск ---
if __name__ == "__main__":
    # Запуск бота в отдельном потоке
    threading.Thread(target=lambda: asyncio.run(main())).start()

    # Запуск HTTP-сервера (чтобы Render видел открытый порт)
    run_web_server()
