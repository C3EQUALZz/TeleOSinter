import asyncio
from typing import LiteralString

from src.core.email_scripts import utils
from src.core.email_scripts.interface import EmailSearcher
from src.core.processor import Processor


class EmailProcessor(Processor):
    def __init__(self):
        self.utilities = (
            cls() for cls in utils.__dict__.values() if isinstance(cls, type) and issubclass(cls, EmailSearcher)
        )

    async def handle(self, email: str) -> LiteralString:
        results = await asyncio.gather(*(utility.search(email) for utility in self.utilities))
        return '\n'.join(results)
