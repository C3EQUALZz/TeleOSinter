"""
Здесь в модуле содержится класс, с паттерном фабричный метод.
Это удобный вариант для создания других экземпляров класса.
Здесь у меня определяется коряво с помощью паттернов, которые проверяют текст,
а потом в зависимости от содержания запускают логику.
"""
from teleosinter.email_scripts import EmailProcessor
import re


class ProcessorFactory:
    """
    Класс, который реализует паттерн фабричный метод.
    Он нужен нам для того, чтобы в зависимости от сообщения запускалась нужная обработка.
    """  # noqa: E501

    @staticmethod
    def is_email(message: str) -> str | bool:
        """
        Проверка на то, что в сообщении содержится почта.

        https://emailregex.com/
        """
        email_pattern = r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b'
        match = re.search(email_pattern, message)
        return match.group(0) if match else False

    @staticmethod
    async def create_processor(message: str) -> str:
        """
        Фабричный метод, который создает в зависимости от сообщения нужную обработку
        """  # noqa: E501

        if email := ProcessorFactory.is_email(message):
            return await EmailProcessor().handle(email=email)

        return "Ничего не распознано"
