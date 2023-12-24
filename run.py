from time import sleep
from tg_logger import TelegramBot
from utils import TGTqdm
import os

token = os.getenv('TOKEN')
chat_id = os.getenv('USER_ID')

bot = TelegramBot(token, chat_id)
TGTqdm = TGTqdm(bot, True)

for _ in TGTqdm(list([1, 2, 4, 5, 6])):
    sleep(2)
