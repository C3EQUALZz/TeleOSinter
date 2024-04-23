"""
Здесь описаны тесты для почты
"""

from unittest.mock import AsyncMock

import pytest

from core.email_scripts import EmailProcessor
from core.factory import ProcessorFactory


def test_is_email_example_dot_com():
    """
    Проверка на то, что проходит почта test@example.com
    """
    assert bool(ProcessorFactory.is_email("test@example.com")) is True


def test_is_email_example_dot_ru():
    """
    Проверка на то, что проходит почта test@example.ru
    """
    assert bool(ProcessorFactory.is_email("test@example.ru")) is True


def test_is_email_example_dot_org():
    """
    Проверка на то, что проходит почта test@example.org
    """
    assert bool(ProcessorFactory.is_email("test@example.org")) is True


def test_is_email_random_correct():
    """
    Проверка на то, что почта yewali9743@togito.com корректна

    Почта взята с temp-mail.org
    """
    assert bool(ProcessorFactory.is_email("yewali9743@togito.com")) is True


def test_is_email_empty_string():
    """
    Проверка на то, что при пустой строке будет false
    """
    assert bool(ProcessorFactory.is_email("")) is False


def test_is_email_wrong_data():
    """
    Проверка на то, что не проходит почта wrong_data
    """
    assert bool(ProcessorFactory.is_email("wrong_data")) is False


def test_is_email_without_domain_dot_com():
    """
    Проверка на то, что is_email выдаст false, когда нет домена в строке
    """
    assert bool(ProcessorFactory.is_email("test@example")) is False


def test_is_email_not_in_sentence():
    """
    Проверка на то, что среди предложения нет почты
    """
    assert bool(ProcessorFactory.is_email("Привет, мир! Как дела?")) is False


def test_is_email_not_in_sentence_even_with_symbol():
    """
    Проверка на то, что среди предложения нет почты, хотя есть знак '@'
    """
    assert bool(ProcessorFactory.is_email("Привет, @мир@! Как дела?")) is False


def test_is_email_in_sentence():
    """
    Проверка на то, что в предложении есть почта
    """
    assert bool(ProcessorFactory.is_email("Привет пользователь под почтой, kekw@teml.net")) is True


def test_is_email_get_email():
    """
    Проверка на то, что наш метод правильно достает почту из предложения
    """
    assert ProcessorFactory.is_email("Привет пользователь под почтой, kekw@teml.net") == "kekw@teml.net"


@pytest.mark.asyncio
async def test_create_processor_if_email_sentence(mocker):
    """
    Тест для функции create_processor класса ProcessorFactory.

    Этот тест проверяет, что функция create_processor правильно обрабатывает сообщения,
    содержащие адрес электронной почты. В частности, тест проверяет, что при наличии адреса
    электронной почты в сообщении вызывается метод handle класса EmailProcessor и возвращается
    корректная строка.

    :param mocker: фикстура pytest-mock, используется для создания мок-объекта для метода handle.

    Предполагается, что возвращаемое значение метода handle - это строка "Email processed".

    Проверки:
    - Результат является строкой.
    - Результат не пустой.
    - Результат равен "Email processed".
    - Метод handle вызывается ровно один раз с адресом электронной почты "test@example.com".
    """

    mock_handle = mocker.patch.object(
        EmailProcessor,
        'handle',
        new_callable=AsyncMock,
        return_value="Email processed"
    )

    result = await ProcessorFactory.create_processor("My email is test@example.com")

    assert isinstance(result, str)
    assert len(result) > 0
    assert result == "Email processed"

    mock_handle.assert_called_once_with(email="test@example.com")


@pytest.mark.asyncio
async def test_create_processor_if_email_not_in_sentence():
    """
    Тест для функции create_processor класса ProcessorFactory.

    Этот тест проверяет, что функция create_processor правильно обрабатывает сообщения,
    содержащие адрес электронной почты. В частности, тест проверяет, что при отсутствии адреса
    электронной почты в сообщении не вызывается ни один метод, возвращается, что ничего не найдено
    """
    result = await ProcessorFactory.create_processor("My email is test@example")

    assert isinstance(result, str)
    assert len(result) > 0
    assert result == "Ничего не распознано"


if __name__ == '__main__':
    pytest.main()
