"""
Данный модуль создан для обработки интернациональных номеров телефона
Библиотека phonenumbers поддерживает только зарубежные номера телефонов
Здесь скорее всего не имеет смысл делать асинхронно, потому что функции синхронны, но для удобства сделал так.
"""

__all__ = ["PhoneNumberParser"]

from enum import Enum
from typing import TYPE_CHECKING
from phonenumbers import carrier, geocoder, timezone, is_valid_number, number_type
from teleosinter.core.abstract import PhoneParser

if TYPE_CHECKING:
    from phonenumbers import PhoneNumber


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


class PhoneNumberParser(PhoneParser):
    async def parse(self, phone_number: "PhoneNumber") -> str:
        """
        Обработка вывода всех функций для добавления в сообщения.
        Здесь мы получаем всю информацию с phonenumbers.
        :param phone_number: Номер телефона, который отправил человек.
        :return: Возвращает номер телефона пользователя.
        """
        titles = ("Тип телефона", "Провайдер", "Регион", "Часовой пояс")

        source_name = "\U0001F4AC Информация, полученная с phonenumbers\n"

        info_about_person = await self.__get_all_info_phone_numbers(phone_number)

        return source_name + '\n'.join(
            f"{paragraph}: {info}"
            for paragraph, info in zip(titles, info_about_person)
        )

    async def __get_all_info_phone_numbers(self, phone: "PhoneNumber") -> tuple[str, ...]:
        """
        Служит интерфейсом для получения всей информации, используя phonenumbers.
        :param phone: Номер телефона, который отправил пользователь.
        :return: Возвращает кортеж с функциями, которые используются для определения всех параметров с phonenumbers
        """
        return (
            await self._type_of_number(phone),
            await self._operator_of_number(phone),
            await self._region_of_number(phone),
            await self._timezone_of_number(phone)
        )

    @staticmethod
    async def _type_of_number(phone: "PhoneNumber") -> str:
        """
        Определяет тип номера телефона (частный, мобильный, домашний и т.п).
        :param phone: Номер телефона, который обработан phonenumber.parse().
        :return: Тип, к которому относится наш номер телефона. Результат - str.
        """
        if is_valid_number(phone):
            return TypePhone.get(number_type(phone)).value
        return TypePhone.UNKNOWN.value

    @staticmethod
    async def _operator_of_number(phone: "PhoneNumber") -> str:
        """
        Определяет оператора, к которому принадлежит номер телефона.
        :param phone: Номер телефона, который обработан phonenumber.parse().
        :return: Название оператора в виде str
        """
        res = carrier.name_for_number(phone, lang="en")
        return res if res else "Нет информации по провайдеру"

    @staticmethod
    async def _region_of_number(phone: "PhoneNumber") -> str:
        """
        Определяет регион оператора, к которому принадлежит номер телефона.
        :param phone: Номер телефона, который обработан phonenumber.parse().
        :return: Название региона в виде str
        """
        return geocoder.description_for_number(phone, 'ru')

    @staticmethod
    async def _timezone_of_number(phone: "PhoneNumber") -> str:
        """
        Определяет часовой пояс, к которому принадлежит номер телефона.
        :param phone: Номер телефона, который обработан phonenumbers.parse().
        :return: Часовой пояс в виде str
        """
        if (result := timezone.time_zones_for_number(phone)[0]) is None:
            result = "Неизвестный пояс"
        return result
