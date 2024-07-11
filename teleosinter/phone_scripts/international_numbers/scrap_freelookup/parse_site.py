"""
Здесь происходит запросы к freelookup.net, за основу был взят код отсюда:
https://github.com/N0rz3/Phunter/blob/master/lib/free_lookup.py
"""

from typing import TYPE_CHECKING
from bs4 import BeautifulSoup
from teleosinter.core.abstract import PhoneParser
from phonenumbers import format_number, PhoneNumberFormat

if TYPE_CHECKING:
    from phonenumbers import PhoneNumber

__all__ = ["FreeLookUpParser"]


class FreeLookUpParser(PhoneParser):
    async def parse(self, phone_number: "PhoneNumber") -> str:
        """
        Метод, который парсит сайт free-lookup.net
        """
        string_phone_number = format_number(phone_number, PhoneNumberFormat.E164).strip('+')
        text = await self.fetch(f"https://free-lookup.net/{string_phone_number}")
        html_body = BeautifulSoup(text, "html.parser")

        list_info = html_body.findChild("ul", class_="report-summary__list").findAll("div")

        source_name = "✍️ Информация с сайта free-lookup.net:\n"

        return source_name + "\n".join(
            f"{k.text.strip()}: {info.text.strip() if info.text.strip() else 'Not found'}"
            for _, (k, info) in enumerate(zip(list_info[::2], list_info[1::2]))
        )
