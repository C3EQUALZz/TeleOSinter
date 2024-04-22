"""
Здесь описаны тесты для почты
"""

import pytest
from unittest.mock import patch, AsyncMock

from core.email_scripts import EmailProcessor
from core.factory import ProcessorFactory


def test_is_email_example_dot_com():
    """
    Проверка на то, что проходит почта test@example.com
    """
    assert ProcessorFactory.is_email("test@example.com")


def test_is_email_example_dot_ru():
    """
    Проверка на то, что проходит почта test@example.ru
    """
    assert ProcessorFactory.is_email("test@example.ru")


def test_is_email_example_dot_org():
    """
    Проверка на то, что проходит почта test@example.org
    """
    assert ProcessorFactory.is_email("test@example.org")


def test_is_email_random_correct():
    """
    Проверка на то, что почта yewali9743@togito.com корректна

    Почта взята с temp-mail.org
    """
    assert ProcessorFactory.is_email("yewali9743@togito.com")


def test_is_email_empty_string():
    """
    Проверка на то, что при пустой строке будет false
    """
    assert not ProcessorFactory.is_email("")


def test_is_email_wrong_data():
    """
    Проверка на то, что не проходит почта wrong_data
    """
    assert not ProcessorFactory.is_email("wrong_data")


def test_is_email_without_domain_dot_com():
    """
    Проверка на то, что is_email выдаст false, когда нет домена в строке
    """
    assert not ProcessorFactory.is_email("test@example")


def test_is_email_not_in_sentence():
    """
    Проверка на то, что среди предложения нет почты
    """
    assert not ProcessorFactory.is_email("Привет, мир! Как дела?")


def test_is_email_not_in_sentence_even_with_symbol():
    """
    Проверка на то, что среди предложения нет почты, хотя есть знак '@'
    """
    assert not ProcessorFactory.is_email("Привет, @мир@! Как дела?")


def test_is_email_in_sentence():
    """
    Проверка на то, что в предложении есть почта
    """
    assert ProcessorFactory.is_email("Привет пользователь под почтой, kekw@teml.net")


# @pytest.mark.asyncio
# async def test_create_processor():
#     with patch.object(EmailProcessor, 'handle', new_callable=AsyncMock) as mock_handle:
#         mock_handle.return_value = 'processed'
#         result = await ProcessorFactory.create_processor("test@example.com")
#         mock_handle.assert_called_once_with(email_scripts="test@example.com")
#         assert result == 'processed'
#
#         mock_handle.reset_mock()
#         result = await ProcessorFactory.create_processor("not an email_scripts")
#         mock_handle.assert_not_called()
#         assert result is None


if __name__ == '__main__':
    pytest.main()
