import matplotlib.pyplot as plt
from tg_logger import TelegramBot
from utils import TGTqdm
import random

try:
    import keras
except ImportError:
    from tensorflow import keras


class KerasTelegramCallback(keras.callbacks.Callback):
    def __init__(self, bot: TelegramBot, epoch_bar: bool = True, to_plot: list = []):
        super(KerasTelegramCallback, self).__init__()
        self.bot = bot
        self.epoch_bar = epoch_bar
        self.to_plot = to_plot
        self.plot_id = {}
        self.name = 'Training'
        self.obj = None
        self.pbar = None
        self.metrics = None
        self.n_epochs = None
        self.history = None
        self.current_epoch = None
        self.samples = None
        self.total_steps = None
        self.msg = None

        for i in range(len(self.to_plot)):
            p = self.to_plot[i]
            p['id'] = i
            self.plot_id[p['id']] = None

    def on_train_begin(self, logs={}):
        if 'metrics' not in self.params:
            self.params['metrics'] = []
            for plot_config in self.to_plot:
                if 'metrics' in plot_config:
                    self.params['metrics'].extend(plot_config['metrics'])

        self.metrics = self.params['metrics']
        self.n_epochs = self.params['epochs']
        self.samples = self.params['steps']
        self.history = {}
        for metric in self.metrics:
            self.history[metric] = []
        self.current_epoch = 0
        self.total_steps = self.n_epochs * self.samples

        fields = ['Status', 'Epoch']
        units = ['', '']
        values = ['TRAINING', f"{self.current_epoch}/{self.n_epochs}"]

        self.msg = self.bot.send_structured_text(fields, values, units)
        if self.epoch_bar:
            if self.pbar is None:
                self.obj = TGTqdm(self.bot)
                self.pbar = self.obj(total=self.total_steps)

    def on_epoch_end(self, epoch, logs=None):
        self.current_epoch += 1

        fields = ['Status', 'Epoch']
        units = ['', '']
        values = ['TRAINING', f"{self.current_epoch}/{self.n_epochs}"]

        self.bot.update_structured_text(self.msg, fields, values, units)

        for m in self.metrics:
            self.history[m].append(logs[m])

        random.shuffle(self.to_plot)
        for plot_par in self.to_plot:
            self.plot_id[plot_par['id']] = self.plot(
                plot_par, self.plot_id[plot_par['id']], force=True if self.current_epoch == self.n_epochs else False)

        if self.epoch_bar:
            message = ''
            for m in self.metrics:
                if 'val_' not in m:
                    message += f"{m}: {logs[m]:.4f} - "
            if self.epoch_bar:
                self.pbar.set_description(message[:-3])
                self.pbar.update(self.samples)

    def on_train_end(self, logs=None):
        fields = ['Status']
        units = ['']
        values = ['TRAINING END']
        self.bot.update_structured_text(self.msg, fields, values, units,
                                        force=True if self.current_epoch == self.n_epochs else False)
        self.bot.clean_tmp_dir()

    def plot(self, params: dict, plot_id=None, force: bool = False):
        metrics = params['metrics']
        title = params.get('title', 'Loss')
        ylabel = params.get('ylabel', 'Loss')
        xlabel = params.get('xlabel', 'Epochs')
        xlim = params.get('xlim', None)
        ylim = params.get('ylim', None)

        t = [k + 1 for k in range(len(self.history[metrics[0]]))]

        for m in metrics:
            plt.plot(t, self.history[m])

        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.legend(metrics)

        if xlim is not None:
            plt.xlim(xlim[0], xlim[1])
        if ylim is not None:
            plt.ylim(ylim[0], ylim[1])

        if plot_id is None:
            plot_id = self.bot.send_plot(plt, self.name)
        else:
            self.bot.update_plot(plot_id, plt, self.name, force=force)

        plt.gcf().clear()
        return plot_id
