import os
import shutil
import time
import telebot
from telebot import types
import logging


class TelegramBot:
    def __init__(self, token: str, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.bot = telebot.TeleBot(token)
        self.logger = telebot.logger
        self.tmp_dir = './temp/'

        # telebot.logger.setLevel(logging.DEBUG)

    # @self.bot.message_handler(commands=['start'])
    # def start_message(self, message):
    #     return self.bot.send_message(message.chat.id, 'Привет')

    def send_message(self, text):
        return self.bot.send_message(self.chat_id, text)

    def update_message(self, message, text):
        return self.bot.edit_message_text(text, chat_id=self.chat_id, message_id=message.message_id)

    def send_plot(self, plt, name: str = None):

        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        if name is None:
            ts = int(time.time())
            img_path = self.tmp_dir+str(ts)+'.png'
        else:
            img_path = self.tmp_dir+name

        plt.savefig(img_path, dpi=100)
        return self.bot.send_photo(self.chat_id, open(img_path, 'rb'))

    def send_image(self, img_path: str):
        return self.bot.send_photo(self.chat_id, open(img_path, 'rb'))

    def update_plot(self, message, plt, name: str = None):
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        if name is None:
            ts = int(time.time())
            img_path = self.tmp_dir+str(ts)+'.png'
        else:
            img_path = self.tmp_dir+name

        plt.savefig(img_path, dpi=100)
        try:
            self.bot.edit_message_media(message_id=message.id, chat_id=self.chat_id,
                                        media=types.InputMediaPhoto(open(img_path, 'rb')))
        except Exception as e:
            pass




    # def clean_tmp_dir(self):
    #     """
    #     Delete temporary folder function.
    #     """
    #     shutil.rmtree(self.tmp_dir)