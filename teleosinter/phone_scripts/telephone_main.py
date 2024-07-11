"""
Данный модуль служит интерфейсом для взаимодействия
"""
import asyncio
from typing import Generator, Any

import phonenumbers
from teleosinter.phone_scripts import international_numbers
from teleosinter.core.abstract import PhoneParser


async def get_info_about_number(number: str) -> str:
    """
    С помощью данной функции мы будем запускать все другие скрипты для определения номера телефона.
    :param number: Номер телефона, который ввел пользователь.
    :return: Полную информацию по номеру телефона.
    """
    try:
        phone = phonenumbers.parse(number)
    except phonenumbers.NumberParseException:
        return "Неправильно ввели номер телефона, возможно отсутствует ссылка на регион"

    if not phonenumbers.is_possible_number(phone):
        return "Невозможный номер телефона, проверьте корректность ввода"

    return await _extract_info(phone)


async def _extract_info(number: phonenumbers.PhoneNumber) -> str:
    """
    Ради удобства я решил все автоматически запускать, каждый результат подпрограммы (скрапера)
    должен возвращаться в виде строки, чтобы здесь все склеивалось
    :param number: номер телефона, который ввел пользователь
    :return: полную информацию со всех OSINT источников
    """
    classes: Generator[PhoneParser, Any, None] = (getattr(international_numbers, attr)
                                                  for attr in dir(international_numbers)
                                                  if callable(getattr(international_numbers, attr)))

    results = await asyncio.gather(*(_class().parse(number) for _class in classes))
    return "\n\n".join(results)


async def main():
    result = await get_info_about_number("+37160006110")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
