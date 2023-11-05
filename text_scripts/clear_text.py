"""
Здесь будут вспомогательные функции для обработки текстовых вещей
"""


def clear_text_from_tabs(text: str) -> str:
    return "\n".join(line.lstrip() for line in text.split("\n"))
