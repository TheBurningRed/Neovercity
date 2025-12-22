
"""
Task 3: Знаходження суми всіх значень у двійковому дереві
"""

import sys
from pathlib import Path

# Додаємо поточну директорію до path для імпорту
sys.path.insert(0, str(Path(__file__).parent))

# Імпортуємо з файлу як модуль
import importlib.util
spec = importlib.util.spec_from_file_location("binary_tree_mock", "binary-tree.mock.py")
binary_tree_mock = importlib.util.module_from_spec(spec)
spec.loader.exec_module(binary_tree_mock)

Node = binary_tree_mock.Node
get_tree = binary_tree_mock.get_tree


def sum_tree_recursive(root):
    """
    Знаходить суму всіх значень у двійковому дереві (рекурсивний підхід).

    Використовує рекурсію для обходу дерева в глибину (DFS).

    Args:
        root (Node): Корінь дерева

    Returns:
        int/float: Сума всіх значень у дереві або 0 якщо дерево порожнє

    Часова складність: O(n) - n кількість вузлів
    Просторова складність: O(h) - h висота дерева (стек викликів)
    """
    if root is None:
        return 0

    # Рекурсивно додаємо значення поточного вузла та сум поддерев
    left_sum = sum_tree_recursive(root.left)
    right_sum = sum_tree_recursive(root.right)

    return root.value + left_sum + right_sum


def sum_tree_iterative_bfs(root):
    """
    Знаходить суму всіх значень у двійковому дереві (ітеративний BFS).

    Використовує чергу для обходу дерева рівень за рівнем.

    Args:
        root (Node): Корінь дерева

    Returns:
        int/float: Сума всіх значень у дереві або 0 якщо дерево порожнє

    Часова складність: O(n) - n кількість вузлів
    Просторова складність: O(w) - w максимальна ширина дерева
    """
    if root is None:
        return 0

    total_sum = 0
    queue = [root]

    while queue:
        node = queue.pop(0)
        total_sum += node.value

        # Додаємо дітей до черги
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return total_sum


def sum_tree_iterative_dfs(root):
    """
    Знаходить суму всіх значень у двійковому дереві (ітеративний DFS зі стеком).

    Використовує явний стек для обходу в глибину замість рекурсії.

    Args:
        root (Node): Корінь дерева

    Returns:
        int/float: Сума всіх значень у дереві або 0 якщо дерево порожнє

    Часова складність: O(n) - n кількість вузлів
    Просторова складність: O(h) - h висота дерева
    """
    if root is None:
        return 0

    total_sum = 0
    stack = [root]

    while stack:
        node = stack.pop()
        total_sum += node.value

        # Додаємо дітей до стека (права спочатку, щоб ліва обробилася першою)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return total_sum


def sum_tree_with_count(root):
    """
    Знаходить суму всіх значень та кількість вузлів у дереві.

    Повертає кортеж (сума, кількість вузлів, середнє значення).

    Args:
        root (Node): Корінь дерева

    Returns:
        tuple: (сума, кількість вузлів, середнє значення)

    Часова складність: O(n)
    Просторова складність: O(h)
    """
    if root is None:
        return 0, 0, 0

    left_sum, left_count, _ = sum_tree_with_count(root.left)
    right_sum, right_count, _ = sum_tree_with_count(root.right)

    total_sum = root.value + left_sum + right_sum
    total_count = 1 + left_count + right_count
    average = total_sum / total_count if total_count > 0 else 0

    return total_sum, total_count, average


def sum_tree_by_level(root):
    """
    Знаходить суму значень для кожного рівня дерева.

    Args:
        root (Node): Корінь дерева

    Returns:
        list: Список сум для кожного рівня

    Часова складність: O(n)
    Просторова складність: O(w)
    """
    if root is None:
        return []

    level_sums = []
    queue = [root]

    while queue:
        level_sum = 0
        next_level = []

        # Обробляємо всі вузли поточного рівня
        for node in queue:
            level_sum += node.value
            if node.left:
                next_level.append(node.left)
            if node.right:
                next_level.append(node.right)

        level_sums.append(level_sum)
        queue = next_level

    return level_sums


def count_nodes(root):
    """
    Підраховує кількість вузлів у дереві.

    Args:
        root (Node): Корінь дерева

    Returns:
        int: Кількість вузлів

    Часова складність: O(n)
    Просторова складність: O(h)
    """
    if root is None:
        return 0

    return 1 + count_nodes(root.left) + count_nodes(root.right)


def get_tree_height(root):
    """
    Обчислює висоту дерева.

    Args:
        root (Node): Корінь дерева

    Returns:
        int: Висота дерева (0 для одного вузла, -1 для порожного)

    Часова складність: O(n)
    Просторова складність: O(h)
    """
    if root is None:
        return -1

    left_height = get_tree_height(root.left)
    right_height = get_tree_height(root.right)

    return 1 + max(left_height, right_height)


def print_tree_statistics(tree_name, tree):
    """
    Виводить статистику по дереву.

    Args:
        tree_name (str): Назва дерева
        tree (Node): Корінь дерева
    """
    print(f"\n{'='*70}")
    print(f"Дерево: {tree_name.upper()}")
    print(f"{'='*70}")

    # Три методи обчислення суми
    result_recursive = sum_tree_recursive(tree)
    result_bfs = sum_tree_iterative_bfs(tree)
    result_dfs = sum_tree_iterative_dfs(tree)

    print(f"Сума значень (рекурсивний DFS):      {result_recursive}")
    print(f"Сума значень (ітеративний BFS):    {result_bfs}")
    print(f"Сума значень (ітеративний DFS):    {result_dfs}")

    # Перевіримо що всі методи дають однаковий результат
    assert result_recursive == result_bfs == result_dfs, \
        "Результати методів не збігаються!"
    print(f"✅ Всі методи дали однаковий результат")

    # Додаткова статистика
    total_sum, node_count, average = sum_tree_with_count(tree)
    height = get_tree_height(tree)

    print(f"\n📊 Статистика:")
    print(f"   Кількість вузлів:     {node_count}")
    print(f"   Висота дерева:        {height}")
    print(f"   Сума значень:         {total_sum}")
    print(f"   Середнє значення:     {average:.2f}")

    # Сума по рівням
    level_sums = sum_tree_by_level(tree)
    print(f"\n📈 Сума по рівням:")
    for level, level_sum in enumerate(level_sums):
        print(f"   Рівень {level}: {level_sum}")


def main():
    """Основна функція для тестування алгоритмів."""

    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  ЗНАХОДЖЕННЯ СУМИ ВСІХ ЗНАЧЕНЬ У ДВІЙКОВОМУ ДЕРЕВІ  ".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)

    # Тестуємо на різних деревах
    trees_to_test = [
        ('balanced', get_tree('balanced')),
        ('left_skewed', get_tree('left_skewed')),
        ('right_skewed', get_tree('right_skewed')),
        ('full', get_tree('full')),
        ('complex', get_tree('complex')),
        ('sparse', get_tree('sparse')),
    ]

    for tree_name, tree in trees_to_test:
        print_tree_statistics(tree_name, tree)

    # Тестуємо на порожному дереві
    print(f"\n{'='*70}")
    print("Дерево: EMPTY (ПОРОЖНЄ)")
    print(f"{'='*70}")
    result = sum_tree_recursive(None)
    print(f"Сума значень (порожнє дерево): {result}")
    print(f"✅ Коректно обробляється порожне дерево")

    # Тестуємо на дереві з одним вузлом
    print(f"\n{'='*70}")
    print("Дерево: SINGLE NODE (ОДИН ВУЗОЛ)")
    print(f"{'='*70}")
    single_node_tree = Node(42)
    result = sum_tree_recursive(single_node_tree)
    total_sum, node_count, average = sum_tree_with_count(single_node_tree)
    print(f"Сума значень (один вузол зі значенням 42): {result}")
    print(f"📊 Статистика:")
    print(f"   Кількість вузлів:     {node_count}")
    print(f"   Висота дерева:        {get_tree_height(single_node_tree)}")
    print(f"   Середнє значення:     {average:.2f}")
    print(f"✅ Коректно обробляється дерево з одним вузлом")

    # Тестуємо на дереві з від'ємними числами
    print(f"\n{'='*70}")
    print("Дерево: NEGATIVE AND POSITIVE NUMBERS")
    print(f"{'='*70}")
    mixed_tree = Node(5,
                      left=Node(-10, left=Node(-5)),
                      right=Node(15, right=Node(20)))
    print_tree_statistics('mixed (від\'ємні та позитивні)', mixed_tree)

    # Порівняння складності
    print(f"\n{'█' * 70}")
    print("█" + " " * 68 + "█")
    print("█" + "  ПОРІВНЯННЯ СКЛАДНОСТІ АЛГОРИТМІВ  ".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)

    print(f"\n{'─'*70}")
    print(f"{'Метод':<30} {'Часова':<20} {'Просторова':<20}")
    print(f"{'─'*70}")
    print(f"{'Рекурсивний DFS':<30} {'O(n)':<20} {'O(h)':<20}")
    print(f"{'Ітеративний BFS':<30} {'O(n)':<20} {'O(w)':<20}")
    print(f"{'Ітеративний DFS':<30} {'O(n)':<20} {'O(h)':<20}")
    print(f"{'─'*70}")
    print(f"де n - кількість вузлів, h - висота, w - максимальна ширина")

    print("\n" + "█" * 70)
    print("█" + "  ТЕСТУВАННЯ ЗАВЕРШЕНО УСПІШНО ✅  ".center(68) + "█")
    print("█" * 70 + "\n")


if __name__ == "__main__":
    main()
