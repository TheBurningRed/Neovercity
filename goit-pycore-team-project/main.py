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


class NoteNotFoundError(ContactError):
    pass


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid format. Check that the arguments are entered correctly."
        except IndexError:
            return (
                "Insufficient arguments. Enter a command, name, and optionally a value."
            )
        except KeyError:
            return "Contact not found."
        except PhoneValidationError as e:
            return str(e)
        except DateValidationError as e:
            return str(e)
        except RecordNotFoundError as e:
            return str(e)
        except NoteNotFoundError as e:
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


def normalize_tags(tags: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for raw in tags:
        if not raw:
            continue
        cleaned = raw.strip().lower()
        if cleaned.startswith("tags:"):
            cleaned = cleaned[5:].strip()
        parts = re.split(r"[,\s]+", cleaned)
        for part in parts:
            if not part:
                continue
            part = part.lstrip("#")
            part = re.sub(r"[^\w\-]+", "", part, flags=re.UNICODE)
            if not part:
                continue
            if part not in seen:
                seen.add(part)
                normalized.append(part)
    return normalized


def split_tags_string(raw: str) -> list[str]:
    interim = raw.replace(",", " ")
    parts = [p for p in interim.split() if p]
    return normalize_tags(parts)


def ensure_note_has_tags(note):
    if not hasattr(note, "tags"):
        note.tags = []


def normalize_note_text(raw: str) -> str:
    t = raw.strip()
    while len(t) >= 2 and t[0] == t[-1] and t[0] in ("'", '"'):
        t = t[1:-1].strip()
    return t


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
            raise PhoneValidationError(
                "The phone number must consist of exactly 10 digits."
            )
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


class Note:
    def __init__(self, note_id: int, text: str, tags: list[str] | None = None):
        self.id = note_id
        self.text = text
        self.tags: list[str] = normalize_tags(tags or [])
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def update_text(self, new_text: str):
        self.text = new_text
        self.updated_at = datetime.now()

    def add_tags(self, tags: list[str]):
        ensure_note_has_tags(self)
        to_add = normalize_tags(tags)
        existing = set(self.tags)
        for t in to_add:
            if t not in existing:
                self.tags.append(t)
                existing.add(t)
        self.updated_at = datetime.now()

    def remove_tags(self, tags: list[str]):
        ensure_note_has_tags(self)
        to_remove = set(normalize_tags(tags))
        if not self.tags:
            return
        self.tags = [t for t in self.tags if t not in to_remove]
        self.updated_at = datetime.now()

    def clear_tags(self):
        ensure_note_has_tags(self)
        self.tags = []
        self.updated_at = datetime.now()

    def __str__(self):
        ensure_note_has_tags(self)
        tags_str = f" [#{', #'.join(self.tags)}]" if self.tags else ""
        return f"[{self.id}] {self.text}{tags_str}"


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.notes: list[Note] = []
        self.next_note_id = 1

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
            return (
                f"Error: Number {phone_number} not found for contact {self.name.value}."
            )

    def add_note(self, text: str, tags: list[str] | None = None):
        text = normalize_note_text(text)
        if not text:
            return "Note text cannot be empty."
        note = Note(self.next_note_id, text, tags or [])
        self.notes.append(note)
        self.next_note_id += 1
        if note.tags:
            return f"Note [{note.id}] added for contact {self.name.value} with tags: {', '.join('#' + t for t in note.tags)}."
        return f"Note [{note.id}] added for contact {self.name.value}."

    def list_notes(self) -> list[Note]:
        return list(self.notes)

    def find_note(self, note_id: int) -> Note | None:
        for n in self.notes:
            if n.id == note_id:
                return n
        return None

    def search_notes(self, query: str) -> list[Note]:
        q = query.strip().lower()
        if not q:
            return []
        return [n for n in self.notes if q in n.text.lower()]

    def search_notes_by_tags(
        self, tags: list[str], match_all: bool = True
    ) -> list[tuple[Note, int]]:
        query_tags = set(normalize_tags(tags))
        if not query_tags:
            return []
        results: list[tuple[Note, int]] = []
        for n in self.notes:
            ensure_note_has_tags(n)
            note_tags = set(n.tags)
            match_count = len(query_tags & note_tags)
            if (match_all and query_tags.issubset(note_tags)) or (
                not match_all and match_count > 0
            ):
                results.append((n, match_count))

        results.sort(
            key=lambda item: (-item[1], -item[0].updated_at.timestamp(), item[0].id)
        )
        return results

    def list_notes_sorted_by_tags(self) -> list[Note]:
        for n in self.notes:
            ensure_note_has_tags(n)
        return sorted(self.notes, key=lambda n: (" ".join(n.tags), n.id))

    def edit_note(self, note_id: int, new_text: str):
        note = self.find_note(note_id)
        if note is None:
            raise NoteNotFoundError(
                f"Note [{note_id}] not found for contact {self.name.value}."
            )
        new_text = normalize_note_text(new_text)
        if not new_text:
            return "Note text cannot be empty."
        note.update_text(new_text)
        return f"Note [{note_id}] updated for contact {self.name.value}."

    def delete_note(self, note_id: int):
        note = self.find_note(note_id)
        if note is None:
            raise NoteNotFoundError(
                f"Note [{note_id}] not found for contact {self.name.value}."
            )
        self.notes.remove(note)
        return f"Note [{note_id}] deleted for contact {self.name.value}."

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        notes_str = f", notes: {len(self.notes)}" if self.notes else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}{notes_str}"


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

    def search_notes_global(self, query: str):
        q = query.strip()
        if not q:
            return []
        results = []
        for record in self.data.values():
            for note in record.search_notes(q):
                results.append(
                    {"name": record.name.value, "note_id": note.id, "text": note.text}
                )
        return results

    def search_notes_by_tags_global(self, tags: list[str], match_all: bool = True):
        query_tags = normalize_tags(tags)
        if not query_tags:
            return []
        results = []
        for record in self.data.values():
            matches = record.search_notes_by_tags(query_tags, match_all=match_all)
            for note, match_count in matches:
                ensure_note_has_tags(note)
                results.append(
                    {
                        "name": record.name.value,
                        "note_id": note.id,
                        "text": note.text,
                        "tags": list(note.tags),
                        "matches": match_count,
                    }
                )

        results.sort(key=lambda x: (-x["matches"], x["name"].lower(), x["note_id"]))
        return results

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
                    days_until_monday = 7 - bday_this_year.weekday()
                    bday_this_year += timedelta(days=days_until_monday)

                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": bday_this_year.strftime("%d.%m.%Y"),
                    }
                )

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
    (name,) = args
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
    (name,) = args
    record = book.find(name)
    if record is None:
        raise KeyError

    if record.birthday:
        return f"Birthday for {name}: {record.birthday}"
    else:
        return f"The birthday is not set for contact {name}."


@input_error
def upcoming_birthdays(book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "There are no birthdays next week."
    output = "Upcoming birthdays:\n"
    for item in upcoming:
        output += f"- {item['name']} needs to be congratulated on: {item['congratulation_date']}\n"
    return output.strip()


@input_error
def add_note_cmd(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: add-note <name> <note text> [tags: <tag1,tag2,...>]"
    name = args[0]
    if "tags:" in args:
        tags_index = args.index("tags:")
        text_tokens = args[1:tags_index]
        tag_tokens = args[tags_index + 1 :]
        text = " ".join(text_tokens).strip()
        tags = normalize_tags(tag_tokens) if tag_tokens else []
    else:
        text = " ".join(args[1:]).strip()
        tags = []
    record = book.find(name)
    if record is None:
        raise KeyError
    return record.add_note(text, tags)


@input_error
def list_notes_cmd(args, book: AddressBook):
    if len(args) < 1:
        return "Usage: list-notes <name> [--sort tags]"
    name = args[0]
    sort_by_tags = False
    if len(args) >= 3 and args[1] in ("--sort", "-s") and args[2] == "tags":
        sort_by_tags = True
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.notes:
        return f"No notes for contact {name}."
    notes = record.list_notes_sorted_by_tags() if sort_by_tags else record.list_notes()
    lines = [f"Notes for {name}:"]
    for n in notes:
        ensure_note_has_tags(n)
        tag_suffix = f" [#{', #'.join(n.tags)}]" if n.tags else ""
        lines.append(f"- [{n.id}] {n.text}{tag_suffix}")
    return "\n".join(lines)


@input_error
def search_notes_cmd(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: search-notes <name> <query>"
    name = args[0]
    query = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        raise KeyError
    found = record.search_notes(query)
    if not found:
        return f"No notes matched '{query}' for contact {name}."
    lines = [f"Found notes for {name} (query: '{query}'):"]
    for n in found:
        ensure_note_has_tags(n)
        tag_suffix = f" [#{', #'.join(n.tags)}]" if n.tags else ""
        lines.append(f"- [{n.id}] {n.text}{tag_suffix}")
    return "\n".join(lines)


@input_error
def edit_note_cmd(args, book: AddressBook):
    if len(args) < 3:
        return "Usage: edit-note <name> <note_id> <new text>"
    name = args[0]
    try:
        note_id = int(args[1])
    except ValueError:
        return "note_id must be an integer."
    new_text = " ".join(args[2:])
    record = book.find(name)
    if record is None:
        raise KeyError
    return record.edit_note(note_id, new_text)


@input_error
def delete_note_cmd(args, book: AddressBook):
    name, note_id_str = args
    try:
        note_id = int(note_id_str)
    except ValueError:
        return "note_id must be an integer."
    record = book.find(name)
    if record is None:
        raise KeyError
    return record.delete_note(note_id)


@input_error
def find_notes_cmd(args, book: AddressBook):
    if not args:
        return "Usage: find-notes <query>"
    query = " ".join(args)
    results = book.search_notes_global(query)
    if not results:
        return f"No notes matched '{query}'."
    lines = [f"Global notes search (query: '{query}'):"]
    for item in results:
        lines.append(f"- {item['name']} [{item['note_id']}]: {item['text']}")
    return "\n".join(lines)


@input_error
def add_tags_cmd(args, book: AddressBook):
    if len(args) < 3:
        return "Usage: add-tags <name> <note_id> <tag1> [tag2 ...]"
    name = args[0]
    try:
        note_id = int(args[1])
    except ValueError:
        return "note_id must be an integer."
    tags = normalize_tags(args[2:])
    if not tags:
        return "Provide at least one tag."
    record = book.find(name)
    if record is None:
        raise KeyError
    note = record.find_note(note_id)
    if note is None:
        raise NoteNotFoundError(f"Note [{note_id}] not found for contact {name}.")
    note.add_tags(tags)
    return f"Tags added to note [{note_id}] for contact {name}: {', '.join('#' + t for t in tags)}"


@input_error
def remove_tags_cmd(args, book: AddressBook):
    if len(args) < 3:
        return "Usage: remove-tags <name> <note_id> <tag1> [tag2 ...]"
    name = args[0]
    try:
        note_id = int(args[1])
    except ValueError:
        return "note_id must be an integer."
    tags = normalize_tags(args[2:])
    if not tags:
        return "Provide at least one tag."
    record = book.find(name)
    if record is None:
        raise KeyError
    note = record.find_note(note_id)
    if note is None:
        raise NoteNotFoundError(f"Note [{note_id}] not found for contact {name}.")
    note.remove_tags(tags)
    return f"Tags removed from note [{note_id}] for contact {name}: {', '.join('#' + t for t in tags)}"


@input_error
def clear_tags_cmd(args, book: AddressBook):
    name, note_id_str = args
    try:
        note_id = int(note_id_str)
    except ValueError:
        return "note_id must be an integer."
    record = book.find(name)
    if record is None:
        raise KeyError
    note = record.find_note(note_id)
    if note is None:
        raise NoteNotFoundError(f"Note [{note_id}] not found for contact {name}.")
    note.clear_tags()
    return f"All tags cleared for note [{note_id}] of contact {name}."


@input_error
def search_tags_cmd(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: search-tags <name> <tag1> [tag2 ...] [--any]"
    name = args[0]
    match_all = True
    tags_tokens = args[1:]
    if "--any" in tags_tokens:
        match_all = False
        tags_tokens = [t for t in tags_tokens if t != "--any"]
    tags = normalize_tags(tags_tokens)
    if not tags:
        return "Provide at least one tag."
    record = book.find(name)
    if record is None:
        raise KeyError
    found = record.search_notes_by_tags(tags, match_all=match_all)
    if not found:
        return f"No notes matched tags for contact {name}."
    criterion = "all" if match_all else "any"
    lines = [
        f"Notes for {name} matching {criterion} of tags: {', '.join('#' + t for t in tags)}"
    ]
    for note, match_count in found:
        ensure_note_has_tags(note)
        tag_suffix = f" [#{', #'.join(note.tags)}]" if note.tags else ""
        lines.append(f"- [{note.id}] {note.text}{tag_suffix} (matches: {match_count})")
    return "\n".join(lines)


@input_error
def find_tags_cmd(args, book: AddressBook):
    if not args:
        return "Usage: find-tags <tag1> [tag2 ...] [--any]"
    match_all = True
    tags_tokens = list(args)
    if "--any" in tags_tokens:
        match_all = False
        tags_tokens = [t for t in tags_tokens if t != "--any"]
    tags = normalize_tags(tags_tokens)
    if not tags:
        return "Provide at least one tag."
    results = book.search_notes_by_tags_global(tags, match_all=match_all)
    if not results:
        return "No notes matched the given tags."
    criterion = "all" if match_all else "any"
    lines = [
        f"Global notes search by {criterion} tags: {', '.join('#' + t for t in tags)}"
    ]
    for item in results:
        tag_suffix = f" [#{', #'.join(item['tags'])}]" if item.get("tags") else ""
        lines.append(
            f"- {item['name']} [{item['note_id']}]: {item['text']}{tag_suffix} (matches: {item['matches']})"
        )
    return "\n".join(lines)


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
        "add-note": add_note_cmd,
        "list-notes": list_notes_cmd,
        "search-notes": search_notes_cmd,
        "edit-note": edit_note_cmd,
        "delete-note": delete_note_cmd,
        "find-notes": find_notes_cmd,
        "add-tags": add_tags_cmd,
        "remove-tags": remove_tags_cmd,
        "clear-tags": clear_tags_cmd,
        "search-tags": search_tags_cmd,
        "find-tags": find_tags_cmd,
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
                "Invalid command. Available commands:\n"
                "hello - greeting\n"
                "add <name> <phone> - add contact or phone\n"
                "change <name> <old_phone> <new_phone> - change phone\n"
                "phone <name> - show phones\n"
                "all - show all contacts\n"
                "add-birthday <name> <DD.MM.YYYY> - add birthday\n"
                "show-birthday <name> - show birthday\n"
                "birthdays - show upcoming birthdays\n"
                "add-note <name> <text> [tags: <t1,t2,...>] - add note\n"
                "list-notes <name> [--sort tags] - list contact notes\n"
                "search-notes <name> <query> - search contact notes\n"
                "edit-note <name> <note_id> <new text> - edit note\n"
                "delete-note <name> <note_id> - delete note\n"
                "find-notes <query> - global notes search\n"
                "add-tags <name> <note_id> <tag1> [tag2 ...] - add tags to note\n"
                "remove-tags <name> <note_id> <tag1> [tag2 ...] - remove tags from note\n"
                "clear-tags <name> <note_id> - clear note tags\n"
                "search-tags <name> <tag1> [tag2 ...] [--any] - search notes by tags\n"
                "find-tags <tag1> [tag2 ...] [--any] - global search by tags\n"
                "close | exit - save and quit"
            )


if __name__ == "__main__":
    main()
