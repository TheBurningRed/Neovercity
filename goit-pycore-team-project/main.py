import pickle
import re
from collections import UserDict
from datetime import datetime, timedelta
from difflib import get_close_matches

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion


class ContactError(Exception):
    pass


class PhoneValidationError(ContactError):
    pass


class DateValidationError(ContactError):
    pass


class RecordNotFoundError(ContactError):
    pass


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            return "Invalid input. Check your command and arguments."
        except KeyError:
            return "Contact not found."
        except (
            PhoneValidationError, DateValidationError, RecordNotFoundError
        ) as e:
            return str(e)
        except Exception as e:
            return f"Unexpected error: {e}"

    return wrapper


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
            self._value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise DateValidationError(
                "Invalid date format. Use DD.MM.YYYY"
            )

    def __str__(self):
        return self._value.strftime("%d.%m.%Y")


class Address(Field):
    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, new_value):
        if not new_value.strip():
            raise ValueError("Address cannot be empty.")
        self._value = new_value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.addresses = []
        self.birthday = None

    # --- Телефони ---
    def add_phone(self, phone):
        phone_obj = Phone(phone)
        if phone_obj.value not in [p.value for p in self.phones]:
            self.phones.append(phone_obj)
            return f"Phone {phone} added to {self.name.value}."
        return f"Phone {phone} already exists for {self.name.value}."

    def edit_phone(self, old, new):
        phone_obj = next((p for p in self.phones if p.value == old), None)
        if not phone_obj:
            return f"Phone {old} not found for {self.name.value}."
        phone_obj.value = new
        return f"Phone {old} updated to {new}."

    def remove_phone(self, phone):
        phone_obj = next((p for p in self.phones if p.value == phone), None)
        if phone_obj:
            self.phones.remove(phone_obj)
            return f"Phone {phone} removed from {self.name.value}."
        return f"Phone {phone} not found for {self.name.value}."

    # --- Адреси ---
    def add_address(self, addr):
        addr_obj = Address(addr)
        if addr_obj.value not in [a.value for a in self.addresses]:
            self.addresses.append(addr_obj)
            return f"Address '{addr}' added to {self.name.value}."
        return f"Address '{addr}' already exists for {self.name.value}."

    def edit_address(self, old, new):
        addr_obj = next((a for a in self.addresses if a.value == old), None)
        if not addr_obj:
            return f"Address '{old}' not found for {self.name.value}."
        addr_obj.value = new
        return f"Address '{old}' updated to '{new}'."

    def remove_address(self, addr):
        addr_obj = next((a for a in self.addresses if a.value == addr), None)
        if addr_obj:
            self.addresses.remove(addr_obj)
            return f"Address '{addr}' removed from {self.name.value}."
        return f"Address '{addr}' not found for {self.name.value}."

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return f"Birthday {birthday} added to {self.name.value}."

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) or "No phones"
        addresses = "; ".join(a.value for a in self.addresses) or "No address"
        bday = f", birthday: {self.birthday}" if self.birthday else ""
        return (
            f"Contact: {self.name.value}, Phones: {phones}, "
            f"Addresses: {addresses}{bday}"
        )


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
        raise RecordNotFoundError(f"No record found for {name}.")

    def get_upcoming_birthdays(self, days=7):
        today = datetime.now().date()
        end_date = today + timedelta(days=days)
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday_this_year = record.birthday.value.replace(year=today.year)
            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)

            if today <= bday_this_year <= end_date:
                result.append({
                    "name": record.name.value,
                    "congratulation_date": bday_this_year.strftime("%d.%m.%Y")
                })

        return result


@input_error
def search_contacts(args, book):
    (keyword,) = args
    results = []

    for record in book.data.values():
        if keyword.lower() in record.name.value.lower():
            results.append(str(record))
        elif any(keyword in p.value for p in record.phones):
            results.append(str(record))
        elif any(keyword.lower() in a.value.lower() for a in record.addresses):
            results.append(str(record))

    if not results:
        return "No matching contacts found."
    return "\n".join(results)


class HintsCompleter(Completer):
    def __init__(self, commands):
        self.commands = commands

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lower().strip()
        for cmd in self.commands:
            if cmd.startswith(text):
                yield Completion(cmd, start_position=-len(text))


def guess_command(user_command, known_commands):
    matches = get_close_matches(user_command, known_commands, n=1, cutoff=0.6)
    return matches[0] if matches else None


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
def add_address(args, book):
    name, addr = args
    record = book.find(name)
    if not record:
        raise KeyError
    return record.add_address(addr)


@input_error
def change_contact(args, book):
    name, old, new = args
    record = book.find(name)
    if not record:
        raise KeyError
    if old.isdigit():
        return record.edit_phone(old, new)
    return record.edit_address(old, new)


@input_error
def delete_contact(args, book):
    name = args[0]
    return book.delete(name)


@input_error
def show_all(book):
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def upcoming_birthdays(args, book):
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return "No birthdays in the next days."
    return "\n".join(
        f"- {u['name']} → {u['congratulation_date']}" for u in upcoming
    )


@input_error
def add_birthday(args, book):
    name, bday = args
    record = book.find(name)
    if not record:
        raise KeyError
    return record.add_birthday(bday)


@input_error
def show_phones(args, book):
    (name,) = args
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.phones:
        return f"{name} has no phones."
    return "; ".join(p.value for p in record.phones)


@input_error
def show_addresses(args, book):
    (name,) = args
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.addresses:
        return f"{name} has no addresses."
    return "; ".join(a.value for a in record.addresses)


def main():
    book = load_data()
    print("=" * 50)
    print("Hello! This is your personal contacts assistant.")
    print("Enter a command or use autocomplete.")
    print("=" * 50)

    commands = {
        "add": add_contact,
        "add-address": add_address,
        "change": change_contact,
        "delete": delete_contact,
        "all": show_all,
        "birthday": add_birthday,
        "birthdays": upcoming_birthdays,
        "phones": show_phones,
        "addresses": show_addresses,
        "search": search_contacts,
    }

    system_commands = ["hello", "exit", "close"]
    all_commands = list(commands.keys()) + system_commands
    completer = HintsCompleter(all_commands)

    while True:
        try:
            user_input = prompt("Enter a command: ", completer=completer)
        except (KeyboardInterrupt, EOFError):
            save_data(book)
            print("\nWork completed. Data saved.")
            break

        if not user_input.strip():
            continue

        command, *args = user_input.strip().split()
        command = command.lower()

        if command in ["exit", "close"]:
            save_data(book)
            print("Work completed. Data saved. Bye!")
            break
        elif command == "hello":
            print("How can I help you?")
            continue
        elif command in commands:
            if command in ["all", "birthdays"]:
                print(commands[command](args=[], book=book))
            else:
                print(commands[command](args, book))
            continue

        guessed = guess_command(command, all_commands)
        if guessed:
            print(f"Did you mean '{guessed}'?")
            if guessed in ["all", "birthdays"]:
                print(commands[guessed](args=[], book=book))
            elif guessed in commands:
                print(commands[guessed](args, book))
            elif guessed == "hello":
                print("How can I help you?")
            elif guessed in ["exit", "close"]:
                save_data(book)
                print("Work completed. Data saved. Bye!")
                break
        else:
            print("Unknown command. Try again.")


if __name__ == "__main__":
    main()
