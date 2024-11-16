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
    g_n = State()


@ext_report_router.message(F.text == "Расширенный отчет")
async def gen_gos_number(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите гос-номер")
    await state.set_state(GNumb.g_n)


@ext_report_router.message(GNumb.g_n)
async def g_n(message: Message, state: FSMContext):
    gn = await check_and_convert_gn(message.text)
    if gn is False:
        await message.answer("Не верный формат номера, повторите попытку.")
        await state.set_state(GNumb.g_n)
    else:
        await state.update_data(g_n=gn)
