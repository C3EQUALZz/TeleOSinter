"""
Здесь описаны тесты для почты
"""

from unittest.mock import AsyncMock

import pytest

from teleosinter.core.factory import ProcessorFactory
from teleosinter.email_scripts import EmailProcessor


@pytest.mark.parametrize("test_input, expected", [
    ("test@example.com", True),
    ("test@example.ru", True),
    ("test@example.org", True),
    ("yewali9743@togito.com", True),
    ("", False),
    ("wrong_data", False),
    ("test@example", False),
    ("Привет, мир! Как дела?", False),
    ("Привет, @мир@! Как дела?", False),
    ("Привет пользователь под почтой, kekw@teml.net", True),
    ("Привет пользователь под почтой, kekw@teml.net", "kekw@teml.net")
])
def test_is_email_correct(test_input: str, expected: bool | str):
    """
    Проверка на то, что проходит почта test@example.com
    """
    assert bool(ProcessorFactory.is_email("test@example.com")) is True


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

    result = await ProcessorFactory.create_processor("My email_utils is test@example.com")

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
    result = await ProcessorFactory.create_processor("My email_utils is test@example")

    assert isinstance(result, str)
    assert len(result) > 0
    assert result == "Ничего не распознано"


if __name__ == '__main__':
    pytest.main()
