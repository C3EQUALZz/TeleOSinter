"""
Данный модуль предназначен для установки Telerecon, если он отсутствует.
"""
import subprocess


def clone_telerecon_repository():
    subprocess.call(['git', 'clone', 'https://github.com/ваш-репозиторий/telerecon.git'])


def install_telerecon_repository():
    ...
