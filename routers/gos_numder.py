import requests
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.util import await_only

from core.config import settings
from utils.check_func import check_and_convert_gn

gos_number_router = Router()


class GNumb(StatesGroup):
    g_n = State()


@gos_number_router.message(F.text == "Проверка авто по гос номеру")
async def gen_gos_number(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите гос-номер")
    await state.set_state(GNumb.g_n)


@gos_number_router.message(GNumb.g_n)
async def g_n(message: Message, state: FSMContext):
    gn = await check_and_convert_gn(message.text)
    if gn is False:
        await message.answer("Не верный формат номера, повторите попытку.")
        await state.set_state(GNumb.g_n)
    else:
        await state.update_data(g_n=gn)
        resp = requests.get(
            f"https://data.tronk.info/convertb2b.ashx?key={settings.tron__key}&gosnumber={gn}"
        )
        data = resp.json()
        if data.get("error"):
            print(data.get("error"))
        else:
            result = data.get("result", {})
            mess = (
                f"VIN: {result.get('vin')}\n"
                f"номер кузова: {result.get('body_number')}\n"
                f"номер шасси: {result.get('chassis_number')}\n"
                f"Гос.номер: {result.get('gosnumber')}\n"
                f"Модель ТС: {result.get('model')}\n"
                f"Год выпуска ТС: {result.get('year')}\n"
                f"СТС: {result.get('sts')}\n"
                f"категория ТС: {result.get('category')}\n"
                f"ристрационный статус ТС: {result.get('record_status')}\n"
                f"дата регистрационного действия: {result.get('registration_date')}\n"
                f"Мощность двигателя ТС (л.c.): {result.get('power_hp')}\n"
                f"Мощность двигателя ТС (кВ): {result.get('power_kw')}"
            )
            await message.answer(mess)
        await state.clear()
