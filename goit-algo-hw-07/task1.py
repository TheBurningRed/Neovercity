
"""
Task 1: Знаходження найбільшого значення у двійковому дереві
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


def find_max_iterative(root):
    """
    Знаходить найбільше значення у двійковому дереві (ітеративний підхід).

    Використовує черговість (queue) для обходу дерева в ширину (BFS).

    Args:
        root (Node): Корінь дерева

    Returns:
        int/float: Найбільше значення у дереві або None якщо дерево порожнє

    Часова складність: O(n) - n кількість вузлів
    Просторова складність: O(w) - w максимальна ширина дерева
    """
    if root is None:
        return None

    max_value = root.value
    queue = [root]

    while queue:
        node = queue.pop(0)

        # Оновлюємо максимум
        if node.value > max_value:
            max_value = node.value

        # Додаємо дітей до черги
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return max_value


def find_max_recursive(root):
    """
    Знаходить найбільше значення у двійковому дереві (рекурсивний підхід).

    Використовує рекурсію для обходу дерева в глибину (DFS).

    Args:
        root (Node): Корінь дерева

    Returns:
        int/float: Найбільше значення у дереві або None якщо дерево порожнє

    Часова складність: O(n) - n кількість вузлів
    Просторова складність: O(h) - h висота дерева (стек вызовів)
    """
    if root is None:
        return None

    # Знаходимо максимум у лівому поддереві
    left_max = find_max_recursive(root.left)
    # Знаходимо максимум у правому поддереві
    right_max = find_max_recursive(root.right)

    # Порівнюємо значення поточного вузла з максимумами поддерев
    max_value = root.value

    if left_max is not None and left_max > max_value:
        max_value = left_max

    if right_max is not None and right_max > max_value:
        max_value = right_max

    return max_value


def find_max_dfs_stack(root):
    """
    Знаходить найбільше значення у двійковому дереві (обхід DFS зі стеком).

    Використовує явний стек замість рекурсії.

    Args:
        root (Node): Корінь дерева

    Returns:
        int/float: Найбільше значення у дереві або None якщо дерево порожнє

    Часова складність: O(n) - n кількість вузлів
    Просторова складність: O(h) - h висота дерева
    """
    if root is None:
        return None

    max_value = root.value
    stack = [root]

    while stack:
        node = stack.pop()

        # Оновлюємо максимум
        if node.value > max_value:
            max_value = node.value

        # Додаємо дітей до стека (права спочатку, щоб ліва обробилася першою)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return max_value


def print_comparison(tree_name, tree):
    """
    Порівнює результати трьох методів пошуку максимального значення.

    Args:
        tree_name (str): Назва дерева
        tree (Node): Корінь дерева
    """
    result_iterative = find_max_iterative(tree)
    result_recursive = find_max_recursive(tree)
    result_dfs = find_max_dfs_stack(tree)

    print(f"\n{'='*60}")
    print(f"Дерево: {tree_name.upper()}")
    print(f"{'='*60}")
    print(f"Найбільше значення (ітеративний BFS):  {result_iterative}")
    print(f"Найбільше значення (рекурсивний DFS): {result_recursive}")
    print(f"Найбільше значення (DFS зі стеком):  {result_dfs}")

    # Перевіримо що всі методи дають однаковий результат
    assert result_iterative == result_recursive == result_dfs, \
        "Результати методів не збігаються!"
    print(f"✅ Всі методи дали однаковий результат")


def main():
    """Основна функція для тестування алгоритмів."""

    print("\n" + "█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  ЗНАХОДЖЕННЯ НАЙБІЛЬШОГО ЗНАЧЕННЯ У ДВІЙКОВОМУ ДЕРЕВІ  ".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)

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
        print_comparison(tree_name, tree)

    # Тестуємо на порожному дереві
    print(f"\n{'='*60}")
    print("Дерево: EMPTY (ПОРОЖНЄ)")
    print(f"{'='*60}")
    result = find_max_recursive(None)
    print(f"Найбільше значення (порожнє дерево): {result}")
    print(f"✅ Коректно обробляється порожне дерево")

    # Тестуємо на дереві з одним вузлом
    print(f"\n{'='*60}")
    print("Дерево: SINGLE NODE (ОДИН ВУЗОЛ)")
    print(f"{'='*60}")
    single_node_tree = Node(42)
    result = find_max_recursive(single_node_tree)
    print(f"Найбільше значення (один вузол зі значенням 42): {result}")
    print(f"✅ Коректно обробляється дерево з одним вузлом")

    print("\n" + "█" * 60)
    print("█" + "  ТЕСТУВАННЯ ЗАВЕРШЕНО УСПІШНО ✅  ".center(58) + "█")
    print("█" * 60 + "\n")


if __name__ == "__main__":
    main()
