import random

def simulate_dice_rolls(num_rolls=100000):
    # Словник для зберігання кількості випадінь кожної суми (від 2 до 12)
    counts = {i: 0 for i in range(2, 13)}

    # Симуляція кидків
    for _ in range(num_rolls):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2
        counts[total] += 1

    # Обчислення ймовірностей
    probabilities = {sum_val: (count / num_rolls) * 100 for sum_val, count in counts.items()}

    return counts, probabilities

def print_results(num_rolls, counts, probabilities):
    print(f"Результати симуляції {num_rolls} кидків:")
    print(f"{'Сума':<10} | {'Кількість':<15} | {'Ймовірність (%)':<15}")
    print("-" * 45)
    for sum_val in range(2, 13):
        print(f"{sum_val:<10} | {counts[sum_val]:<15} | {probabilities[sum_val]:.2f}%")

if __name__ == "__main__":
    trials = 100000  # Кількість ітерацій
    results_counts, results_probs = simulate_dice_rolls(trials)
    print_results(trials, results_counts, results_probs)

    # Опціонально: Побудова графіка (потребує matplotlib)
    try:
        import matplotlib.pyplot as plt

        sums = list(results_probs.keys())
        probs = list(results_probs.values())

        plt.figure(figsize=(10, 6))
        plt.bar(sums, probs, color='skyblue', edgecolor='black')
        plt.xlabel('Сума чисел на кубиках')
        plt.ylabel('Ймовірність (%)')
        plt.title(f'Ймовірності сум при киданні двох кубиків ({trials} симуляцій)')
        plt.xticks(range(2, 13))
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()
    except ImportError:
        print("\nПорада: Встановіть matplotlib (`pip install matplotlib`), щоб побачити графік.")
