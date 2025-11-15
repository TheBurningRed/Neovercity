import pickle
import re
from collections import UserDict
from datetime import datetime, timedelta
from difflib import get_close_matches

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion


# Exceptions
class ContactError(Exception):
    pass


class PhoneValidationError(ContactError):
    pass


class DateValidationError(ContactError):
    pass


class RecordNotFoundError(ContactError):
    pass


# Error handler
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            return "Invalid input. Please check your command."
        except KeyError:
            return "Contact not found."
        except (
            PhoneValidationError,
            DateValidationError,
            RecordNotFoundError
        ) as e:
            return str(e)
        except Exception as e:
            return f"Unexpected error: {e}"

    return wrapper


# Data persistence
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


# Field classes
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
    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, new_value):
        if not re.fullmatch(r"\d{10}", new_value):
            raise PhoneValidationError(
                "Phone number must be exactly 10 digits."
            )
        self._value = new_value


class Birthday(Field):
    def __init__(self, value):
        try:
            self._value = datetime.strptime(
                value, "%d.%m.%Y"
            ).date()
        except ValueError:
            raise DateValidationError(
                "Invalid date format. Use DD.MM.YYYY"
            )

    def __str__(self):
        return self._value.strftime("%d.%m.%Y")


# Record class
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        phone_obj = Phone(phone)

        if phone_obj.value not in [p.value for p in self.phones]:
            self.phones.append(phone_obj)
            return (
                f"Phone {phone} added to {self.name.value}."
            )

        return (
            f"Phone {phone} already exists for "
            f"{self.name.value}."
        )

    def find_phone(self, phone):
        return next(
            (p for p in self.phones if p.value == phone),
            None
        )

    def edit_phone(self, old, new):
        phone_obj = self.find_phone(old)
        if not phone_obj:
            return (
                f"Phone {old} not found for "
                f"{self.name.value}."
            )

        phone_obj.value = new
        return (
            f"Phone {old} updated to {new}."
        )

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)

        if phone_obj:
            self.phones.remove(phone_obj)
            return (
                f"Phone {phone} removed from "
                f"{self.name.value}."
            )

        return (
            f"Phone {phone} not found for "
            f"{self.name.value}."
        )

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return (
            f"Birthday {birthday} added to "
            f"{self.name.value}."
        )

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        bday = (
            f", birthday: {self.birthday}"
            if self.birthday else ""
        )

        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones}{bday}"
        )


# AddressBook class
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        return f"Record for {record.name.value} added."

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record for {name} deleted."

        raise RecordNotFoundError(
            f"No record found for {name}."
        )

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday = record.birthday.value.replace(
                year=today.year
            )

            if bday < today:
                bday = bday.replace(
                    year=today.year + 1
                )

            if today <= bday <= next_week:
                if bday.weekday() >= 5:
                    bday += timedelta(
                        days=(7 - bday.weekday())
                    )

                result.append({
                    "name": record.name.value,
                    "congratulation_date": (
                        bday.strftime("%d.%m.%Y")
                    )
                })

        return result


# Command parsing
def parse_input(user_input):
    parts = user_input.strip().split()

    if not parts:
        return "", []

    return parts[0].lower(), parts[1:]


# Command handlers
@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)

    if record:
        return record.add_phone(phone)

    record = Record(name)
    record.add_phone(phone)
    return book.add_record(record)


@input_error
def change_contact(args, book):
    name, old, new = args
    record = book.find(name)

    if not record:
        raise KeyError

    return record.edit_phone(old, new)


@input_error
def show_phone(args, book):
    (name,) = args
    record = book.find(name)

    if not record:
        raise KeyError

    if not record.phones:
        return f"{name} has no phone numbers."

    return (
        "Numbers for {name}: {numbers}".format(
            name=name,
            numbers="; ".join(
                p.value for p in record.phones
            )
        )
    )


@input_error
def show_all(book):
    if not book.data:
        return "Address book is empty."

    return "\n".join(
        str(record) for record in book.data.values()
    )


@input_error
def add_birthday(args, book):
    name, bday = args
    record = book.find(name)

    if not record:
        raise KeyError

    return record.add_birthday(bday)


@input_error
def show_birthday(args, book):
    (name,) = args
    record = book.find(name)

    if not record:
        raise KeyError

    if record.birthday:
        return (
            f"Birthday for {name}: "
            f"{record.birthday}"
        )

    return f"No birthday set for {name}."


@input_error
def upcoming_birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No birthdays in the next 7 days."

    lines = [
        f"- {u['name']} → {u['congratulation_date']}"
        for u in upcoming
    ]

    return "\n".join(lines)


@input_error
def delete_contact(args, book):
    (name,) = args
    return book.delete(name)


@input_error
def search_contacts(args, book):
    (keyword,) = args
    results = []

    for record in book.data.values():
        if keyword.lower() in record.name.value.lower():
            results.append(str(record))
        elif any(
            keyword in phone.value
            for phone in record.phones
        ):
            results.append(str(record))

    if not results:
        return "No matching contacts found."

    return "\n".join(results)


# Autocompletion
class HintsCompleter(Completer):
    def __init__(self, commands):
        self.commands = commands

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lower().strip()

        for cmd in self.commands:
            if cmd.startswith(text):
                yield Completion(
                    cmd, start_position=-len(text)
                )


# Guessing similar commands
def guess_command(user_command, known_commands):
    matches = get_close_matches(
        user_command, known_commands, n=1, cutoff=0.6
    )
    return matches[0] if matches else None


# Main loop
def main():
    book = load_data()

    print("=" * 50)
    print(
        "Hello! This is your personal contacts assistant."
    )
    print(
        "Enter a command or use "
        "autocomplete."
    )
    print("=" * 50)

    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": upcoming_birthdays,
        "delete": delete_contact,
        "search": search_contacts,
    }

    system_commands = ["hello", "close", "exit"]
    all_commands = list(commands.keys()) + system_commands

    completer = HintsCompleter(all_commands)

    while True:
        try:
            user_input = prompt(
                "Enter a command: ",
                completer=completer
            )
        except (KeyboardInterrupt, EOFError):
            save_data(book)
            print("Work completed. Data saved.")
            break

        command, args = parse_input(user_input)

        if not command:
            continue

        if command in ["close", "exit"]:
            save_data(book)
            print("=" * 50)
            print(
                "Work completed. Data saved."
            )
            print("Bye!")
            print("=" * 50)
            break

        if command == "hello":
            print("How can I help you?")
            continue

        if command in commands:
            if command in ["all", "birthdays"]:
                print(commands[command](book))
            else:
                print(commands[command](args, book))
            continue

        guessed = guess_command(command, all_commands)

        if guessed:
            print(f"Maybe you meant '{guessed}'?")

            if guessed in ["all", "birthdays"]:
                print(commands[guessed](book))
            elif guessed in commands:
                print(commands[guessed](args, book))
            elif guessed == "hello":
                print("How can I help you?")
            elif guessed in ["close", "exit"]:
                save_data(book)
                print("=" * 50)
                print(
                    "Work completed. Data saved."
                )
                print("See you later!")
                print("=" * 50)
                break
        else:
            print("Unknown command. Try again.")


if __name__ == "__main__":
    main()
