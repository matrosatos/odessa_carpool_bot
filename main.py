import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

from config import BOT_TOKEN
from database.db import init_db
from handlers import common, passenger, driver

logging.basicConfig(level=logging.INFO)

# ─── HTTP-сервер ────────────────────────────────────────────────
async def handle(request):
    return web.Response(text="Bot is running!")

async def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# ─── Основной async запуск ──────────────────────────────────────
async def main():
    await init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()
    dp.include_routers(common.router, passenger.router, driver.router)

    # Запуск бота и веб-сервера параллельно
    await asyncio.gather(
        dp.start_polling(bot),
        run_web_server()
    )

if __name__ == "__main__":
    asyncio.run(main())
