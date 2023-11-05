"""
Данный модуль является основным для реализации логики с телеграмм ботом
"""
# Встроенные библиотеки или посторонние
import os
import asyncio

# Aiogram импорты и дополнение к интерфейсу
import keyboards_telegram
import string_content
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

# Мои заготовленные скрипты


#######################################################################################################################

load_dotenv()
# Связываемся с нашим ботом, используя Telegram API
bot: Bot = Bot(os.getenv("TOKEN"), parse_mode="HTML")
# Класс, который отвечает за обработку событий нашего бота, установка хендлеров и т.п
dp: Dispatcher = Dispatcher()


#######################################################################################################################

# Здесь у нас встроенные команды от Telegram, которые я выбрал в BotFather
@dp.message(Command("start"))
async def start_message(message: Message):
    """
    Этот хэндлер будет срабатывать на команду "/start"
    :param message: сообщение в Telegram
    :return: ответ, где будут указаны возможности мои бота
    """
    await message.reply(f"Привет <b>{message.from_user.first_name}</b>!", **string_content.content.as_kwargs())


@dp.message(Command(commands=["support", "Поддержка"], ignore_case=True))
async def support_message(message: Message):
    """
    Этот handler будет срабатывать на команду "/help"
    :param message: сообщение в Telegram
    :return: ответ, где будут указаны мои контакты для помощи
    """
    await message.answer(string_content.text_support, reply_markup=keyboards_telegram.help_kb)


@dp.message(Command(commands=["menu", "Меню возможностей"], ignore_case=True))
async def help_message(message: Message):
    """
    Этот handler будет срабатывать на команду "/menu"
    :param message: сообщение в Telegram
    :return: ответ, где будут указаны возможности бота
    """
    await message.answer(string_content.text_menu, reply_markup=keyboards_telegram.menu_kb)


########################################################################################################################

@dp.message(F.photo)
async def photo_message(message: Message):
    """
    Этот handler обрабатывает фотографии. Здесь будут присылаться метаданные с фото
    :param message: Фотография от нашего пользователя в Telegram сообщениях.
    :return: Метаданные с фото.
    """
    pass


@dp.message()
async def send_echo(message: Message):
    await message.reply(f'Неизвестная команда')


async def main() -> None:
    # Удаляем каждый раз, чтобы
    await bot.delete_webhook(drop_pending_updates=True)
    # включаем long-polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
