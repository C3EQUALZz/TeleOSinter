import abc
import aiohttp
import fake_useragent
import phonenumbers
import typing

# Генерация случайных заголовков (метаданные, которые отправляются вместе с запросом на сервер).
# Они должны быть случайными, так как в большинстве случаев сервера имеют защиты на частые запросы.
HEADERS = {'User-Agent': fake_useragent.UserAgent().random}


class PhoneParser(abc.ABC):
    @abc.abstractmethod
    async def parse(self, phone_number: phonenumbers.PhoneNumber) -> str:
        ...

    @staticmethod
    async def fetch(url: str) -> str:
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
