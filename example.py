import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import RMSprop
import numpy as np

from model import KerasTelegramCallback
from tg_logger import TelegramBot

X = np.random.rand(1000, 100)
y = (np.random.rand(1000, 3) > 0.5).astype('float32')

model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(100,)))
model.add(Dense(512, activation='relu'))
model.add(Dense(3, activation='softmax'))


model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

n_epochs = 3

token = '6519815802:AAG9bufsMqZvFX42rY6_nSccOK0euwkFX2k'
user_id = 543987419
bot = TelegramBot(token, user_id)

tl = KerasTelegramCallback(bot, epoch_bar=True, to_plot=[
    {
        'metrics': ['loss', 'val_loss']
    },
    {
        'metrics': ['acc', 'val_acc'],
        'title':'Accuracy plot',
        'ylabel':'acc',
        'ylim':(0, 1),
        'xlim':(1, n_epochs)
    }
])

history = model.fit(X, y,
                    batch_size=10,
                    epochs=n_epochs,
                    validation_split=0.15,
                    callbacks=[tl])


# bot.clean_tmp_dir()