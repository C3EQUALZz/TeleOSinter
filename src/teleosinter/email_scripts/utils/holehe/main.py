"""
Здесь я пользуюсь терминальной версией скрипта holehe https://github.com/megadose/holehe
По умолчанию он асинхронный, поэтому я использовал такой интерфейс.
# noqa: E501
"""

import re
import asyncio
from teleosinter.core._email_utils.interface import EmailSearcher


class Holehe(EmailSearcher):
    """
    Получает информацию, используя https://github.com/megadose/holehe
    """

    @staticmethod
    async def search(email: str) -> str:
        """
        :param email: почта, которую ввел пользователь
        :return: строка, где указано на каких сервисах есть данная почта
        """

        process = await asyncio.create_subprocess_exec(
            'holehe', email,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f"Произошла ошибка {stderr}")

        return "😈 Результат поиска holehe:\n" + '\n'.join(
            match.group()
            for match in re.finditer(
                r"\[.].+",
                stdout.decode(),
                re.MULTILINE | re.IGNORECASE
            )
        )
