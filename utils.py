from tg_logger import TelegramBot
from datetime import datetime
from tqdm import tqdm


class _TelegramIO:
    def __init__(self, bot, show_last_update):
        self.bot = bot
        self.show_last_update = show_last_update
        self.text = self.prev_text = "<PB init>"
        self.message = self.bot.send_message(self.text)

    def write(self, text):
        new_text = text.strip().replace('\r', '')
        if new_text:
            self.text = new_text

    def flush(self):
        if self.prev_text != self.text:
            if '%' in self.text:
                self.bot.update_message(self.message, self.text +
                                                      '\nLast update: {}'.format(
                                                          datetime.now()) if self.show_last_update else self.text)
            self.prev_text = self.text


class TGTqdm:
    def __init__(self, bot: TelegramBot, show_last_update: bool = False):
        self.bot = bot
        self.tg_io = _TelegramIO(bot, show_last_update)

    def __call__(self, iterable=None, **kwargs):
        params = {
            'file': self.tg_io,
            'ascii': False,
        }

        params.update(kwargs)

        if iterable is not None:
            params['iterable'] = iterable

        return tqdm(**params)
