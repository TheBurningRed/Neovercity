from collections import UserDict
from datetime import datetime, timedelta
import re
import pickle


class ContactError(Exception):
    pass


class PhoneValidationError(ContactError):
    pass


class DateValidationError(ContactError):
    pass


class RecordNotFoundError(ContactError):
    pass


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid format. Check that the arguments are entered correctly."
        except IndexError:
            return "Insufficient arguments. Enter a command, name, and optionally a value."
        except KeyError:
            return "Contact not found."
        except PhoneValidationError as e:
            return str(e)
        except DateValidationError as e:
            return str(e)
        except RecordNotFoundError as e:
            return str(e)
        except Exception as e:
            return f"Raised other error: {e}"
    return inner


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not re.fullmatch(r"^\d{10}$", new_value):
            raise PhoneValidationError("The phone number must consist of exactly 10 digits.")
        self._value = new_value

    def __init__(self, value):
        self.value = value


class Birthday(Field):
    def __init__(self, value):
        try:
            date_obj = datetime.strptime(value, "%d.%m.%Y").date()
            self._value = date_obj
        except ValueError:
            raise DateValidationError("Invalid date format. Use DD.MM.YYYY")

    @property
    def value(self):
        return self._value

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday: str):
        try:
            self.birthday = Birthday(birthday)
            return f"Birthday {birthday} added for contact {self.name.value}."
        except DateValidationError as e:
            return str(e)

    def add_phone(self, phone_number: str):
        try:
            phone = Phone(phone_number)
            if phone.value not in [p.value for p in self.phones]:
                self.phones.append(phone)
                return f"Phone {phone_number} added to contact {self.name.value}."
            else:
                return f"The number {phone_number} already exists for contact {self.name.value}."
        except PhoneValidationError as e:
            return str(e)

    def find_phone(self, phone_number: str) -> Phone | None:
        for p in self.phones:
            if p.value == phone_number:
                return p
        return None

    def edit_phone(self, old_phone: str, new_phone: str):
        phone_obj = self.find_phone(old_phone)

        if phone_obj is None:
            return f"Error: Number {old_phone} not found for contact {self.name.value}."

        try:
            phone_obj.value = new_phone
            return f"Phone {old_phone} successfully updated to {new_phone}."
        except PhoneValidationError as e:
            return str(e)

    def remove_phone(self, phone_number: str):
        phone_obj = self.find_phone(phone_number)
        if phone_obj:
            self.phones.remove(phone_obj)
            return f"Phone {phone_number} deleted for contact {self.name.value}."
        else:
            return f"Error: Number {phone_number} not found for contact {self.name.value}."

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return f"Record for contact {record.name.value} added."

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
            return f"Record for contact {name} deleted."
        else:
            raise RecordNotFoundError(f"Record with name {name} not found.")

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.now().date()
        next_week = today + timedelta(days=7)

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday_date = record.birthday.value
            bday_this_year = bday_date.replace(year=today.year)

            if bday_this_year < today:
                bday_this_year = bday_date.replace(year=today.year + 1)

            if today <= bday_this_year <= next_week:
                if bday_this_year.weekday() >= 5:
                    days_until_monday = (7 - bday_this_year.weekday())
                    bday_this_year += timedelta(days=days_until_monday)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": bday_this_year.strftime("%d.%m.%Y")
                })

        return upcoming_birthdays


def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)

    if record:
        return record.add_phone(phone)
    else:
        new_record = Record(name)
        new_record.add_phone(phone)
        return book.add_record(new_record)


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError
    return record.edit_phone(old_phone, new_phone)


@input_error
def show_phone(args, book: AddressBook):
    name, = args
    record = book.find(name)
    if record is None:
        raise KeyError

    if not record.phones:
        return f"Contact {name} has no phone numbers."

    phones_str = "; ".join([p.value for p in record.phones])
    return f"Numbers for {name}: {phones_str}"


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "The address book is empty."

    result = "All contacts:\n"
    for record in book.data.values():
        result += str(record) + "\n"
    return result.strip()


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError

    return record.add_birthday(birthday)


@input_error
def show_birthday(args, book: AddressBook):
    name, = args
    record = book.find(name)
    if record is None:
        raise KeyError

    if record.birthday:
        return f"Birthday for {name}: {record.birthday}"
    else:
        return f"The birthday is not set for contact {name}."

@input_error
def upcoming_birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "There are no birthdays next week."

    output = "Upcoming birthdays:\n"
    for item in upcoming:
        output += f"- {item['name']} needs to be congratulated on: {item['congratulation_date']}\n"
    return output.strip()


def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": upcoming_birthdays,
    }

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye! Data saved.")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command in commands:
            if command == "all" or command == "birthdays":
                print(commands[command](book))
            else:
                print(commands[command](args, book))

        else:
            print(
                "Invalid command. Use hello for greeting, "
                "add to add contact, change to change contact, "
                "phone to show phone, all to show all contacts, "
                "add-birthday to add birthday, show-birthday to show birthday, "
                "birthdays to show upcoming birthdays."
            )


if __name__ == "__main__":
    main()
