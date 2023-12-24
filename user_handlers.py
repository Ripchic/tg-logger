from tg_logger import TelegramBot
from keras_example import keras_example
import os

token = os.getenv('TOKEN')

bot = TelegramBot(token, None).bot


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user

    bot.send_message(message.chat.id, text=f"Hey, {user.first_name}! 👋\n\nI'm your personal assistant📕 for logging "
                                           f"models📝, so let's get started!\n\nFirst of all, you should find out "
                                           f"your /chat_id, which you will specify in the Python🐍 project, "
                                           f"and then you can run the model using the /running_the_model "
                                           f"command.\n\nIf anything, call for /help, and I will immediately rush to "
                                           f"your rescue! ⛑")


@bot.message_handler(commands=['chat_id'])
def chat_id(message):
    bot.send_message(message.chat.id, f"⬇️ Your ID:")
    bot.send_message(message.chat.id, f"{message.chat.id}")


@bot.message_handler(commands=['running_the_model'])
def running_the_model(message):
    bot.send_message(message.chat.id, f"<i>~Starting model training...</i>", parse_mode='HTML')
    keras_example(token=token, user_id=os.getenv('CHAT_ID'), n_epochs=15)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"Of course! Here is a list of possible commands:\n\n"
                                      f"/start — Getting started\n\n"
                                      f"/chat_id — Find out your Chat ID\n\n"
                                      f"/help — Help")


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, f"I don't understand... But maybe you will be satisfied that the 🅰️nswer to the "
                                      f"Main question of Life, the Universe and everything else is 42! 🪐 ✨\n\nIf "
                                      f"that's not enough, use /help 🛟")


bot.polling()
