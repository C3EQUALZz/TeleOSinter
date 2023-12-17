"""
Данный модуль направлен на взаимодействие в случае отсутствия git.
Может показаться странным, что здесь есть проверка на git, но некоторые люди бывает просто копируют код....
Вставляя в IDE и наслаждаясь этим, поэтому есть такая проверка.
"""
__all__ = ["install_git"]

import platform
import subprocess
import sys

from .custom_errors import *


def _run_command(command: str, message: str) -> bool:
    """
    Выполняет команду с сообщением пользователю и обработкой ошибок.
    """
    print(message)

    try:
        # запуск процесса в терминале, который будет устанавливать зависимости в виде git для дурачков
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Выводит все комментарии для пользователя, если произошла проблема.
        for line in process.stdout:
            sys.stdout.write(line)
        # ожидание, пока закончится скачивание.
        process.wait()

        # В случае кода 1 (его возвращает bash скрипт) будет возмущено исключение
        if process.returncode != 0:
            raise DownloadError(f"Не удалось выполнить команду. Код ошибки: {process.returncode}")

        return True

    except Exception as e:
        raise DownloadError(f"Произошла ошибка: {e}")

    finally:
        sys.stdout.flush()
        sys.stderr.flush()


def _install_git_windows() -> bool:
    """
    В Windows нет по умолчанию git, поэтому будем его автоматически скачивать
    :return: скачивает git, если платформа будет Windows.
    """
    command = 'winget install --id Git.Git -e --source winget'
    return _run_command(command, "Устанавливаю Git. Это может занять несколько минут. Пожалуйста, подождите...")


def _install_git_linux() -> bool:
    """
    Устанавливает git, если его нет на вашем Linux. Есть далеко не вся поддержка.
    :return: Скачивает git, если платформа будет на Linux.
    """
    script_path = "install_git_linux.sh"
    return _run_command(f"bash {script_path}", "Устанавливаю Git. Это может занять несколько минут. Пожалуйста, "
                                               "подождите...")


def _install_git_macos() -> bool:
    """
    Устанавливает git, если его нет на MacOS.
    :return: Скачивает git, если платформа будет на MacOS.
    """
    homebrew_install_command = ('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master'
                                '/install.sh)"')
    git_install_command = 'brew install git'

    # Установка Homebrew
    _run_command(homebrew_install_command,
                 "Устанавливаю Homebrew. Это может занять несколько минут. Пожалуйста, подождите...")

    # Установка Git с использованием Homebrew
    return _run_command(git_install_command, "Устанавливаю Git. Это может занять несколько минут. Пожалуйста, "
                                             "подождите...")


def install_git() -> NoSupport | bool:
    """
    Интерфейс для скачивания git, если его нет на ПК
    :return: скачивает git, пользователь должен будет согласится
    """

    match platform.system():
        case 'Windows':
            return _install_git_windows()

        case "Linux":
            return _install_git_linux()

        case "Darwin":
            return _install_git_macos()

        case _:
            error = (f"Нет поддержки данной операционной системы. Пожалуйста, скачайте вручную git.\n"
                     f"Мануал по установке: https://gist.github.com/derhuerst/1b15ff4652a867391f03 ")
            raise NoSupport(error)
