"""
https://youtu.be/_rUpNlFh5UU?si=ZEx78vC59JQ1A7Qm
"""
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import secrets
import base64
import getpass
import argparse


def generate_salt(size=16):
    return secrets.token_bytes(size)


def load_salt():
    return open("salt.salt", "rb").read()


def derive_key(salt, password):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())


def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    if load_existing_salt:
        salt = load_salt()
    elif save_salt:
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)

    derived_key = derive_key(salt, password)
    return base64.urlsafe_b64encode(derived_key)


def encrypt(filename, key):
    f = Fernet(key)

    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()

    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("Недопустимый токен.")
        return

    with open(filename, "wb") as file:
        file.write(decrypted_data)

    print("Файл успешно расшифрован")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт для шифрования/дешифрования файлов с паролем")
    parser.add_argument("file", help="Файл для шифрования/дешифрования")
    parser.add_argument("-s", "--salt-size",
                        help="Если это значение задано, генерируется новая соль с переданным размером", type=int)
    parser.add_argument("-e", "--encrypt", action="store_true", help="Зашифровать файл")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Расшифровать файл")

    args = parser.parse_args()
    file = args.file

    if args.encrypt:
        password = getpass.getpass("Введите пароль для шифрования: ")
    elif args.decrypt:
        password = getpass.getpass("Введите пароль, который вы использовали для шифрования: ")

    if args.salt_size:
        key = generate_key(password, salt_size=args.salt_size, save_salt=True)
    else:
        key = generate_key(password, load_existing_salt=True)

    encrypt_ = args.encrypt
    decrypt_ = args.decrypt

    if encrypt_ and decrypt_:
        raise TypeError("Пожалуйста, укажите, хотите ли вы зашифровать файл или расшифровать его.")
    elif encrypt_:
        encrypt(file, key)
    elif decrypt_:
        decrypt(file, key)
    else:
        raise TypeError("Пожалуйста, укажите, хотите ли вы зашифровать файл или расшифровать его.")