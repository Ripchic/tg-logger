from tg_logger import TelegramBot
import subprocess
import os

token = os.getenv('TOKEN')

bot = TelegramBot(token, None).bot


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user

    bot.send_message(message.chat.id, text=f"Hey, {user.first_name}! I'm your personal assistant for logging models, "
                                           f"so let's get started!\n\nFirst of all, you should find out your /chat_id, "
                                           f"which you will specify in the Python project, and then you can run the "
                                           f"model using the /running_the_model command.\n\nIf anything, call for "
                                           f"/help, and I will immediately rush to your rescue!")


@bot.message_handler(commands=['chat_id'])
def chat_id(message):
    bot.send_message(message.chat.id, f"Your ID:")
    bot.send_message(message.chat.id, f"{message.chat.id}")


@bot.message_handler(commands=['running_the_model'])
def running_the_model(message):
    # subprocess.run(['python', 'example.py'])

    bot.send_message(message.chat.id, f"<i>~Starting model training...</i>", parse_mode='HTML')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"Of course! Here is a list of possible commands:\n\n"
                                      f"/start - Getting started\n\n"
                                      f"/chat_id - Find out your Chat ID\n\n"
                                      f"/help - Help")


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, f"I don't understand... But maybe you will be satisfied that the Answer to the "
                                      f"Main question of Life, the Universe and everything else is 42!")


bot.polling()
