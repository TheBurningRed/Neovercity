import timeit
import os
from typing import List


def boyer_moore(text: str, pattern: str) -> List[int]:
    """
    Алгоритм Боєра-Мура для пошуку підрядка.

    Args:
        text: Текст, у якому здійснюється пошук
        pattern: Підрядок для пошуку

    Returns:
        Список позицій знайдених входжень патерну
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    # Таблиця зміщень для поганого символу
    bad_char = {}
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i

    # Таблиця добрих суфіксів
    good_suffix = [0] * len(pattern)
    compute_good_suffix(pattern, good_suffix)

    matches = []
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1

        if j < 0:
            matches.append(i)
            i += 1 if i + len(pattern) < len(text) else 1
        else:
            bad_char_shift = j - bad_char.get(text[i + j], -1)
            good_suffix_shift = good_suffix[j] if j < len(good_suffix) else 1
            i += max(bad_char_shift, good_suffix_shift)

    return matches


def compute_good_suffix(pattern: str, good_suffix: List[int]) -> None:
    """Допоміжна функція для обчислення таблиці добрих суфіксів."""
    m = len(pattern)
    s = m + 1
    f = [0] * (m + 1)

    f[m] = m + 1
    j = m + 1

    for i in range(m - 1, -1, -1):
        while j <= m and pattern[i] != pattern[j - 1]:
            s = j if s == m + 1 else s
            j = f[j]
        j -= 1
        f[i] = j

    j = f[0]
    for i in range(m):
        good_suffix[i] = j if i == j else good_suffix[i]
        if i == j:
            j = f[j]


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Алгоритм Кнута-Морріса-Пратта для пошуку підрядка.

    Args:
        text: Текст, у якому здійснюється пошук
        pattern: Підрядок для пошуку

    Returns:
        Список позицій знайдених входжень патерну
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    # Побудова таблиці відмов (failure function)
    lps = build_lps_table(pattern)

    matches = []
    i = 0  # індекс для тексту
    j = 0  # індекс для патерну

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            matches.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches


def build_lps_table(pattern: str) -> List[int]:
    """Побудова таблиці найдовших правильних префіксів (LPS)."""
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def rabin_karp(text: str, pattern: str, prime: int = 101) -> List[int]:
    """
    Алгоритм Рабіна-Карпа для пошуку підрядка.

    Args:
        text: Текст, у якому здійснюється пошук
        pattern: Підрядок для пошуку
        prime: Просте число для обчислення хешу

    Returns:
        Список позицій знайдених входжень патерну
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    base = 256
    m = len(pattern)
    n = len(text)
    pattern_hash = 0
    text_hash = 0
    h = 1

    # Обчислення h = base^(m-1) % prime
    for i in range(m - 1):
        h = (h * base) % prime

    # Обчислення хешу патерну та першого вікна тексту
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        text_hash = (base * text_hash + ord(text[i])) % prime

    matches = []

    # Ковзаюче вікно для пошуку
    for i in range(n - m + 1):
        # Якщо хеші збігаються
        if pattern_hash == text_hash:
            # Перевірка точного збігу
            if text[i:i + m] == pattern:
                matches.append(i)

        # Обчислення хешу для наступного вікна
        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            # Забезпечення позитивного хешу
            if text_hash < 0:
                text_hash += prime

    return matches


def run_benchmarks():
    """Запуск бенчмарків для порівняння алгоритмів."""
    
    # Отримуємо шлях до поточної директорії
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Читання статей
    article_1_path = os.path.join(current_dir, 'article_1.txt')
    article_2_path = os.path.join(current_dir, 'article_2.txt')
    
    with open(article_1_path, 'r', encoding='utf-8') as f:
        article_1 = f.read()
    
    with open(article_2_path, 'r', encoding='utf-8') as f:
        article_2 = f.read()

    # Підрядки для тестування
    test_cases = {
        'існуючі': [
            ('Алгоритми пошуку', article_1),
            ('текстом', article_1),
            ('Пошук в структурах', article_2),
            ('алгоритм', article_2),
        ],
        'вигадані': [
            ('XYZqwerty123notfound', article_1),
            ('абвгдеєжзийклмнопрстуфхцчшщюя', article_1),
            ('NotInTheText999', article_2),
            ('zzz_impossible_zzz', article_2),
        ]
    }

    algorithms = {
        'Boyer-Moore': boyer_moore,
        'KMP': kmp_search,
        'Rabin-Karp': rabin_karp,
    }

    print("=" * 80)
    print("ПОРІВНЯННЯ ЕФЕКТИВНОСТІ АЛГОРИТМІВ ПОШУКУ ПІДРЯДКА")
    print("=" * 80)
    print()

    results = {}

    for case_type in ['існуючі', 'вигадані']:
        print(f"\n{'=' * 80}")
        print(f"ТЕСТУВАННЯ НА {case_type.upper()} ПІДРЯДКАХ")
        print(f"{'=' * 80}\n")

        results[case_type] = {}

        for algo_name, algo_func in algorithms.items():
            results[case_type][algo_name] = {}
            print(f"\n--- Алгоритм: {algo_name} ---\n")

            for idx, (pattern, text) in enumerate(test_cases[case_type], 1):
                article_num = 1 if text == article_1 else 2

                # Визначення кількості повторень для timeit
                repeat_count = 1000

                # Вимірювання часу
                time_taken = timeit.timeit(
                    lambda: algo_func(text, pattern),
                    number=repeat_count
                )

                avg_time = (time_taken / repeat_count) * 1000000  # мікросекунди

                results[case_type][algo_name][f'Test {idx}'] = avg_time

                print(f"  Стаття {article_num}, Підрядок: '{pattern[:30]}{'...' if len(pattern) > 30 else ''}'")
                print(f"    Час (мкс): {avg_time:.4f}")
                print(f"    Знайдено входжень: {len(algo_func(text, pattern))}")
                print()

    # Підсумкова таблиця
    print("\n" + "=" * 80)
    print("ПІДСУМКОВА ТАБЛИЦЯ (час в мікросекундах)")
    print("=" * 80)

    for case_type in ['існуючі', 'вигадані']:
        print(f"\n{case_type.upper()} ПІДРЯДКИ:")
        print("-" * 60)
        print(f"{'Алгоритм':<20} {'Test 1':>12} {'Test 2':>12} {'Test 3':>12} {'Test 4':>12}")
        print("-" * 60)

        for algo_name in algorithms.keys():
            row = f"{algo_name:<20}"
            times = []
            for test_key in ['Test 1', 'Test 2', 'Test 3', 'Test 4']:
                if test_key in results[case_type][algo_name]:
                    time_val = results[case_type][algo_name][test_key]
                    row += f" {time_val:>11.4f}"
                    times.append(time_val)

            # Середній час
            avg_time = sum(times) / len(times) if times else 0
            print(row)

        print("-" * 60)

    # Визначення найшвидшого алгоритму
    print("\n" + "=" * 80)
    print("ВИСНОВКИ")
    print("=" * 80)

    for case_type in ['існуючі', 'вигадані']:
        print(f"\n{case_type.upper()} ПІДРЯДКИ:")
        times_per_algo = {}
        for algo_name in algorithms.keys():
            times = list(results[case_type][algo_name].values())
            avg_time = sum(times) / len(times)
            times_per_algo[algo_name] = avg_time

        fastest = min(times_per_algo, key=times_per_algo.get)
        print(f"  ✓ Найшвидший алгоритм: {fastest} ({times_per_algo[fastest]:.4f} мкс в середньому)")

        for algo_name, time_val in sorted(times_per_algo.items(), key=lambda x: x[1]):
            print(f"    - {algo_name}: {time_val:.4f} мкс")

    # Загальний висновок
    print(f"\n{'=' * 80}")
    print("ЗАГАЛЬНИЙ РЕЗУЛЬТАТ:")
    all_times = {}
    for algo_name in algorithms.keys():
        all_times[algo_name] = []
        for case_type in ['існуючі', 'вигадані']:
            all_times[algo_name].extend(results[case_type][algo_name].values())
        all_times[algo_name] = sum(all_times[algo_name]) / len(all_times[algo_name])

    fastest_overall = min(all_times, key=all_times.get)
    print(f"\nНайефективніший алгоритм в цілому: {fastest_overall}")
    print("\nРейтинг алгоритмів:")
    for idx, (algo_name, avg_time) in enumerate(sorted(all_times.items(), key=lambda x: x[1]), 1):
        print(f"  {idx}. {algo_name}: {avg_time:.4f} мкс")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    run_benchmarks()
