import torch
from pytorch_lightning.loggers import TensorBoardLogger
from torch import nn
import pytorch_lightning as pl
from torch.utils.data import DataLoader, random_split
from torch.nn import functional as F
from torchvision.datasets import MNIST
from torchvision import datasets, transforms
from pytorch_lightning.callbacks import Callback
import numpy as np
import os
from torch_cb import TorchCallback
from tg_logger import TelegramBot
import torch
import pytorch_lightning as pl
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.optimizers import RMSprop


# X = np.random.rand(1000, 100)
# y = (np.random.rand(1000, 3) > 0.5).astype('float32')
#
# model = Sequential()
# model.add(Dense(512, activation='relu', input_shape=(100,)))
# model.add(Dense(512, activation='relu'))
# model.add(Dense(3, activation='softmax'))
#
# model.compile(loss='categorical_crossentropy',
#               optimizer=RMSprop(),
#               metrics=['accuracy'])
#
n_epochs = 5

token = os.getenv('TOKEN')
user_id = os.getenv('ID')
bot = TelegramBot(token, user_id)


tl = TorchCallback(bot, epoch_bar=True, to_plot=[
    {
        'metrics': ['loss', 'val_loss']
    },
    {
        'metrics': ['accuracy', 'val_accuracy'],
        'title': 'Accuracy plot',
        'ylabel': 'accuracy',
        'ylim': (0, 1),
        'xlim': (1, n_epochs)
    }
])

# history = model.fit(X, y,
#                     batch_size=10,
#                     epochs=n_epochs,
#                     validation_split=0.15,
#                     callbacks=[tl])


class LightningMNISTClassifier(pl.LightningModule):

  def __init__(self):
    super().__init__()

    # mnist images are (1, 28, 28) (channels, width, height)
    self.layer_1 = torch.nn.Linear(28 * 28, 128)
    self.layer_2 = torch.nn.Linear(128, 256)
    self.layer_3 = torch.nn.Linear(256, 10)

  def forward(self, x):
      batch_size, channels, width, height = x.size()

      # (b, 1, 28, 28) -> (b, 1*28*28)
      x = x.view(batch_size, -1)

      # layer 1 (b, 1*28*28) -> (b, 128)
      x = self.layer_1(x)
      x = torch.relu(x)

      # layer 2 (b, 128) -> (b, 256)
      x = self.layer_2(x)
      x = torch.relu(x)

      # layer 3 (b, 256) -> (b, 10)
      x = self.layer_3(x)

      # probability distribution over labels
      x = torch.log_softmax(x, dim=1)

      return x

  def cross_entropy_loss(self, logits, labels):
    return F.nll_loss(logits, labels)

  def training_step(self, train_batch, batch_idx):
      x, y = train_batch
      logits = self.forward(x)
      loss = self.cross_entropy_loss(logits, y)
      self.log('train_loss', loss)
      return loss

  def validation_step(self, val_batch, batch_idx):
      x, y = val_batch
      logits = self.forward(x)
      loss = self.cross_entropy_loss(logits, y)
      self.log('val_loss', loss)

  def configure_optimizers(self):
      optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
      return optimizer

# data
# transforms for images
transform=transforms.Compose([transforms.ToTensor(),
                              transforms.Normalize((0.1307,), (0.3081,))])

# prepare transforms standard to MNIST
mnist_train = MNIST(os.getcwd(), train=True, download=True, transform=transform)
mnist_test = MNIST(os.getcwd(), train=False, download=True, transform=transform)

train_dataloader = DataLoader(mnist_train, batch_size=64)
val_loader = DataLoader(mnist_test, batch_size=64)


# train
model = LightningMNISTClassifier()
logger = TensorBoardLogger('logs/')
trainer = pl.Trainer(logger=logger, max_epochs=5)

trainer.fit(model, train_dataloader, val_loader)