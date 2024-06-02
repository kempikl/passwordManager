import os
import json
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import string
import secrets
from password_entry import PasswordEntry


def generate_key(password: str) -> bytes:
    """
    Generuje klucz szyfrowania na podstawie hasła użytkownika.

    Args:
        password (str): Hasło użytkownika.

    Returns:
        bytes: Wygenerowany klucz szyfrowania.
    """
    salt = b'\x00' * 16
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def generate_password(length=16) -> str:
    """
    Generuje hasło o podanej długości.

    Args:
        length (int): Długość hasła. Domyślnie 16.

    Returns:
        str: Wygenerowane hasło.
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


class PasswordManager:
    """
    Klasa zarządzająca hasłami użytkownika.

    Attributes:
        key (bytes): Klucz szyfrowania wygenerowany z hasła głównego.
        filename (str): Nazwa pliku do przechowywania zaszyfrowanych haseł.
        passwords (dict): Słownik przechowujący obiekty PasswordEntry.
    """
    def __init__(self, master_password):
        self.key = generate_key(master_password)
        self.filename = 'passwords.enc'
        self.passwords = self.load_passwords()

    def save_passwords(self):
        """
        Szyfruje i zapisuje hasła do pliku.
        """
        fernet = Fernet(self.key)
        encrypted_data = fernet.encrypt(json.dumps([entry.__dict__ for entry in self.passwords.values()]).encode())
        with open(self.filename, 'wb') as file:
            file.write(encrypted_data)

    def load_passwords(self) -> dict:
        """
        Odczytuje i deszyfruje hasła z pliku.

        Returns:
            dict: Słownik przechowujący obiekty PasswordEntry.
        """
        if not os.path.exists(self.filename):
            return {}
        fernet = Fernet(self.key)
        try:
            with open(self.filename, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            password_dicts = json.loads(decrypted_data)
            return {entry['site']: PasswordEntry(entry['site'], entry['username'], entry['password'], entry['pwned'])
                    for entry in password_dicts}
        except (InvalidToken, json.JSONDecodeError):
            print("Niepoprawne hasło lub uszkodzone dane. Spróbuj ponownie.")

    def add_password(self, site, username, password):
        """
        Dodaje nowe hasło i sprawdza czy zostało skompromitowane.

        Args:
            site (str): Nazwa strony.
            username (str): Nazwa użytkownika.
            password (str): Hasło.
        """
        entry = PasswordEntry(site, username, password)
        if entry.pwned:
            print("To hasło zostało skompromitowane.")
        self.passwords[site] = entry
        self.save_passwords()
        print("Hasło dodane pomyślnie.")

    def remove_password(self, site):
        """
        Usuwa hasło dla podanej strony.

        Args:
            site (str): Nazwa strony.
        """
        if site in self.passwords:
            del self.passwords[site]
            self.save_passwords()
            print("Hasło usunięte pomyślnie.")
        else:
            print("Nie znaleziono hasła dla podanej strony.")

    def search_password(self, site):
        """
        Wyszukuje i wyświetla hasło dla podanej strony.

        Args:
            site (str): Nazwa strony.
        """
        if site in self.passwords:
            entry = self.passwords[site]
            print(f"Strona: {entry.site}")
            print(f"Nazwa użytkownika: {entry.username}")
            print(f"Hasło: {entry.password}")
            print(f"Skompromitowane: {'Tak' if entry.pwned else 'Nie'}")
        else:
            print("Nie znaleziono hasła dla podanej strony.")

    def display_passwords(self):
        """
         Wyświetla wszystkie zapisane hasła.
        """
        if not self.passwords:
            print("Brak zapisanych haseł.")
        else:
            for entry in self.passwords.values():
                print(
                    f"Strona: {entry.site}, Nazwa użytkownika: {entry.username}, Skompromitowane: "
                    f"{'Tak' if entry.pwned else 'Nie'}")
