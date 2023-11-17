from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

load = KeyboardButton('Load course')
delete = KeyboardButton('Delete course')
cansel = KeyboardButton('тм')

new_kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

new_kb_admin.row(load, cansel)