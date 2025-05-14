from aiogram import Dispatcher
from .common import router as common_router
from .passenger import router as passenger_router
from .driver import router as driver_router

def register_handlers(dp: Dispatcher):
    print("✅ Registering routers...")  # добавь это!
    dp.include_router(common_router)
    dp.include_router(passenger_router)
    dp.include_router(driver_router)

