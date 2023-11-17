from aiogram import Bot
from aiogram import Dispatcher
import asyncio

# from create_bot import dp
# from data_base import sqlite_db
from handlers import client, other

from aiogram.fsm.storage.memory import MemoryStorage
import os


async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(client.router)
    dp.include_router(other.router)
    # dp.startup.register(await bot.send_message(os.getenv('ADMIN'), text="Танцуй!"))
    print("Loaded!")
    await dp.start_polling(bot)
    # sqlite_db.sql_start()


if __name__ == "__main__":
    asyncio.run(main())

# client.register_handlers_client(dp)
# admin.register_handlers_admin(dp)
# other.register_handlers_other(dp)

# executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
