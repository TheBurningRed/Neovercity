class Node:
    """Клас для вузла однозв'язного списку"""
    def __init__(self, data):
        self.data = data
        self.next = None

def reverse_list(head):
    """1. Реверсування списку (зміна посилань між вузлами)"""
    prev = None
    current = head
    while current:
        next_node = current.next  # Зберігаємо наступний вузол
        current.next = prev       # Змінюємо посилання на попередній
        prev = current            # Пересуваємо prev
        current = next_node       # Пересуваємо current
    return prev

def merge_sorted_lists(l1, l2):
    """2. Об'єднання двох відсортованих списків в один відсортований"""
    dummy = Node(0)  # Тимчасовий "якірний" вузол
    tail = dummy

    while l1 and l2:
        if l1.data <= l2.data:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    # Додаємо залишок елементів, якщо один зі списків закінчився раніше
    tail.next = l1 or l2

    return dummy.next

def insertion_sort_list(head):
    """3. Сортування однозв'язного списку методом вставок"""
    if not head or not head.next:
        return head

    sorted_head = None
    current = head

    while current:
        next_node = current.next # Зберігаємо наступний для ітерації

        # Вставка поточного вузла у відсортовану частину
        if not sorted_head or current.data <= sorted_head.data:
            current.next = sorted_head
            sorted_head = current
        else:
            search = sorted_head
            while search.next and search.next.data < current.data:
                search = search.next
            current.next = search.next
            search.next = current

        current = next_node

    return sorted_head

def print_list(head):
    """Допоміжна функція для друку списку"""
    elements = []
    curr = head
    while curr:
        elements.append(str(curr.data))
        curr = curr.next
    print(" -> ".join(elements) + " -> None")

# --- Приклад використання ---
if __name__ == "__main__":
    # Створення невідсортованого списку: 5 -> 2 -> 8 -> 1
    head = Node(5)
    head.next = Node(2)
    head.next.next = Node(8)
    head.next.next.next = Node(1)

    print("Оригінальний список:")
    print_list(head)

    # Тест сортування
    head = insertion_sort_list(head)
    print("\nПісля сортування вставками:")
    print_list(head)

    # Тест реверсування
    head = reverse_list(head)
    print("\nПісля реверсування:")
    print_list(head)

    # Тест об'єднання двох відсортованих списків
    list_a = Node(1); list_a.next = Node(3); list_a.next.next = Node(10)
    list_b = Node(2); list_b.next = Node(4); list_b.next.next = Node(6)

    print("\nСписок A:", end=" ")
    print_list(list_a)
    print("Список B:", end=" ")
    print_list(list_b)

    merged = merge_sorted_lists(list_a, list_b)
    print("Результат об'єднання:")
    print_list(merged)
