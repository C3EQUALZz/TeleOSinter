"""
Этот код представляет собой простой веб-скрапер (web scraper) на основе библиотек requests и BeautifulSoup,
который используется для получения информации о телефонных номерах
с веб-сайта https://spamcalls.net.
"""
__all__ = ["SpamCallsParser"]

from asyncio import gather
from typing import TYPE_CHECKING
from bs4 import BeautifulSoup
from phonenumbers import format_number, PhoneNumberFormat
from translate import Translator

from teleosinter.core.abstract import PhoneParser

if TYPE_CHECKING:
    from phonenumbers import PhoneNumber


class SpamCallsParser(PhoneParser):

    async def parse(self, phone_number: "PhoneNumber") -> str:
        """
        :param phone_number: номер телефона, который предоставил пользователь для обработки
        :return: информацию о человеке с сайта https://spamcalls.net
        """
        # Нужно вставить в ссылку строчный тип, чтобы заработало, убираю '+' с начала номера телефона
        phone_number_str = format_number(phone_number, PhoneNumberFormat.E164)[1:]

        # Получаем информацию с сайта
        request = await self.fetch(f"https://spamcalls.net/en/number/{phone_number_str}")

        # Парсим страницу и переводим слова на русский, так как по умолчанию там английский
        info_about_person = await gather(*map(self._translate_word, await self._parse_page(request)))

        titles = ("Название страны", "Вероятность спама", "Люди чаще всего жаловались на")
        source_name = "\U0001F4A5 Информация с сайта https://spamcalls.net:\n"
        return source_name + "\n".join(
            f"{paragraph}: {info}"
            for paragraph, info in zip(titles, info_about_person)
        )

    @staticmethod
    async def _translate_word(word: str) -> str:
        """
        Данная функция переводит текст, используя библиотеку translate.
        :param word: Слово/предложение, которое мы получили с сайта https://spamcalls.net.
        :return: Переведенное слово/предложение
        """
        translator = Translator(to_lang='ru', from_lang='en')
        return translator.translate(word)

    @staticmethod
    async def _parse_page(request: str) -> tuple[str, ...]:
        """
        Данная функция парсит страницу на сайте.
        Все заготовленные селекторы можно спокойно открыть и использовать, данный сайт маловероятно будет модифицироваться.
        :param request: Наш запрос к сайту, который при производим.
        :return: Название страны, вероятность спама, оценка пользователя (на основе отзывов с сайта)
        """
        source = BeautifulSoup(request, "lxml")

        async def get_text_or_default(selector: str, default: str) -> str:
            """
            Функция для DRY кода, позволяет извлечь селекторы с сайта
            Если значение пусто
            :param selector: CSS селектор, который мы хотим спарсить с сайта.
            :param default: Значение по умолчанию, если нет значения там.
            :return: Возвращает строку с информацией
            """
            element = source.select(selector)
            return element[0].text if element else default

        # Рейтинг от пользователей
        situation_spam = await get_text_or_default('a[href="#ratings"]',
                                                   "Пользовательские отчеты по номеру телефона"
                                                   " недоступны (больше не доступны).")
        # оценки от пользователей
        user_evaluations = await get_text_or_default('a[href="#estimates"]',
                                                     "Нет оценок или отзывов по данному пользователю")

        # название страны
        country_name = await get_text_or_default('a[href="#origin"]', "Неизвестная страна")

        return country_name, situation_spam, user_evaluations
