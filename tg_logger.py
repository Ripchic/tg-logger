import telebot
import logging


class TelegramBot:
    def __init__(self, token: str, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.bot = telebot.TeleBot(token)
        self.logger = telebot.logger
        # telebot.logger.setLevel(logging.DEBUG)

    def send_message(self, text):
        return self.bot.send_message(self.chat_id, text)

    def update_message(self, message, text):
        return self.bot.edit_message_text(text, chat_id=self.chat_id, message_id=message.message_id)
