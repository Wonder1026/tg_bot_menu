import logging
import os
import asyncio

# from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import food_handlers, start_handler

load_dotenv()

TG_API_TOKEN = os.getenv("TG_API_TOKEN")

# dp = Dispatcher(storage=MemoryStorage())
# bot = Bot(TG_API_TOKEN)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(TG_API_TOKEN)
    dp.include_router(start_handler.router)
    dp.include_router(food_handlers.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())
