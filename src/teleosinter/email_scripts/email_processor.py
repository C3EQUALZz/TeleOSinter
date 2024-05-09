import asyncio
from typing import LiteralString

from teleosinter.email_scripts import utils
from teleosinter.core.email_utils.interface import EmailSearcher
from teleosinter.core.processor import Processor


class EmailProcessor(Processor):
    """
    Данный класс предназначен для запуска всех утилит, связанных с поиском информации по электронной почте.
    Происходит автоматическая сборка информации о всех классах, которые реализуют интерфейс EmailSearcher.
    """
    def __init__(self) -> None:
        self.utilities = (
            cls() for cls in utils.__dict__.values()
            if isinstance(cls, type) and issubclass(cls, EmailSearcher)
        )

    async def handle(self, email: str) -> LiteralString:
        """
        Запуск утилит для поиска информации, зная электронную почту
        """
        utilities = (utility.search(email) for utility in self.utilities)
        results = await asyncio.gather(*utilities)
        return '\n'.join(results)
