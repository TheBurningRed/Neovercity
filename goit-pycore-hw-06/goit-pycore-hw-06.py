from collections import UserDict
import re
from typing import Optional, List


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        if not value or not str(value).strip():
            raise ValueError("Ім'я не може бути порожнім")
        super().__init__(value.strip())


class Phone(Field):
    _PATTERN = re.compile(r"^\d{10}$")

    def __init__(self, value: str):
        value = str(value).strip()
        if not self._PATTERN.fullmatch(value):
            raise ValueError("Номер телефону має містити рівно 10 цифр")
        super().__init__(value)

    def set(self, value: str):
        """Дозволяє перевстановити коректно валідований номер."""
        value = str(value).strip()
        if not self._PATTERN.fullmatch(value):
            raise ValueError("Номер телефону має містити рівно 10 цифр")
        self.value = value


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []

    def add_phone(self, phone: str) -> None:
        """Додає телефон, ігнорує дублікати за значенням."""
        p = Phone(phone)
        if not any(existing.value == p.value for existing in self.phones):
            self.phones.append(p)

    def find_phone(self, phone: str) -> Optional[Phone]:
        """Повертає Phone або None."""
        phone = str(phone).strip()
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone: str) -> bool:
        """Видаляє телефон за значенням. Повертає True, якщо видалено."""
        target = self.find_phone(phone)
        if target:
            self.phones.remove(target)
            return True
        return False

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Замінює існуючий номер на новий (валідований)."""
        target = self.find_phone(old_phone)
        if not target:
            raise ValueError("Старий номер не знайдено")
        # Перевірка нового номера
        new_p = Phone(new_phone)
        # Якщо новий вже існує як дублікат — просто оновимо поточний
        target.set(new_p.value)

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        """Додає або замінює запис за ім'ям."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Пошук запису за іменем."""
        return self.data.get(str(name).strip())

    def delete(self, name: str) -> bool:
        """Видаляє запис за іменем. Повертає True, якщо видалено."""
        key = str(name).strip()
        if key in self.data:
            del self.data[key]
            return True
        return False


# ===================== Приклад використання =====================

book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Очікувано: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону в записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Очікувано: 5555555555

# Видалення запису Jane
book.delete("Jane")