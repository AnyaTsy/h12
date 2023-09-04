import json
from collections import UserDict
import datetime

class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        if not self.is_valid_phone():
            raise ValueError("Invalid phone number")

    def is_valid_phone(self) -> bool:
        return all(char.isdigit() for char in self.value) and len(self.value) <= 15

class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        if not self.is_valid_birthday():
            raise ValueError("Invalid birthday format")

    def is_valid_birthday(self) -> bool:
        try:
            datetime.datetime.strptime(self.value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}"

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.date.today()
            next_birthday = datetime.date(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime.date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_until_birthday = (next_birthday - today).days
            return days_until_birthday
        else:
            return "Birthday not specified"

    def __str__(self) -> str:
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"

    def iterator(self, n):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i + n]

    def save_to_file(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.data, file)

    def load_from_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            pass

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
def main():
    address_book = AddressBook()
    file_name = "address_book.json"  # Имя файла для сохранения и загрузки

    # Попробуйте загрузить данные из файла при запуске программы
    address_book.load_from_file(file_name)

    while True:
        user_input = input(">>> ").strip()
        if user_input.lower() in ["good bye", "close", "exit"]:
            print("Good bye!")
            # Сохраните данные в файл перед выходом
            address_book.save_to_file(file_name)
            break

        command, *args = user_input.split()

        if command == "add":
            if len(args) < 2:
                print("Please provide name and phone number.")
                continue
            name, phone = args[0], args[1]
            birthday = None 
            if len(args) >= 3:
                birthday = Birthday(args[2])

            if name in address_book:
                print(f"Contact {name} already exists.")
            else:
                record = Record(Name(name), Phone(phone), birthday)  # Передача дня народження
                address_book.add_record(record)
                print(f"Contact {name} added with phone {phone} and birthday {args[2] if birthday else 'not specified'}.")

        elif command == "change":
            if len(args) < 2:
                print("Please provide name and phone number.")
                continue
            name, phone = args[0], args[1]
            if name not in address_book:
                print(f"Contact {name} not found.")
            else:
                record = address_book[name]
                record.change_phone(record.phones[0], Phone(phone))
                print(f"Contact {name} updated with new phone {phone}.")

        elif command == "phone":
            if not args:
                print("Please provide a name.")
                continue
            name = args[0]
            if name not in address_book:
                print(f"Contact {name} not found.")
            else:
                record = address_book[name]
                print(f"The phone number for {name} is {record.phones[0].value}.")

        elif command == "show":
            if len(args) > 0 and args[0] == "all":
                if not address_book:
                    print("No contacts found.")
                else:
                    print("Contacts:")
                    for name, record in address_book.items():
                        print(f"{name}: {record.phones[0].value}")
            else:
                print("Unknown command")

        elif command == "days_to_birthday":  
            if not args:
                print("Please provide a name.")
                continue
            name = args[0]
            if name not in address_book:
                print(f"Contact {name} not found.")
            else:
                record = address_book[name]
                print(record.days_to_birthday())

        elif command == "save":
            # Сохранить данные в файл вручную
            address_book.save_to_file(file_name)
            print("Address book saved to file.")

        elif command == "load":
            # Загрузить данные из файла вручную
            address_book.load_from_file(file_name)
            print("Address book loaded from file.")

        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
