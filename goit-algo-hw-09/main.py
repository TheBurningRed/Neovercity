def find_coins_greedy(amount, coins=[50, 25, 10, 5, 2, 1]):
    """
    Жадібний алгоритм для видачі решти.
    Вибирає найбільші доступні номінали спочатку.
    """
    result = {}
    for coin in coins:
        if amount >= coin:
            count = amount // coin
            result[coin] = count
            amount %= coin
    return result

def find_min_coins(amount, coins=[50, 25, 10, 5, 2, 1]):
    """
    Алгоритм динамічного програмування для пошуку мінімальної кількості монет.
    """
    # min_coins_count[i] зберігає мінімальну кількість монет для суми i
    min_coins_count = [0] + [float('inf')] * amount
    # last_coin_used[i] зберігає останню монету, використану для суми i
    last_coin_used = [0] * (amount + 1)

    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin and min_coins_count[i - coin] + 1 < min_coins_count[i]:
                min_coins_count[i] = min_coins_count[i - coin] + 1
                last_coin_used[i] = coin

    # Відновлюємо набір монет зі списку використаних номіналів
    result = {}
    current_amount = amount
    while current_amount > 0:
        coin = last_coin_used[current_amount]
        result[coin] = result.get(coin, 0) + 1
        current_amount -= coin

    return result

if __name__ == "__main__":
    test_amount = 113
    print(f"Сума: {test_amount}")
    print(f"Жадібний: {find_coins_greedy(test_amount)}")
    print(f"Динамічний: {find_min_coins(test_amount)}")
