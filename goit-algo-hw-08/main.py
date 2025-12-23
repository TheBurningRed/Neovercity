import heapq

def minimize_connection_costs(cables):
    if not cables:
        return 0
    if len(cables) == 1:
        return 0

    # Перетворюємо список у структуру даних Heap (мінімальна купа)
    heapq.heapify(cables)

    total_cost = 0

    # Поки в купі більше одного кабелю
    while len(cables) > 1:
        # Беремо два найкоротші кабелі
        first = heapq.heappop(cables)
        second = heapq.heappop(cables)

        # Витрати на їхнє з'єднання
        current_cost = first + second
        total_cost += current_cost

        # Додаємо з'єднаний кабель назад у купу
        heapq.heappush(cables, current_cost)

    return total_cost

# Приклад використання:
cables_lengths = [12, 4, 8, 21]
result = minimize_connection_costs(cables_lengths)
print(f"Мінімальні витрати на з'єднання: {result}")
