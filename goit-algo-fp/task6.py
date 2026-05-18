items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}

def greedy_algorithm(items, budget):
    # Сортуємо страви за спаданням співвідношення калорій до вартості
    sorted_items = sorted(items.items(),
                          key=lambda x: x[1]['calories'] / x[1]['cost'],
                          reverse=True)

    selected_items = []
    total_calories = 0
    remaining_budget = budget

    for name, info in sorted_items:
        if info['cost'] <= remaining_budget:
            selected_items.append(name)
            total_calories += info['calories']
            remaining_budget -= info['cost']

    return selected_items, total_calories

def dynamic_programming(items, budget):
    # Створюємо список назв та їх параметрів для зручності індексації
    item_names = list(items.keys())
    costs = [items[name]['cost'] for name in item_names]
    calories = [items[name]['calories'] for name in item_names]
    n = len(item_names)

    # Таблиця для зберігання максимальних калорій для кожного бюджету
    # dp[i][j] - макс. калорії для перших i предметів при бюджеті j
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(budget + 1):
            if costs[i-1] <= j:
                # Вибираємо максимум між: не брати страву або взяти її
                dp[i][j] = max(dp[i-1][j], dp[i-1][j - costs[i-1]] + calories[i-1])
            else:
                dp[i][j] = dp[i-1][j]

    # Відновлення списку обраних страв
    selected_items = []
    total_calories = dp[n][budget]
    w = budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(item_names[i-1])
            w -= costs[i-1]

    return selected_items, total_calories

# Тестування
budget = 100

print(f"Бюджет: {budget}")
greedy_res, greedy_cal = greedy_algorithm(items, budget)
print(f"Жадібний алгоритм: {greedy_res}, Сумарна калорійність: {greedy_cal}")

dp_res, dp_cal = dynamic_programming(items, budget)
print(f"Динамічне програмування: {dp_res}, Сумарна калорійність: {dp_cal}")
