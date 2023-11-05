"""
Данный модуль создан для обработки интернациональных номеров телефона
Библиотека phonenumbers поддерживает только зарубежные номера телефонов
"""

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


def get_info_about_number(number: str):
    try:
        phone = phonenumbers.parse(number)
    except phonenumbers.NumberParseException:
        return "Неправильно ввели номер телефона, возможно отсутствует ссылка на регион"

    return (f"Тип телефона: {type_of_number(phone).value}\nПровайдер: {operator_of_number(phone)}\n"
            f"Регион: {region_of_number(phone)}\nЧасовой пояс: {timezone_of_number(phone)}")


def type_of_number(phone: phonenumbers.PhoneNumber) -> TypePhone:
    """
    Определяет тип номера телефона (частный, мобильный, домашний и т.п).
    :param phone: Номер телефона, который обработан phonenumber.parse().
    :return: Тип, к которому относится наш номер телефона. Результат - str.
    """
    if not phonenumbers.is_valid_number(phone):
        return TypePhone.UNKNOWN
    return TypePhone.get(phonenumbers.number_type(phone))


def operator_of_number(phone: phonenumbers.PhoneNumber) -> str:
    """
    Определяет оператора, к которому принадлежит номер телефона.
    :param phone: Номер телефона, который обработан phonenumber.parse().
    :return: Название оператора в виде str
    """
    return phonenumbers.carrier.name_for_number(phone, lang="en")


def region_of_number(phone: phonenumbers.PhoneNumber) -> str:
    """
    Определяет регион оператора, к которому принадлежит номер телефона.
    :param phone: Номер телефона, который обработан phonenumber.parse().
    :return: Название региона в виде str
    """
    return geocoder.description_for_number(phone, 'ru')


def timezone_of_number(phone: phonenumbers.PhoneNumber) -> str:
    """
    Определяет часовой пояс, к которому принадлежит номер телефона.
    :param phone: Номер телефона, который обработан phonenumbers.parse().
    :return: Часовой пояс в виде str
    """
    if (result := timezone.time_zones_for_number(phone)[0]) is None:
        result = "Неизвестный пояс"
    return result
