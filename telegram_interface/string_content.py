"""
Здесь будут сохраняться все нужные мне описания
"""
__all__ = ["content", "text_support", "text_menu"]

from aiogram.utils.formatting import as_list, as_marked_section, Text
from text_scripts.clear_text import clear_text_from_tabs

content: Text = as_list(
    as_marked_section(
        "Я разработан, как проект в области ИБ.\nУ меня есть такие возможности, как: ",
        "☎ Узнать информацию по номеру телефона.",
        "🌐 Узнать информацию по Вконтакте. ",
        "💥 Анализ метаданных по фото",
        marker="  ",
    ), sep="\n\n")

text_support: str = clear_text_from_tabs(f"""
    Если у вас есть вопросы или предложения, вы можете связаться с автором. 
    Рабочее время с 10.00 до 18.00 по Московскому времени. 
    """)


text_menu: str = clear_text_from_tabs(f"""
    Откройте для себя бесконечные возможности для экспериментов и поиска нужной информации
    
    <b>Выберите нужное действие</b>:
    """)
