"""
Данный модуль нужен с той целью, чтобы автоматически пробрасывать классы,
которые осуществляют поиск по открытым источникам.
# noqa: E501
"""

import pkgutil
import importlib
import types


def load_modules(path: str) -> dict[str, types.ModuleType]:
    """
    Функция для динамической загрузки всех модулей в указанном пути.

    :param path: Путь, в котором следует искать модули.
    :return: Словарь, где ключи - это имена модулей, а значения - это сами модули.
    """  # noqa: E501
    return {
        name: importlib.import_module(name)
        for loader, name, is_pkg in pkgutil.walk_packages(path)
        if is_pkg
    }
