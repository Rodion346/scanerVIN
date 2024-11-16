import re

import requests
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.util import await_only

from core.config import settings
from utils.check_func import check_and_convert_gn

pre_report_router = Router()


class GNumb(StatesGroup):
    number = State()


async def check_and_convert_gn_vin(input_string):
    # Регулярное выражение для проверки формата гос. номера
    gov_number_pattern = r"^[А-Яа-я]{1}\d{3}[А-Яа-я]{2}\d{2}$"

    # Регулярное выражение для проверки формата VIN-номера
    vin_number_pattern = r"^[A-HJ-NPR-Z0-9]{17}$"

    # Проверка соответствия формату гос. номера
    if re.match(gov_number_pattern, input_string):
        return "gos_n"
    # Проверка соответствия формату VIN-номера
    elif re.match(vin_number_pattern, input_string):
        return "vin"
    else:
        return False


@pre_report_router.message(F.text == "Предварительный отчёт")
async def gen_gos_number(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите гос-номер или VIN")
    await state.set_state(GNumb.number)


@pre_report_router.message(GNumb.number)
async def g_n(message: Message, state: FSMContext):
    numb = await check_and_convert_gn(message.text)
    if numb is False:
        await message.answer("Не верный формат, повторите попытку.")
        await state.set_state(GNumb.number)
    else:
        await state.update_data(number=numb)
        check = await check_and_convert_gn_vin(message.text)
        if check == "gos_n":
            resp = requests.get(
                f"https://data.tronk.info/reportnewcheck.ashx?key={settings.tron__key}&gosnumber={numb}"
            )
        elif check == "vin":
            resp = requests.get(
                f"https://data.tronk.info/reportnewcheck.ashx?key={settings.tron__key}&vin={numb}"
            )
        data = resp.json()

        if data.get("error"):
            print(data.get("error"))
        else:
            result = data.get("result", {})
            mess = (
                f"VIN: {result.get('Vin')}\n"
                f"Гос.номер: {result.get('Number')}\n"
                f"Марка ТС: {result.get('Marka')}\n"
                f"Модель ТС: {result.get('Model')}\n"
                f"Год выпуска ТС: {result.get('Year')}\n"
                f"Цвет ТС: {result.get('Color')}\n"
                f"Объем двигателя ТС: {result.get('Volume')}\n"
                f"Мощность двигателя ТС (л.c.): {result.get('HorsePower')}\n"
                f"Ссылка на изображение ТС: {result.get('Image')}"
            )

            await message.answer(mess)
        await state.clear()
