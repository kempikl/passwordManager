import hashlib
import requests


class PasswordEntry:
    """
       Klasa reprezentująca pojedynczy wpis hasła.

       Attributes:
           site (str): Nazwa strony.
           username (str): Nazwa użytkownika.
           password (str): Hasło.
           pwned (bool): Flaga wskazująca czy hasło zostało skompromitowane.
       """
    def __init__(self, site, username, password, pwned=None):
        self.site = site
        self.username = username
        self.password = password
        if pwned is None:
            self.pwned = self.check_pwned_password(password)
        else:
            self.pwned = pwned

    @staticmethod
    def check_pwned_password(password: str) -> bool:
        """
        Sprawdza czy hasło zostało skompromitowane korzystając z API haveibeenpwned.com.

        Args:
            password (str): Hasło do weryfikacji.

        Returns:
            bool: True, jeśli hasło zostało skompromitowane, False w przeciwnym razie.
        """
        sha1password = hashlib.sha1(password.encode()).hexdigest().upper()
        first5_chars, rest = sha1password[:5], sha1password[5:]
        url = f"https://api.pwnedpasswords.com/range/{first5_chars}"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Błąd podczas komunikacji z API: {e}")
            return False
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == rest:
                return True
        return False
