"""
Данный модуль предназначен для проверки установленных зависимостей.
В случае отсутствия нужных модулей будет автоматически все скачиваться.
"""
import shutil
import subprocess

from .git_checking import install_git
from .telecron_checking import install_telerecon_repository


# Клонирование репозитория
def clone_telerecon_repository():
    subprocess.call(['git', 'clone', 'https://github.com/ваш-репозиторий/telerecon.git'])


def install_all_dependencies() -> None:
    program_and_function = [
        ('git', install_git),
        ('telerecon', install_telerecon_repository),
        ('')
    ]

    for program, function in program_and_function:
        if shutil.which(program) is None:
            function()
