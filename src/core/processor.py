from abc import ABC, abstractmethod


class Processor(ABC):
    @abstractmethod
    def handle(self, data):
        ...
