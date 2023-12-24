from time import sleep
from tg_logger import TelegramBot
from utils import TGTqdm

token = ""
chat_id = ""

bot = TelegramBot(token, chat_id)
TGTqdm = TGTqdm(bot, True)

for _ in TGTqdm(range(154//2)):
    sleep(0.1)
