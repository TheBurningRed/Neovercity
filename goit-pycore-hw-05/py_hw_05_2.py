import re
from typing import Callable, Iterator


_NUMBER_TOKEN = re.compile(r"(?<!\S)[+-]?\d+(?:\.\d+)?(?!\S)")


def generator_numbers(text: str) -> Iterator[float]:
    """
    Yield all valid numbers from `text` as floats.

    Assumptions:
    - Numbers are correct and delimited by whitespace on both sides.
    - Decimal separator is a dot.
    - Optional leading +/− is allowed.
    """
    for m in _NUMBER_TOKEN.finditer(text):
        yield float(m.group())


def sum_profit(text: str, func: Callable[[str], Iterator[float]]) -> float:
    """
    Sum all numbers produced by `func(text)` and return the total.
    """
    return sum(func(text))


if __name__ == "__main__":
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")