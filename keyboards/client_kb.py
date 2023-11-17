from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup

k1 = KeyboardButton('Курс')
k2 = KeyboardButton('Ничего')
k3 = KeyboardButton('Буквально ничего')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(k1).add(k2).add(k3)

new_kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

new_kb_client.row(k1, k2, k3)

order_key = InlineKeyboardButton(text="Заказать", url="google.com")

order_kb = InlineKeyboardMarkup(row_width=2)

order_kb.add(order_key)


Yes = KeyboardButton('Да')
No = KeyboardButton('Нет')
Cansel = KeyboardButton('Отмена')
YesNo_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
YesNo_kb.row(Yes, No, Cansel)


Subs = InlineKeyboardButton(text="Субтитры", callback_data="1")
Al = InlineKeyboardButton(text="Анилибрия", callback_data="2")
Av = InlineKeyboardButton(text="Анивост", callback_data="3")

notif_kb = InlineKeyboardMarkup(row_width=3).add(Subs, Al, Av)
