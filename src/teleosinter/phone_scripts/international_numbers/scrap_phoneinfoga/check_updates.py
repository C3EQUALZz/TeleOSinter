"""
Оригинальный репозиторий с логикой phoneinfoga описан здесь:
https://github.com/la-deep-web/Phoneinfoga
Там есть папка OSINT, где лежат нужные json для парсинга данных

Ссылка 2 по поводу почему не while True:
https://stackoverflow.com/questions/8867043/is-there-any-case-in-python-when-using-a-while-loop-would-be-best-practice
"""
import json
########################################################################################################################
import os
from datetime import datetime
import pathlib
import fake_useragent
########################################################################################################################
import aiohttp
import aiofiles
import asyncio

########################################################################################################################

OSINT_FILES = (
    'disposable_num_providers.json',
    'individuals.json',
    'reputation.json',
    'social_medias.json'
)

HEADERS = {'User-Agent': fake_useragent.UserAgent().random}


async def update_files_for_phoneinfoga(directory_path: str) -> None:
    """
    Будут автоматически обновляться файлы, если разница между временем скачивания файла и текущего будет неделя.
    :param directory_path: Путь к папке, где мы собираемся все обновить
    :return: Ничего не возвращает, только обновляет данные.
    """
    # Если не существует файла, то мы создаем директорию и будем позже добавлять json
    if not os.path.exists("osint"):
        os.mkdir("osint")

    # время создания файла
    date_creating_file = os.path.getctime(directory_path)
    # текущее время системы
    current_time = datetime.now().timestamp()
    # Раз в неделю будут скачиваться заново файлы или если у пользователя не существует папки osint в данном проекте
    if current_time - date_creating_file > 7 * 24 * 60 * 60 or len(tuple(pathlib.Path('').iterdir())):
        await _download_files(directory_path)


async def _download_files(directory_path: str) -> None:
    """
    Данная функция будет скачивать все json файлы с репозитория, которые находятся в папке osint
    """
    for file in OSINT_FILES:
        url = f'https://raw.githubusercontent.com/la-deep-web/Phoneinfoga/master/osint/{file}'
        output_directory = f"{directory_path}/{file}"
        await _download_file(url, output_directory)


async def _download_file(url: str, output_directory: str) -> None:
    """
    Асинхронное скачивание файла
    """
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url, chunked=True) as response:

            if response.status == 200:
                await _save_response_content(response, output_directory)
            else:
                raise ValueError(f"Ошибка скачивания файла. Статус код: {response.status}")


async def _save_response_content(response: aiohttp.ClientResponse, output_directory: str) -> None:
    """
    Данная функция сохраняет данные в файл после запроса
    """
    # Записываем измененные JSON-данные обратно в файл
    async with aiofiles.open(output_directory, 'w') as file:
        await file.write(await response.text())


async def main():
    directory_path = "osint"
    await update_files_for_phoneinfoga(directory_path)


if __name__ == "__main__":
    asyncio.run(main())
