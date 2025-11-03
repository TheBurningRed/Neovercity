import re

raw_numbers = [
    "067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

MINIMUM_VALID_STR_LENGTH = 9

def normalize_phone(phone_like_string: str) -> str:
    if type(phone_like_string) is not str or len(phone_like_string) < MINIMUM_VALID_STR_LENGTH:
        raise ValueError("Invalid input. Most likely it is not a phone number")
    
    only_numeric_chars = re.findall(r"\d", phone_like_string)
    only_last_9 = only_numeric_chars[-9:]
    formated = f"+380{''.join(only_last_9)}"
    return formated

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)




