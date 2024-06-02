import getpass
from password_manager import PasswordManager, generate_password


def main():
    """
    Główna funkcja uruchomieniowa. Odpowiada za interfejs użytkownika.
    """
    while True:
        password = getpass.getpass('Wprowadź hasło: ')
        manager = PasswordManager(password)
        if manager.passwords is not None:
            break

    while True:
        print("\nMenedżer Haseł")
        print("1. Wyświetl zapisane hasła")
        print("2. Dodaj hasło")
        print("3. Usuń hasło")
        print("4. Szukaj hasła")
        print("5. Generuj hasło")
        print("6. Zakończ")

        choice = input("Wybierz opcję: ")

        match choice:
            case '1':
                manager.display_passwords()
            case '2':
                site = input("Wprowadź nazwę strony: ")
                user = input("Wprowadź nazwę użytkownika: ")
                pwd = getpass.getpass("Wprowadź hasło: ")
                manager.add_password(site, user, pwd)
            case '3':
                site = input("Wprowadź nazwę strony do usunięcia: ")
                manager.remove_password(site)
            case '4':
                site = input("Wprowadź nazwę strony do wyszukania: ")
                manager.search_password(site)
            case '5':
                try:
                    length = int(input("Wprowadź pożądaną długość hasła (16): "))
                    print(f"Wygenerowane hasło: {generate_password(length)}")
                except ValueError:
                    print(f"Wygenerowane hasło: {generate_password()}")
            case '6':
                break
            case _:
                print("Nieprawidłowy wybór. Spróbuj ponownie.")


if __name__ == "__main__":
    main()
