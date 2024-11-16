import re

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.util import await_only

from utils.check_func import check_and_convert_gn

ext_report_router = Router()


class GNumb(StatesGroup):
    number = State()


@ext_report_router.message(F.text == "Полный отчёт")
async def gen_gos_number(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите гос-номер или VIN")
    await state.set_state(GNumb.number)
