"""
Абстрактный класс, который описывает макет для создания классов для поиска информации, зная почту. # noqa: E501
"""

from abc import ABC, abstractmethod


class EmailSearcher(ABC):
    """
    Абстрактный класс, который нужен для связки поиска элементов, зная почту
    """
    @staticmethod
    @abstractmethod
    async def search(email: str) -> str:
        """
        Метод, который запускает поиск информации по почте
        """
        ...
