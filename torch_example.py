import json

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import os

from pytorch_cb import PyTorchTelegramCallback
from tg_logger import TelegramBot

X = np.random.rand(1000, 100).astype(np.float32)
y = np.random.randint(0, 3, size=(1000,), dtype=np.int64)

X_tensor = torch.tensor(X)
y_tensor = torch.tensor(y)

dataset = TensorDataset(X_tensor, y_tensor)
train_loader = DataLoader(dataset, batch_size=5, shuffle=True)


class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(100, 512)
        self.fc2 = nn.Linear(512, 512)
        self.fc3 = nn.Linear(512, 3)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


model = SimpleNN()

criterion = nn.CrossEntropyLoss()
optimizer = optim.RMSprop(model.parameters())

n_epochs = 30

token = os.getenv('TOKEN')
user_id = os.getenv('CHAT_ID')
bot = TelegramBot(token, user_id)

tl = PyTorchTelegramCallback(bot, epoch_bar=True, to_plot=[
    {
        'metrics': ['loss']
    },
    {
        'metrics': ['accuracy'],
        'title': 'Accuracy plot',
        'ylabel': 'accuracy',
        'ylim': (0, 1),
        'xlim': (1, n_epochs)
    }
])

tl.on_train_begin(n_epochs=n_epochs, n_batches=len(train_loader))

history = []
for epoch in range(n_epochs):
    running_loss = 0.0
    correct = 0
    total = 0

    for i, (inputs, labels) in enumerate(train_loader):
        optimizer.zero_grad()

        outputs = model(inputs)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    epoch_loss = running_loss / len(train_loader)
    epoch_accuracy = correct / total
    logs = {'loss': epoch_loss, 'accuracy': epoch_accuracy}
    history.append(logs)
    tl.on_epoch_end(logs)
json_object = json.dumps(history, indent=4)
with open("temp/log.json", "w") as outfile:
    outfile.write(json_object)
bot.send_json()
json_string = json.dumps(history)
with open('temp/log.txt', 'w') as file:
    file.write(json_string)
bot.send_txt()
tl.on_train_end()
