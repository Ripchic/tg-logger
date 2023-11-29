from tqdm import tqdm
from tg_logger import TelegramBot


class _TelegramIO:
    def __init__(self, bot: TelegramBot, show_last_update=False):
        self.bot = bot
        self.show_last_update = show_last_update
        self.prev_text = '<< Init progress bar >>'
        self.text = self.prev_text
        self.message = None
        self.message_id = None

    async def initialize_message(self):
        self.message = await self.bot.send_message(text=self.message)
        self.message_id = self.message.message_id

    def write(self, s):
        new_text = s.strip().replace('\r', '')
        if len(new_text) != 0:
            self.text = new_text

    async def flush(self):
        if self.prev_text != self.text:
            if '%' in self.text:
                await self.bot.edit_message(message_id=self.message_id, text=self.text)
                self.prev_text = self.text


class TelegramTqdm:

    def __init__(self, bot, show_last_update=False):
        self.bot = bot
        self.tg_io = _TelegramIO(bot, show_last_update)

        self.tg_io.initialize_message()

    def __call__(self, iterable=None, show_last_update=False,
                 desc=None, total=None, leave=True, ncols=None, mininterval=1.0, maxinterval=10.0,
                 miniters=None, ascii=False, disable=False, unit='it',
                 unit_scale=False, dynamic_ncols=False, smoothing=0.3,
                 bar_format=None, initial=0, position=None, postfix=None,
                 unit_divisor=1000, gui=False, **kwargs):
        params = {
            'desc': desc,
            'total': total,
            'leave': leave,
            'file': self.tg_io,
            'ncols': ncols,
            'mininterval': mininterval,
            'maxinterval': maxinterval,
            'miniters': miniters,
            'ascii': ascii,
            'disable': disable,
            'unit': unit,
            'unit_scale': unit_scale,
            'dynamic_ncols': dynamic_ncols,
            'smoothing': smoothing,
            'bar_format': bar_format,
            'initial': initial,
            'position': position,
            'postfix': postfix,
            'unit_divisor': unit_divisor,
            'gui': gui
        }

        params.update(kwargs)

        if iterable is not None:
            params['iterable'] = iterable

        return tqdm(**params)
