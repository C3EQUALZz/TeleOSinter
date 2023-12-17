"""
Добавить исправления в коде
Оригинал взят отсюда: https://youtu.be/Pr-DsUzgd_A?si=CsoBm-CAoH6OX0eY
"""
__all__ = ["encrypt_file", "decrypt_file"]

import sys

from PyPDF2 import PdfFileWriter, PdfFileReader


def encrypt_file():
    file_path = input("[+] Enter file path: ")
    password = input("[+] Enter password: ")
    encrypted_file_name = input("[+] Enter a name for the encrypted file: ")

    file_writer = PdfFileWriter()

    try:
        file_reader = PdfFileReader(file_path)
    except FileNotFoundError:
        print(f"[INFO] No file with path: {file_path}")
        sys.exit()

    for page in range(file_reader.numPages):
        file_writer.addPage(file_reader.getPage(page))

    file_writer.encrypt(password)

    with open(encrypted_file_name, "wb") as file:
        file_writer.write(file)

    print(f"[+] Created - {encrypted_file_name}")


def decrypt_file():
    file_path = input("[+] Enter file path: ")
    password = input("[+] Enter password: ")
    decrypted_file_name = input("[+] Enter a name for the decrypted file: ")

    file_writer = PdfFileWriter()

    try:
        file_reader = PdfFileReader(file_path)
    except FileNotFoundError:
        print(f"[INFO] No file with path: {file_path}")
        sys.exit()

    if file_reader.isEncrypted:
        file_reader.decrypt(password)

    for page in range(file_reader.numPages):
        file_writer.addPage(file_reader.getPage(page))

    with open(decrypted_file_name, "wb") as file:
        file_writer.write(file)

    print(f"[+] Created - {decrypted_file_name}")
