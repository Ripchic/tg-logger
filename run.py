from tg_logger import TelegramBot
from utils import TelegramTqdm
from time import sleep
import asyncio

TOKEN = ""
CHATID = 0
bot = TelegramBot(TOKEN, CHATID)
pb = TelegramTqdm(bot)
# asyncio.run(TelegramBot.main(bot))

for i in pb(range(20)):
    sleep(1)
