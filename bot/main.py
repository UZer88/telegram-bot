import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import BOT_TOKEN
from bot.handlers import start, tasks, help
from bot.database.database import AsyncSessionLocal

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Middleware для передачи сессии БД
    @dp.update.middleware()
    async def db_session_middleware(handler, event, data):
        async with AsyncSessionLocal() as session:
            data["session"] = session
            return await handler(event, data)

    dp.include_router(start.router)
    dp.include_router(tasks.router)
    dp.include_router(help.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())