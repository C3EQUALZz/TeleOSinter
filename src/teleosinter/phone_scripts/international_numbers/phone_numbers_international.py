"""
Данный модуль создан для обработки интернациональных номеров телефона
Библиотека phonenumbers поддерживает только зарубежные номера телефонов
Здесь скорее всего не имеет смысл делать асинхронно, потому что функции синхронны, но для удобства сделал так.
"""

__all__ = ["get_info_from_phonenumbers"]

from enum import Enum

import phonenumbers
from phonenumbers import carrier, geocoder, timezone


class TypePhone(Enum):
    FIXED_LINE = "Фиксированная линия"
    MOBILE = "Мобильный телефон"
    FIXED_LINE_OR_MOBILE = "Фиксированная линия или мобильный телефон"
    TOLL_FREE = "Бесплатная линия"
    PREMIUM_RATE = "Платная линия"
    SHARED_COST = "Номер с разделенной стоимостью"
    VOIP = "Voice over IP numbers"
    PERSONAL_NUMBER = "Персональный номер телефона"
    PAGER = "Пейджер"
    UAN = "Компания"
    VOICEMAIL = "Voice Mail Access Numbers"
    UNKNOWN = "Неизвестный или некорректный номер телефона"

    @staticmethod
    def get(item):
        return list(TypePhone)[item]


async def get_info_from_phonenumbers(phone: phonenumbers.PhoneNumber) -> str:
    """
    Обработка вывода всех функций для добавления в сообщения.
    Здесь мы получаем всю информацию с phonenumbers.
    :param phone: Номер телефона, который отправил человек.
    :return: Возвращает номер телефона пользователя.
    """
    titles = ("Тип телефона", "Провайдер", "Регион", "Часовой пояс")

    source_name = "\U0001F4AC Информация, полученная с phonenumbers\n"

    info_about_person = await _get_all_info_phone_numbers(phone)

    return source_name + '\n'.join(
        f"{paragraph}: {info}" for paragraph, info in zip(titles, info_about_person))


async def _get_all_info_phone_numbers(phone: phonenumbers.PhoneNumber) -> tuple[str, ...]:
    """
    Служит интерфейсом для получения всей информации, используя phonenumbers.
    :param phone: Номер телефона, который отправил пользователь.
    :return: Возвращает кортеж с функциями, которые используются для определения всех параметров с phonenumbers
    """
    return (
        await _type_of_number(phone),
        await _operator_of_number(phone),
        await _region_of_number(phone),
        await _timezone_of_number(phone)
    )


async def _type_of_number(phone: phonenumbers.PhoneNumber) -> str:
    """
    Определяет тип номера телефона (частный, мобильный, домашний и т.п).
    :param phone: Номер телефона, который обработан phonenumber.parse().
    :return: Тип, к которому относится наш номер телефона. Результат - str.
    """
    if phonenumbers.is_valid_number(phone):
        return TypePhone.get(phonenumbers.number_type(phone)).value
    return TypePhone.UNKNOWN.value


async def _operator_of_number(phone: phonenumbers.PhoneNumber) -> str:
    """
    Определяет оператора, к которому принадлежит номер телефона.
    :param phone: Номер телефона, который обработан phonenumber.parse().
    :return: Название оператора в виде str
    """
    res = phonenumbers.carrier.name_for_number(phone, lang="en")
    return res if res else "Нет информации по провайдеру"


async def _region_of_number(phone: phonenumbers.PhoneNumber) -> str:
    """
    Определяет регион оператора, к которому принадлежит номер телефона.
    :param phone: Номер телефона, который обработан phonenumber.parse().
    :return: Название региона в виде str
    """
    return geocoder.description_for_number(phone, 'ru')


async def _timezone_of_number(phone: phonenumbers.PhoneNumber) -> str:
    """
    Определяет часовой пояс, к которому принадлежит номер телефона.
    :param phone: Номер телефона, который обработан phonenumbers.parse().
    :return: Часовой пояс в виде str
    """
    if (result := timezone.time_zones_for_number(phone)[0]) is None:
        result = "Неизвестный пояс"
    return result
