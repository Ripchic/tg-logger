from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.enums.dice_emoji import DiceEmoji

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(f"Приветствую тебя {message.from_user.full_name}")


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer("Список доступных команд: in progress")


@router.message(Command(commands=['dice']))
async def cmd_dice(message: Message):
    await message.answer_dice(emoji=DiceEmoji.DICE)  # "🎲"


@router.message(Command(commands=['chat_id']))
async def cmd_chat_id(message: Message):
    await message.answer(f"Chat id: {message.chat.id}")
