
"""
Task 2: Знаходження найменшого значення у двійковому дереві
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


def find_min_iterative(root):
    """
    Знаходить найменше значення у двійковому дереві (ітеративний підхід).

    Використовує чергу (queue) для обходу дерева в ширину (BFS).

    Args:
        root (Node): Корінь дерева

    Returns:
        int/float: Найменше значення у дереві або None якщо дерево порожнє

    Часова складність: O(n) - n кількість вузлів
    Просторова складність: O(w) - w максимальна ширина дерева
    """
    if root is None:
        return None

    min_value = root.value
    queue = [root]

    while queue:
        node = queue.pop(0)

        # Оновлюємо мінімум
        if node.value < min_value:
            min_value = node.value

        # Додаємо дітей до черги
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return min_value


def find_min_recursive(root):
    """
    Знаходить найменше значення у двійковому дереві (рекурсивний підхід).

    Використовує рекурсію для обходу дерева в глибину (DFS).

    Args:
        root (Node): Корінь дерева

    Returns:
        int/float: Найменше значення у дереві або None якщо дерево порожнє

    Часова складність: O(n) - n кількість вузлів
    Просторова складність: O(h) - h висота дерева (стек викликів)
    """
    if root is None:
        return None

    # Знаходимо мінімум у лівому поддереві
    left_min = find_min_recursive(root.left)
    # Знаходимо мінімум у правому поддереві
    right_min = find_min_recursive(root.right)

    # Порівнюємо значення поточного вузла з мінімумами поддерев
    min_value = root.value

    if left_min is not None and left_min < min_value:
        min_value = left_min

    if right_min is not None and right_min < min_value:
        min_value = right_min

    return min_value


def find_min_dfs_stack(root):
    """
    Знаходить найменше значення у двійковому дереві (обхід DFS зі стеком).

    Використовує явний стек замість рекурсії.

    Args:
        root (Node): Корінь дерева

    Returns:
        int/float: Найменше значення у дереві або None якщо дерево порожнє

    Часова складність: O(n) - n кількість вузлів
    Просторова складність: O(h) - h висота дерева
    """
    if root is None:
        return None

    min_value = root.value
    stack = [root]

    while stack:
        node = stack.pop()

        # Оновлюємо мінімум
        if node.value < min_value:
            min_value = node.value

        # Додаємо дітей до стека (права спочатку, щоб ліва обробилася першою)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return min_value


def find_min_bst_optimized(root):
    """
    Знаходить найменше значення у двійковому дереві пошуку (оптимізований підхід).

    Для BST найменше значення завжди знаходиться в найлівішому вузлі.
    Цей метод працює тільки для двійкових дерев пошуку!

    Args:
        root (Node): Корінь BST

    Returns:
        int/float: Найменше значення у BST або None якщо дерево порожнє

    Часова складність: O(h) - h висота дерева (в ідеальному випадку O(log n))
    Просторова складність: O(1) - не використовуємо додатковий простір
    """
    if root is None:
        return None

    current = root
    # Йдемо максимально ліворуч
    while current.left is not None:
        current = current.left

    return current.value


def print_comparison(tree_name, tree):
    """
    Порівнює результати трьох методів пошуку мінімального значення.

    Args:
        tree_name (str): Назва дерева
        tree (Node): Корінь дерева
    """
    result_iterative = find_min_iterative(tree)
    result_recursive = find_min_recursive(tree)
    result_dfs = find_min_dfs_stack(tree)

    print(f"\n{'='*70}")
    print(f"Дерево: {tree_name.upper()}")
    print(f"{'='*70}")
    print(f"Найменше значення (ітеративний BFS):  {result_iterative}")
    print(f"Найменше значення (рекурсивний DFS): {result_recursive}")
    print(f"Найменше значення (DFS зі стеком):  {result_dfs}")

    # Перевіримо що всі методи дають однаковий результат
    assert result_iterative == result_recursive == result_dfs, \
        "Результати методів не збігаються!"
    print(f"✅ Всі методи дали однаковий результат")


def print_comparison_with_bst(tree_name, tree):
    """
    Порівнює результати для BST включаючи оптимізований метод.

    Args:
        tree_name (str): Назва дерева
        tree (Node): Корінь BST
    """
    result_iterative = find_min_iterative(tree)
    result_recursive = find_min_recursive(tree)
    result_dfs = find_min_dfs_stack(tree)
    result_bst_optimized = find_min_bst_optimized(tree)

    print(f"\n{'='*70}")
    print(f"Дерево: {tree_name.upper()} (BST оптимізований пошук)")
    print(f"{'='*70}")
    print(f"Найменше значення (ітеративний BFS):     {result_iterative}")
    print(f"Найменше значення (рекурсивний DFS):    {result_recursive}")
    print(f"Найменше значення (DFS зі стеком):     {result_dfs}")
    print(f"Найменше значення (BST оптимізований): {result_bst_optimized} ⭐")

    # Перевіримо що всі методи дають однаковий результат
    assert result_iterative == result_recursive == result_dfs == result_bst_optimized, \
        "Результати методів не збігаються!"
    print(f"✅ Всі методи дали однаковий результат")


def main():
    """Основна функція для тестування алгоритмів."""

    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  ЗНАХОДЖЕННЯ НАЙМЕНШОГО ЗНАЧЕННЯ У ДВІЙКОВОМУ ДЕРЕВІ  ".center(68) + "█")
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
        print_comparison(tree_name, tree)

    # Спеціальний тест для BST дерева з оптимізованим методом
    print(f"\n\n{'█' * 70}")
    print("█" + " " * 68 + "█")
    print("█" + "  ОПТИМІЗОВАНИЙ ПОШУК ДЛЯ ДВІЙКОВИХ ДЕРЕВ ПОШУКУ (BST)  ".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)

    complex_tree = get_tree('complex')
    print_comparison_with_bst('complex (BST)', complex_tree)

    # Тестуємо на порожному дереві
    print(f"\n{'='*70}")
    print("Дерево: EMPTY (ПОРОЖНЄ)")
    print(f"{'='*70}")
    result = find_min_recursive(None)
    print(f"Найменше значення (порожнє дерево): {result}")
    print(f"✅ Коректно обробляється порожне дерево")

    # Тестуємо на дереві з одним вузлом
    print(f"\n{'='*70}")
    print("Дерево: SINGLE NODE (ОДИН ВУЗОЛ)")
    print(f"{'='*70}")
    single_node_tree = Node(42)
    result = find_min_recursive(single_node_tree)
    print(f"Найменше значення (один вузол зі значенням 42): {result}")
    print(f"✅ Коректно обробляється дерево з одним вузлом")

    # Тестуємо на дереві з від'ємними числами
    print(f"\n{'='*70}")
    print("Дерево: NEGATIVE NUMBERS (З'ЄМНІ ЧИСЛА)")
    print(f"{'='*70}")
    negative_tree = Node(-5, left=Node(-10, left=Node(-20)), right=Node(-1))
    result = find_min_recursive(negative_tree)
    print(f"Найменше значення (дерево з від'ємними числами): {result}")
    print(f"✅ Коректно обробляється дерево з від'ємними числами")

    print("\n" + "█" * 70)
    print("█" + "  ТЕСТУВАННЯ ЗАВЕРШЕНО УСПІШНО ✅  ".center(68) + "█")
    print("█" * 70 + "\n")


if __name__ == "__main__":
    main()
