import matplotlib.pyplot as plt
import random
from tg_logger import TelegramBot
from utils import TGTqdm


class PyTorchTelegramCallback:
    def __init__(self, bot: TelegramBot, epoch_bar: bool = True, to_plot: list = []):
        self.bot = bot
        self.epoch_bar = epoch_bar
        self.to_plot = to_plot
        self.plot_id = {}
        self.name = 'Training'
        self.metrics = []
        self.n_epochs = None
        self.history = {}
        self.current_epoch = None
        self.obj = None
        self.pbar = None
        self.total_steps = None
        self.msg = None
        self.n_batches = None

        for i, plot_config in enumerate(self.to_plot):
            plot_config['id'] = i
            self.plot_id[i] = None

    def on_train_begin(self, n_epochs, n_batches):
        self.n_epochs = n_epochs
        self.n_batches = n_batches
        self.current_epoch = 0
        self.history = {metric: [] for item in self.to_plot for metric in item.get('metrics', [])}

        fields = ['Status', 'Epoch']
        units = ['', '']
        values = ['TRAINING', f"{self.current_epoch}/{self.n_epochs}"]
        self.total_steps = n_epochs * n_batches
        self.msg = self.bot.send_structured_text(fields, values, units)
        if self.epoch_bar:
            if self.pbar is None:
                self.obj = TGTqdm(self.bot)
                self.pbar = self.obj(total=self.total_steps)

    def on_epoch_end(self, logs):
        self.current_epoch += 1

        fields = ['Status', 'Epoch']
        units = ['', '']
        values = ['TRAINING', f"{self.current_epoch}/{self.n_epochs}"]
        self.bot.update_structured_text(self.msg, fields, values, units)

        for metric, value in logs.items():
            self.history[metric].append(value)

        random.shuffle(self.to_plot)
        for plot_config in self.to_plot:
            self.plot_id[plot_config['id']] = self.plot(
                plot_config, self.plot_id[plot_config['id']],
                force=True if self.current_epoch == self.n_epochs else False)
        if self.epoch_bar:
            self.pbar.update(self.n_batches)

    def on_train_end(self):
        fields = ['Status']
        units = ['']
        values = ['TRAINING END']
        self.bot.update_structured_text(self.msg, fields, values, units, force=True)
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
