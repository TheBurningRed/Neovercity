from __future__ import annotations
from collections import UserDict, defaultdict
from datetime import datetime, date, timedelta
import re
from input_error_decorator import input_error


@input_error
def add_birthday(args, book):
    # add-birthday <name> <DD.MM.YYYY>
    name, birthday_str = args  # якщо аргументів мало/багато — кине ValueError, обробить декоратор

    # Шукаємо існуючий контакт. Якщо його немає — KeyError, обробить декоратор
    record = book[name]

    # Парсимо дату
    birthday_date = datetime.strptime(birthday_str, "%d.%m.%Y").date()

    # Зберігаємо день народження в записі
    record.birthday = birthday_date

    return f"День народження для контакту {name} додано ({birthday_date.strftime('%d.%m.%Y')})."


@input_error
def show_birthday(args, book):
    # show-birthday <name>
    name, = args  # знову ж, нехай декоратор ловить помилки аргументів

    record = book[name]  # KeyError, якщо контакту немає — обробить декоратор

    birthday = getattr(record, "birthday", None)
    if not birthday:
        return f"Для контакту {name} день народження не вказаний."

    if isinstance(birthday, str):
        # якщо раптом зберігаєте як рядок
        try:
            birthday_date = datetime.strptime(birthday, "%d.%m.%Y").date()
        except ValueError:
            # якщо формат якийсь інший — показуємо як є
            return f"День народження контакту {name}: {birthday}"
    elif isinstance(birthday, (date, datetime)):
        birthday_date = birthday if isinstance(birthday, date) else birthday.date()
    else:
        # невідомий тип — просто str()
        return f"День народження контакту {name}: {birthday}"

    return f"День народження контакту {name}: {birthday_date.strftime('%d.%m.%Y')}"


def _collect_birthdays_for_next_week(book, days_ahead: int = 7) -> dict:
    """Сервісна функція: повертає dict[weekday_name] = [names,...] для наступних days_ahead днів.
       Вихідні (субота/неділя) переносяться на понеділок.
    """
    today = date.today()
    result = defaultdict(list)

    for record in book.values():
        birthday = getattr(record, "birthday", None)
        if not birthday:
            continue

        # Нормалізуємо до date
        if isinstance(birthday, str):
            try:
                bd = datetime.strptime(birthday, "%d.%m.%Y").date()
            except ValueError:
                # Якщо формат кривий — пропускаємо
                continue
        elif isinstance(birthday, (date, datetime)):
            bd = birthday if isinstance(birthday, date) else birthday.date()
        else:
            continue

        # День народження в поточному році
        birthday_this_year = bd.replace(year=today.year)

        # Якщо вже був цього року — переносимо на наступний
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        delta = (birthday_this_year - today).days

        # Цікавлять тільки наступні days_ahead днів (0 включно)
        if 0 <= delta < days_ahead:
            weekday_index = birthday_this_year.weekday()  # 0=Mon, 6=Sun

            # Якщо вихідний (5=субота, 6=неділя) — переносимо на понеділок
            if weekday_index >= 5:
                weekday_name = "Monday"
            else:
                weekday_name = birthday_this_year.strftime("%A")

            # Ім'я контакту з Record: або record.name.value, або просто record.name/ключ
            if hasattr(record, "name") and hasattr(record.name, "value"):
                contact_name = record.name.value
            elif hasattr(record, "name"):
                contact_name = str(record.name)
            else:
                # fallback, якщо book — простий dict {name: record}
                # і ми зараз перебираємо тільки значення
                # тоді краще зберігати name в самому Record
                contact_name = getattr(record, "contact_name", "<unknown>")

            result[weekday_name].append(contact_name)

    return result


@input_error
def birthdays(args, book):
    # birthdays
    # Аргументи ігноруємо, але якщо хтось передасть зайве — нехай декоратор це розрулить при потребі
    upcoming = _collect_birthdays_for_next_week(book, days_ahead=7)

    if not upcoming:
        return "Немає днів народження на наступному тижні."

    # Виводимо у фіксованому порядку робочих днів
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    lines = []

    for day in ordered_days:
        if day in upcoming:
            names = ", ".join(upcoming[day])
            lines.append(f"{day}: {names}")

    return "\n".join(lines)

# ===== Базові поля =====
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Ім'я не може бути порожнім")
        super().__init__(value.strip())


class Phone(Field):
    """
    Валідний телефон: рівно 10 цифр (без +38, пробілів, тире тощо).
    """
    _re = re.compile(r"^\d{10}$")

    def __init__(self, value: str):
        value = str(value).strip()
        if not Phone._re.fullmatch(value):
            raise ValueError("Невірний формат телефону. Використовуйте 10 цифр, напр.: 0501234567")
        super().__init__(value)


class Birthday(Field):
    """
    Зберігає дату народження як datetime.date.
    Формат введення: DD.MM.YYYY
    """
    def __init__(self, value: str):
        try:
            dt = datetime.strptime(value.strip(), "%d.%m.%Y").date()
            # Не обов'язково, але логічно заборонити дати з майбутнього
            if dt > date.today():
                raise ValueError("Дата народження не може бути в майбутньому")
            super().__init__(dt)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


# ===== Запис контакту =====
class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    # --- Робота з телефонами ---
    def add_phone(self, phone: str) -> Phone:
        ph = Phone(phone)
        self.phones.append(ph)
        return ph

    def find_phone(self, phone: str) -> Phone | None:
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None

    def edit_phone(self, old: str, new: str) -> None:
        ph = self.find_phone(old)
        if not ph:
            raise ValueError("Телефон не знайдено")
        ph_new = Phone(new)
        ph.value = ph_new.value

    def remove_phone(self, phone: str) -> None:
        ph = self.find_phone(phone)
        if not ph:
            raise ValueError("Телефон не знайдено")
        self.phones.remove(ph)

    # --- День народження ---
    def add_birthday(self, birthday_str: str) -> Birthday:
        if self.birthday is not None:
            raise ValueError("День народження вже задано для цього контакту")
        bd = Birthday(birthday_str)
        self.birthday = bd
        return bd

    def __str__(self) -> str:
        phones = ", ".join(p.value for p in self.phones) if self.phones else "—"
        bd = str(self.birthday) if self.birthday else "—"
        return f"{self.name.value}: phones=[{phones}], birthday={bd}"


# ===== Адресна книга =====
class AddressBook(UserDict):
    """
    Ключ — ім'я контакту (Name.value), значення — Record.
    """
    def add_record(self, record: Record) -> None:
        key = record.name.value
        if key in self.data:
            raise ValueError("Контакт з таким ім'ям вже існує")
        self.data[key] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name not in self.data:
            raise ValueError("Контакт не знайдено")
        del self.data[name]

    # --- Привітання на наступному тижні ---
    def get_upcoming_birthdays(self, *, days: int = 7, today: date | None = None) -> list[dict]:
        """
        Повертає список словників:
        [{ 'name': <ім'я>, 'congratulation_date': 'YYYY-MM-DD' }, ...]
        лише для контактів, чиї ДН випадають у найближчі `days` днів.
        Якщо ДН припадає на суботу/неділю — переносимо привітання на понеділок.
        """
        if today is None:
            today = date.today()

        end_day = today + timedelta(days=days)
        results: list[tuple[date, str]] = []

        for rec in self.data.values():
            if not rec.birthday:
                continue

            bd: date = rec.birthday.value
            # День народження в поточному році
            next_bd = bd.replace(year=today.year)
            if next_bd < today:
                next_bd = bd.replace(year=today.year + 1)

            # Тільки якщо у вікні [today, end_day]
            if today <= next_bd <= end_day:
                congr_date = next_bd
                # Переносимо на понеділок, якщо вихідні
                if congr_date.weekday() == 5:      # Saturday
                    congr_date += timedelta(days=2)
                elif congr_date.weekday() == 6:    # Sunday
                    congr_date += timedelta(days=1)

                results.append((congr_date, rec.name.value))

        # Сортуємо за датою, формуємо вихід
        results.sort(key=lambda x: (x[0], x[1]))
        return [
            {"name": name, "congratulation_date": d.isoformat()}
            for d, name in results
        ]


# ===== Приклад використання =====
if __name__ == "__main__":
    ab = AddressBook()

    john = Record("John Doe")
    john.add_phone("0501234567")
    john.add_birthday("15.11.1990")

    jane = Record("Jane Smith")
    jane.add_phone("0670000000")
    jane.add_birthday("16.11.1992")

    ab.add_record(john)
    ab.add_record(jane)

    print(ab.get_upcoming_birthdays(days=7))