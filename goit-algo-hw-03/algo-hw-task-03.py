def hanoi(n, from_rod, aux_rod, to_rod):
    """
    Переміщує n дисків зі стрижня from_rod на стрижень to_rod,
    використовуючи aux_rod як допоміжний.
    """
    if n == 0:
        return

    # 1. Перемістити n-1 дисків з from_rod на aux_rod, використовуючи to_rod
    hanoi(n - 1, from_rod, to_rod, aux_rod)

    # 2. Перемістити найбільший диск з from_rod на to_rod
    print(f"Перемістити диск {n} зі стрижня {from_rod} на стрижень {to_rod}")

    # 3. Перемістити n-1 дисків з aux_rod на to_rod, використовуючи from_rod
    hanoi(n - 1, aux_rod, from_rod, to_rod)


if __name__ == "__main__":
    n = int(input("Введіть кількість дисків: "))
    hanoi(n, "A", "B", "C")
