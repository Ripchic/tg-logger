from time import sleep
from tg_logger import TelegramBot
from utils import TGTqdm

token = ""
# chat_id =

bot = TelegramBot(token)
TGTqdm = TGTqdm(bot, True)

for _ in TGTqdm(range(3)):
    sleep(2)
