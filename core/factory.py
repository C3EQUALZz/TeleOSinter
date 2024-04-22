"""
Здесь в модуле содержится класс, с паттерном фабричный метод.
Это удобный вариант для создания других экземпляров класса.
Здесь у меня определяется коряво с помощью паттернов, которые проверяют текст,
а потом в зависимости от содержания запускают логику.
"""
from core.email_scripts import EmailProcessor
import re


class ProcessorFactory:
    """
    Класс, который реализует паттерн фабричный метод.
    Он нужен нам для того, чтобы в зависимости от сообщения запускалась нужная обработка.
    """
    @staticmethod
    def is_email(message: str) -> bool:
        """
        Проверка на то, что в сообщении содержится почта.

        https://emailregex.com/
        """
        email_pattern = r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b'
        return bool(re.search(email_pattern, message))

    @staticmethod
    async def create_processor(message: str) -> str:
        """
        Фабричный метод, который создает в зависимости от сообщения нужную обработку
        """
        if ProcessorFactory.is_email(message):
            return await EmailProcessor().handle(email=message)

        return "Ничего не распознано"
