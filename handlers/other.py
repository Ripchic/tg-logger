from aiogram import types, Dispatcher
from aiogram import Router, F
from aiogram.filters import Command

router = Router()


@router.message()
async def echo_send(message: types.Message):
    await message.answer("Прости, я не настолько умён, чтобы ответить тебе на это сообщение. Может, тебе поможет меню?")

