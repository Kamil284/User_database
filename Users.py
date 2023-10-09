import os
import json

DB = {}
db_manager = None  # Przechowuje jedną wspólną instancję DBManager


class DBManager:
    def __init__(self, filename: str = "users.json") -> None:
        self.filename = filename
        if not self.file_exists():
            self.create_db()  # tworzymy nową bazę danych
        self.load_db()  # Wczytujemy istniejącą bazę danych

    def file_exists(self) -> bool:
        return os.path.exists(self.filename)

    def create_db(self) -> None:
        with open(self.filename, 'w') as file:
            json.dump({}, file)  # tworzy pusty plik JSON, który będzie bazą danych

    def load_db(self) -> None:
        with open(self.filename, 'r') as file:
            global DB
            DB = json.load(file)  # Wczytuje dane z pliku JSON do zmiennej globalnej DB

    def add_new_record(self, user_data: dict) -> None:
        global DB
        user_id = len(DB) + 1
        DB[user_id] = user_data  # dodaje nowy rekord do bazy danych

    def save_db(self) -> None:
        with open(self.filename, 'w') as file:
            json.dump(DB, file)  # apisuje aktualny stan bazy danych do pliku JSON


class User:
    def __init__(self, name: str, surname: str, date_birth: str):
        self.name = name
        self.surname = surname
        self.date_birth = date_birth

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "surname": self.surname,
            "date_birth": self.date_birth
        }

    def save(self) -> None:
        user_data = self.to_dict()
        db_manager.add_new_record(user_data)  # dodaje użytkownika do bazy danych
        db_manager.save_db()  # apisuje bazę danych do pliku

    def print_data(self) -> None:
        print(f"Name: {self.name}")
        print(f"Surname: {self.surname}")
        print(f"Date of Birth: {self.date_birth}")


class UserManager:
    def add_user(self):
        print('Add new user ')
        name = input('Name: ')
        surname = input('Surname: ')
        date_birth = input('Date of birth: ')

        new_user = User(name, surname, date_birth)
        new_user.save()  # Dodajemy nowego użytkownika i zapisujemy bazę danych
        print("User added successfully.")

    def view_users(self):
        print("View Users Menu:")
        print("1. View All Users")
        print("2. View User by ID")
        print("3. Back to Main Menu")

        choice = input("Your choice: ")

        if choice == "1":
            self.view_all_users()
        elif choice == "2":
            self.view_user_by_id()
        elif choice == "3":
            print("Returning to Main Menu.")
        else:
            print("Invalid choice. Please select a valid option.")

    def view_all_users(self):
        print("List of all users:")
        for user_id, user_data in DB.items():
            user = User(**user_data)
            print(f"User ID: {user_id}")
            user.print_data()
            print()

    def view_user_by_id(self):
        user_id = input("Enter the user ID you want to view (or 'Q' to quit): ")
        if user_id.upper() == 'Q':
            return

        try:
            user_id = int(user_id)
            user_data = DB.get(user_id)
            if user_data:
                user = User(**user_data)
                user.print_data()
            else:
                print("User not found.")
        except ValueError:
            print("Invalid user ID. Please enter a valid number.")

if __name__ == "__main__":
    db_manager = DBManager()

    while True:
        print("Menu:")
        print("1. Add User")
        print("2. View Users")
        print("3. Select User by ID")
        print("4. Exit")

        choice = input("Your choice: ")

        if choice == "1":
            UserManager().add_user()
        elif choice == "2":
            UserManager().view_users()
        elif choice == "3":
            UserManager().select_user()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")