"""
Этот код представляет собой простой веб-скрапер (web scraper) на основе библиотек requests и BeautifulSoup,
который используется для получения информации о телефонных номерах
с веб-сайта https://spamcalls.net.
"""
__all__ = ["get_info_from_spam_calls"]

import asyncio

import aiohttp
import bs4
import fake_useragent
import googletrans
import phonenumbers

# Генерация случайных заголовков (метаданные, которые отправляются вместе с запросом на сервер).
# Они должны быть случайными, так как в большинстве случаев сервера имеют защиты на частые запросы.
HEADERS = {'User-Agent': fake_useragent.UserAgent().random}


async def _fetch(url: str) -> str:
    """
    Корутина, которая делает асинхронные HTTP-запросы.
    :param url: Ссылка на наш сайт.
    :return: Возвращает html код сайта.
    """
    # Создание асинхронного клиента для запроса
    async with aiohttp.ClientSession() as session:
        # делаем GET запрос для получения информации
        async with session.get(url, headers=HEADERS) as response:
            return await response.text()


async def get_info_from_spam_calls(phone_number: phonenumbers.PhoneNumber) -> str:
    """
    :param phone_number: номер телефона, который предоставил пользователь для обработки
    :return: информацию о человеке с сайта https://spamcalls.net
    """
    # Нужно вставить в ссылку строчный тип, чтобы заработало, убираю '+' с начала номера телефона
    phone_number_str = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)[1:]

    # Получаем информацию с сайта
    request = await _fetch(f"https://spamcalls.net/en/number/{phone_number_str}")

    # Парсим страницу и переводим слова на русский, так как по умолчанию там английский
    info_about_person = await asyncio.gather(*map(_translate_word, await _parse_page(request)))

    titles = ("Название страны", "Вероятность спама", "Люди чаще всего жаловались на")
    source_name = "\U0001F4A5 Информация с сайта https://spamcalls.net:\n"
    return source_name + "\n".join(f"{paragraph}: {info}" for paragraph, info in zip(titles, info_about_person))


async def _translate_word(word: str) -> str:
    """
    Данная функция переводит текст, используя googletrans.
    :param word: Слово/предложение, которое мы получили с сайта https://spamcalls.net.
    :return: Переведенное слово/предложение
    """
    translator = googletrans.Translator(user_agent=fake_useragent.UserAgent().random)
    return translator.translate(word, src='en', dest='ru').text


async def _parse_page(request: str) -> tuple[str, ...]:
    """
    Данная функция парсит страницу на сайте.
    Все заготовленные селекторы можно спокойно открыть и использовать, данный сайт маловероятно будет модифицироваться.
    :param request: Наш запрос к сайту, который при производим.
    :return: Название страны, вероятность спама, оценка пользователя (на основе отзывов с сайта)
    """
    source = bs4.BeautifulSoup(request, "lxml")

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
                                               "Пользовательские отчеты по номеру телефона недоступны (больше не "
                                               "доступны).")
    # оценки от пользователей
    user_evaluations = await get_text_or_default('a[href="#estimates"]',
                                                 "Нет оценок или отзывов по данному пользователю")

    # название страны
    country_name = await get_text_or_default('a[href="#origin"]', "Неизвестная страна")

    return country_name, situation_spam, user_evaluations



