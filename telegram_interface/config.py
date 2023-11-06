"""
Модуль, который отвечает за конфигурацию бота
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class ImproperlyConfigured(Exception):
    """Возмущает ошибку, когда отсутствует нужная переменная"""

    def __init__(self, variable_name, *args):
        self.variable_name = variable_name
        self.message = f"Установите {variable_name} environment variable."
        super().__init__(self.message, *args)


def get_env_variable(var_name: str) -> str:
    """Получает переменную окружение или возмущает ошибку

    Args:
        var_name: имя переменной окружения.

    Returns:
        Значение переменной окружения.

    Raises:
        ImproperlyConfigured: если не установлена переменная окружения.
    """
    try:
        return os.environ[var_name]
    except KeyError:
        raise ImproperlyConfigured(var_name)


BOT_TOKEN: str = get_env_variable("TOKEN")
# BASE_PATH: Path = Path(__file__).resolve().parent.parent
# RESOURCES_PATH: str = os.path.join(BASE_PATH, "res/")
# Возможно здесь добавится конфигурация для базы данных, но я пока не знаю как организовать :D

