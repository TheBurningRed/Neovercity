from collections import deque

def is_palindrome(text: str) -> bool:
    normalized_text = text.lower().replace(' ', '')
    char_deque = deque(normalized_text)

    while len(char_deque) > 1:
        left_char = char_deque.popleft()
        right_char = char_deque.pop()

        if left_char != right_char:
            return False

    return True

# Тестування функції
if __name__ == "__main__":
    test_cases = [
        "racecar",           # Паліндром з непарною кількістю символів
        "race a car",        # Паліндром з пробілами
        "A man a plan a canal Panama",  # Довгий паліндром з пробілами
        "race Car",          # Паліндром з різним регістром
        "hello",             # Не паліндром
        "Madam",             # Паліндром з різним регістром
        "No x in Nixon",     # Не паліндром
        "Mr Owl ate my metal worm",  # Паліндром з пробілами
        "abba",              # Паліндром з парною кількістю символів
        "abcd"               # Не паліндром
    ]
    
    print("Тестування функції is_palindrome:")
    print("-" * 40)
    
    for test in test_cases:
        result = is_palindrome(test)
        print(f"'{test}' -> {result}")
