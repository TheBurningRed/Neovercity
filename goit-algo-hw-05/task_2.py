def binary_search_upper_bound(arr: list[float], target: float) -> tuple[int, float | None]:
    iterations = 0
    left = 0
    right = len(arr)
    upper_bound = None

    while left < right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid

    return (iterations, upper_bound)


# Тестування функції
if __name__ == "__main__":
    # Тест 1: Пошук елемента, який існує
    arr1 = [1.5, 2.3, 3.7, 4.2, 5.1]
    result1 = binary_search_upper_bound(arr1, 3.7)
    print(f"Пошук 3.7 в {arr1}")
    print(f"Результат: {result1}")
    print(f"Ітерацій: {result1[0]}, Верхня межа: {result1[1]}\n")

    # Тест 2: Пошук елемента між двома значеннями
    result2 = binary_search_upper_bound(arr1, 3.0)
    print(f"Пошук 3.0 в {arr1}")
    print(f"Результат: {result2}")
    print(f"Ітерацій: {result2[0]}, Верхня межа: {result2[1]}\n")

    # Тест 3: Пошук елемента більшого за всі в масиві
    result3 = binary_search_upper_bound(arr1, 5.5)
    print(f"Пошук 5.5 в {arr1}")
    print(f"Результат: {result3}")
    print(f"Ітерацій: {result3[0]}, Верхня межа: {result3[1]}\n")

    # Тест 4: Пошук елемента меншого за всі в масиві
    result4 = binary_search_upper_bound(arr1, 0.5)
    print(f"Пошук 0.5 в {arr1}")
    print(f"Результат: {result4}")
    print(f"Ітерацій: {result4[0]}, Верхня межа: {result4[1]}\n")

    # Тест 5: Більший масив
    arr2 = [0.1, 1.2, 2.5, 3.8, 4.9, 5.6, 6.3, 7.1, 8.4, 9.2]
    result5 = binary_search_upper_bound(arr2, 5.0)
    print(f"Пошук 5.0 в {arr2}")
    print(f"Результат: {result5}")
    print(f"Ітерацій: {result5[0]}, Верхня межа: {result5[1]}")
