from tg_logger import TelegramBot

token = ""

bot = TelegramBot(token, None).bot


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет!\n Я ваш личный помощник для логгирования моделей")


@bot.message_handler(commands=['chat_id'])
def chat_id(message):
    bot.send_message(message.chat.id, f"Ваш chat_id: {message.chat.id}")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"Вот список команд:\n"
                                      f"/start - начало работы\n"
                                      f"/chat_id - узнать свой chat_id\n"
                                      f"/help - помощь")


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, f"Вы хотите от меня невозможного")


bot.polling()
