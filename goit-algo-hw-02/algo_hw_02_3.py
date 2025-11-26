
def is_symmetric(s: str) -> bool:
    stack = []
    brackets_map = {
        '(': ')',
        '[': ']',
        '{': '}'
    }

    opening_brackets = set(brackets_map.keys())
    closing_brackets = set(brackets_map.values())

    for char in s:
        # Пропускаємо символи, які не є дужками
        if char not in opening_brackets and char not in closing_brackets:
            continue

        # Якщо це відкриваюча дужка, додаємо її в стек
        if char in opening_brackets:
            stack.append(char)

        # Якщо це закриваюча дужка
        elif char in closing_brackets:
            # Перевіряємо, чи стек не порожній
            if not stack:
                return False

            # Беремо останню відкриваючу дужку зі стеку
            last_opening = stack.pop()

            # Перевіряємо, чи відповідає закриваюча дужка відкриваючій
            if brackets_map[last_opening] != char:
                return False

    # Якщо стек порожній, усі дужки збалансовані
    return len(stack) == 0


def main():
    print("Програма для перевірки симетричності дужок")
    print("Підтримувані дужки: ( ), [ ], { }")
    print("Для виходу введіть 'exit'")
    print("-" * 50)

    while True:
        try:
            user_input = input("Введіть послідовність символів: ").strip()

            if user_input.lower() == 'exit':
                print("До побачення!")
                break

            result = is_symmetric(user_input)
            result_text = "Симетричні" if result else "Несиметричні"
            print(f"Результат: {result_text} ({result})")
            print("-" * 30)

        except KeyboardInterrupt:
            print("\nПрограма завершена користувачем.")
            break
        except Exception as e:
            print(f"Помилка: {e}")


def test_examples():
    test_cases = [
        ("( ){ }[ ]", True),
        ("( ){ }[ ]( )( ){ }", True),
        ("( ( ( )", False),
        ("( }", False),
        ("", True),
        ("abc", True),
        ("(a+b)*[c-d]", True),
        ("([{}])", True),
        ("([{})]", False),
        ("((()))", True),
        ("((())", False),
        ("()[]{}}", False),
    ]

    print("Тестування програми:")
    print("=" * 50)

    for test_input, expected in test_cases:
        result = is_symmetric(test_input)
        status = "✅" if result == expected else "❌"
        result_text = "Симетричні" if result else "Несиметричні"
        expected_text = "Симетричні" if expected else "Несиметричні"
        print(f"{status} Вхід: '{test_input}' -> {result_text} ({result}) | Очікувано: {expected_text} ({expected})")


if __name__ == "__main__":
    test_examples()
    print("\n" + "=" * 50)

    main()
