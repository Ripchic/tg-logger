import os
import time
import telebot
from telebot import types


class TelegramBot:
    def __init__(self, token: str, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.bot = telebot.TeleBot(token)
        self.tmp_dir = 'temp/'
        self.last_message_time = 0
        self.last_picture_time = 0
        self.last_structured_text_time = 0

    def _make_image_path(self, name: str = None):
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        file_name = f"{int(time.time()) if name is None else name}.png"
        return os.path.join(self.tmp_dir, file_name)

    def clean_tmp_dir(self):
        for f in os.listdir(self.tmp_dir):
            os.remove(os.path.join(self.tmp_dir, f))
        os.rmdir(self.tmp_dir)

    def send_message(self, text):
        return self.bot.send_message(chat_id=self.chat_id, text=text)

    def update_message(self, message, text, force: bool = False):
        current_time = time.time()
        if not force:
            if current_time - self.last_message_time < 1:
                return
        self.last_message_time = current_time
        return self.bot.edit_message_text(text=text, chat_id=self.chat_id, message_id=message.message_id)

    def send_plot(self, plt, name: str = None):
        img_path = self._make_image_path(name)
        plt.savefig(img_path, dpi=100)
        with open(img_path, 'rb') as img_file:
            return self.bot.send_photo(chat_id=self.chat_id, photo=img_file)

    def send_image(self, img_path: str):
        with open(img_path, 'rb') as img_file:
            return self.bot.send_photo(chat_id=self.chat_id, photo=img_file)

    def update_plot(self, message, plt, name: str = None, force: bool = False):
        current_time = time.time()
        if not force:
            if current_time - self.last_picture_time < 1:
                return
        self.last_picture_time = current_time
        img_path = self._make_image_path(name)
        plt.savefig(img_path, dpi=100)
        with open(img_path, 'rb') as img_file:
            return self.bot.edit_message_media(media=types.InputMediaPhoto(img_file), chat_id=self.chat_id,
                                               message_id=message.message_id)

    def send_structured_text(self, fields=[], values=[], units=[]):
        msg_text = '\n'.join(f"{field}: {round(value, 3) if isinstance(value, float) else value}{unit}"
                             for field, value, unit in zip(fields, values, units))
        return self.bot.send_message(self.chat_id, msg_text)

    def update_structured_text(self, message, fields=[], values=[], units=[], force: bool = False):
        current_time = time.time()
        if not force:
            if current_time - self.last_structured_text_time < 1:
                return
        self.last_structured_text_time = current_time
        msg_text = '\n'.join(f"{field}: {round(value, 2) if isinstance(value, float) else value}{unit}"
                             for field, value, unit in zip(fields, values, units))
        return self.bot.edit_message_text(msg_text, chat_id=self.chat_id, message_id=message.message_id)

    def send_txt(self):
        with open('temp/log.txt', 'rb') as f:
            return self.bot.send_document(chat_id=self.chat_id, document=f)

    def send_json(self):
        with open('temp/log.json', 'rb') as f:
            return self.bot.send_document(chat_id=self.chat_id, document=f)