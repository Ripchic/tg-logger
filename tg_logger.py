import os
import time
import telebot
from telebot import types


class TelegramBot:
    def __init__(self, token: str, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.bot = telebot.TeleBot(token)
        self.logger = telebot.logger
        self.tmp_dir = 'temp/'

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

    def update_message(self, message, text):
        return self.bot.edit_message_text(text=text, chat_id=self.chat_id, message_id=message.message_id)

    def send_plot(self, plt, name: str = None):
        img_path = self._make_image_path(name)
        plt.savefig(img_path, dpi=100)
        with open(img_path, 'rb') as img_file:
            return self.bot.send_photo(chat_id=self.chat_id, photo=img_file)

    def send_image(self, img_path: str):
        with open(img_path, 'rb') as img_file:
            return self.bot.send_photo(chat_id=self.chat_id, photo=img_file)

    def update_plot(self, message, plt, name: str = None):
        img_path = self._make_image_path(name)
        plt.savefig(img_path, dpi=100)
        try:
            with open(img_path, 'rb') as img_file:
                self.bot.edit_message_media(message_id=message.id, chat_id=self.chat_id,
                                            media=types.InputMediaPhoto(img_file))
        except Exception as e:
            self.logger.error(f"Error updating plot: {e}")

    def send_structured_text(self, fields=[], values=[], units=[]):
        msg_text = '\n'.join(f"{field}: {round(value, 3) if isinstance(value, float) else value}{unit}"
                             for field, value, unit in zip(fields, values, units))
        return self.bot.send_message(self.chat_id, msg_text)

    def update_structured_text(self, message, fields=[], values=[], units=[]):
        msg_text = '\n'.join(f"{field}: {round(value, 2) if isinstance(value, float) else value}{unit}"
                             for field, value, unit in zip(fields, values, units))
        return self.bot.edit_message_text(msg_text, chat_id=self.chat_id, message_id=message.message_id)
