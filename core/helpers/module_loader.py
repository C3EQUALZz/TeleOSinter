import pkgutil
import importlib


def load_modules(path: str) -> dict:
    """
    Функция для динамической загрузки всех модулей в указанном пути.

    :param path: Путь, в котором следует искать модули.
    :return: Словарь, где ключи - это имена модулей, а значения - это сами модули.
    """
    return {
        name: importlib.import_module(name)
        for loader, name, is_pkg in pkgutil.walk_packages(path)
        if is_pkg
    }
