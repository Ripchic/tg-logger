import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import RMSprop
import numpy as np
import os

from keras_cb import KerasTelegramCallback
from tg_logger import TelegramBot


def keras_example(token, user_id, n_epochs=10):
    x = np.random.rand(1000, 100)
    y = (np.random.rand(1000, 3) > 0.5)

    model = Sequential()
    model.add(Dense(512, activation='relu', input_shape=(100,)))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(3, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=RMSprop(),
                  metrics=['accuracy'])

    bot = TelegramBot(token, user_id)

    tl = KerasTelegramCallback(bot, epoch_bar=True, to_plot=[
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

    history = model.fit(x, y,
                        batch_size=10,
                        epochs=n_epochs,
                        validation_split=0.15,
                        callbacks=[tl])
