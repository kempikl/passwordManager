# Menedżer Haseł

Menedżer Haseł to aplikacja konsolowa napisana w Pythonie, która umożliwia bezpieczne przechowywanie i zarządzanie hasłami użytkowników. Aplikacja oferuje funkcje takie jak dodawanie, usuwanie, przeszukiwanie haseł, generowanie silnych haseł oraz wyświetlanie wszystkich zapisanych danych. Dodatkowo, aplikacja sprawdza, czy hasło zostało skompromitowane, korzystając z API `haveibeenpwned.com`.

## Funkcjonalności

- **Zarządzanie hasłami**: Dodawanie, usuwanie oraz wyszukiwanie zapisanych haseł.
- **Generowanie silnych haseł**: Możliwość generowania trudnych do złamania haseł.
- **Sprawdzanie skompromitowania haseł**: Weryfikacja, czy hasło zostało ujawnione w znanych wyciekach danych za pomocą API `haveibeenpwned.com`.
- **Szyfrowanie danych**: Bezpieczne przechowywanie haseł przy użyciu szyfrowania symetrycznego Fernet z biblioteki `cryptography`.

## Użyte Technologie

- **Python 3.10+**
- **cryptography**: Do szyfrowania danych.
- **requests**: Do komunikacji z API `haveibeenpwned.com`.

## Struktura Plików

- `password_entry.py`: Zawiera klasę `PasswordEntry`.
- `password_manager.py`: Zawiera klasę `PasswordManager`.
- `main.py`: Zawiera funkcję `main`. Służy do uruchomienia programu.

## Użycie

Po uruchomieniu aplikacji zostaniesz poproszony o wprowadzenie głównego hasła, które będzie używane do szyfrowania i deszyfrowania danych. Następnie będziesz mieć dostęp do menu z następującymi opcjami:

1. **Wyświetl zapisane hasła**
2. **Dodaj hasło**
3. **Usuń hasło**
4. **Szukaj hasła**
5. **Generuj hasło**
6. **Zakończ**

### Przykład

```text
Menedżer Haseł
1. Wyświetl zapisane hasła
2. Dodaj hasło
3. Usuń hasło
4. Szukaj hasła
5. Generuj hasło
6. Zakończ

Wybierz opcję: 1
Wprowadź nazwę strony: example.com
Wprowadź nazwę użytkownika: user123
Wprowadź hasło: ********
Hasło dodane pomyślnie.
```

### Szyfrowanie
Aplikacja korzysta z szyfrowania symetrycznego Fernet z biblioteki `cryptography` do bezpiecznego przechowywania haseł. Klucz szyfrowania jest generowany na podstawie hasła głównego użytkownika przy użyciu algorytmu PBKDF2 z SHA-256. Dane są szyfrowane i deszyfrowane przy użyciu tego klucza, co zapewnia ich poufność i integralność.
