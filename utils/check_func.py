import re


async def check_and_convert_gn(input_string):
    # Регулярное выражение для проверки формата гос. номера
    gov_number_pattern = r"^[А-Яа-я]{1}\d{3}[А-Яа-я]{2}\d{2}$"

    # Регулярное выражение для проверки формата VIN-номера
    vin_number_pattern = r"^[A-HJ-NPR-Z0-9]{17}$"

    # Проверка соответствия формату гос. номера
    if re.match(gov_number_pattern, input_string):
        return input_string.upper()
    # Проверка соответствия формату VIN-номера
    elif re.match(vin_number_pattern, input_string):
        return input_string.upper()
    else:
        return False
