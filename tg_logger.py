import asyncio
import logging
import sys
# from os import getenv

from aiogram import Bot, Dispatcher, types, Router
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart
# from aiogram.types import Message
# from aiogram.utils.markdown import hbold


import user_handlers


class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.bot = Bot(token=self.token)
        self.chat_id = chat_id

    async def send_message(self, text):
        await self.bot.send_message(chat_id=self.chat_id, text=text)

    async def edit_message(self, message_id, text):
        await self.bot.edit_message_text(chat_id=self.chat_id, message_id=message_id, text=text)

    async def main(self) -> None:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        dp = Dispatcher()
        bot = Bot(token=self.token)
        dp.include_router(user_handlers.router)
        await self.send_message(text = "I'm alive!\nWrite /start to initialize chat_id for bot")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

# if __name__ == "__main__":
#     TOKEN = ""
#     CHATID = 0
#     telegram_bot = TelegramBot(TOKEN, CHATID)
#     asyncio.run(telegram_bot.main())
