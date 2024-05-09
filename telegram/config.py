"""
Модуль, который отвечает за конфигурацию бота
"""
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN: str = env("TOKEN")
#ADMIN_ID: int = env.int("ADMIN_TOKEN")


