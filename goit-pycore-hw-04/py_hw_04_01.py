def total_salary(path: str) -> tuple[int, float]:
    total = 0
    count = 0

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                _, salary = line.split(',')
                total += int(salary)
                count += 1
            except ValueError:
                # Пропускаємо рядки з неправильним форматом
                continue

    avg = total / count if count else 0
    return total, avg

# Приклад використання:
total, average = total_salary("py_hw_04_01.txt")
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")
