"""
Данный модуль предназначен только для написания логики клавиатур
"""
__all__ = ["main_kb", "help_kb", "menu_kb"]

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# Клавиатура, которая появляется, когда пользователь нажал "/start"
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню возможностей"),
            KeyboardButton(text="Поддержка")
        ]
    ],
    # оптимизация для телефонов
    resize_keyboard=True,
    # скрытие клавиатуры, а не удаление
    one_time_keyboard=True,
    # текст по умолчанию для выбора действия
    input_field_placeholder="Выберите действие",
    # клавиатура видна не у всех, если бота добавили в беседу
    selective=True
)

# Клавиатура, которая появляется, когда пользователь нажал "/help"
help_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Связаться с автором", url="tg://resolve?domain=C3EQUALZ"),
            InlineKeyboardButton(text="Посмотреть проект на GitHub", url="https://github.com/C3EQUALZz/TeleOSinter")
        ]
    ],
    # оптимизация для телефонов
    resize_keyboard=True,
    # скрытие клавиатуры, а не удаление
    one_time_keyboard=True,
    # текст по умолчанию для выбора действия
    input_field_placeholder="Выберите предложенное действие",
    # клавиатура видна не у всех, если бота добавили в беседу
    selective=True
)

# Клавиатура, которая появляется, когда пользователь нажал "/menu"
menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Узнать информацию по номеру телефона"),
            InlineKeyboardButton(text="Узнать информацию Вконтакте")
        ],
        [
            InlineKeyboardButton(text="Анализ метаданных по фото"),
            InlineKeyboardButton(text="Узнать информацию по IP")
        ]
    ],
    # оптимизация для телефонов
    resize_keyboard=True,
    # скрытие клавиатуры, а не удаление
    one_time_keyboard=True,
    # текст по умолчанию для выбора действия
    input_field_placeholder="Выберите действие",
    # клавиатура видна не у всех, если бота добавили в беседу
    selective=True
)
