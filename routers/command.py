from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message


from utils.create_keyboard import create_kb

command_router = Router()


@command_router.message(Command("start"))
async def start_command(message: Message):
    buttons = [
        "Проверка авто по гос номеру",
        "Предварительный отчёт",
        "Расширенный отчет",
        "Полный отчёт",
    ]
    await message.answer(
        "Приветственное сообщение",
        reply_markup=await create_kb.create_keyboard(buttons),
    )
