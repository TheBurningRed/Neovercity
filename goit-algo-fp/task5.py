import uuid
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def draw_tree(tree_root, title="Tree Visualization"):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()

def generate_color(step, total_steps):
    """Генерує колір від темного до світлого у форматі #RRGGBB."""
    # Базовий колір: синій відтінок
    # Змінюємо інтенсивність від темного (напр. 30) до світлого (напр. 220)
    base_val = int(30 + (step / total_steps) * 190)
    # Форматуємо у HEX (R, G, B) - робимо синій градієнт
    return f"#{base_val:02x}{base_val:02x}F0"

def count_nodes(root):
    if not root:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)

def visualize_dfs(root):
    """Обхід у глибину (DFS) з використанням стека."""
    if not root:
        return

    total_nodes = count_nodes(root)
    stack = [root]
    visited = set()
    step = 0

    while stack:
        node = stack.pop()
        if node.id not in visited:
            visited.add(node.id)
            node.color = generate_color(step, total_nodes)
            step += 1

            # Додаємо правий, потім лівий, щоб лівий оброблявся першим (LIFO)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

    draw_tree(root, title="DFS Traversal (Dark to Light)")

def visualize_bfs(root):
    """Обхід у ширину (BFS) з використанням черги."""
    if not root:
        return

    total_nodes = count_nodes(root)
    queue = deque([root])
    visited = {root.id}
    step = 0

    while queue:
        node = queue.popleft()
        node.color = generate_color(step, total_nodes)
        step += 1

        if node.left:
            if node.left.id not in visited:
                visited.add(node.left.id)
                queue.append(node.left)
        if node.right:
            if node.right.id not in visited:
                visited.add(node.right.id)
                queue.append(node.right)

    draw_tree(root, title="BFS Traversal (Dark to Light)")

# Створення тестового дерева
if __name__ == "__main__":
    # Будуємо дерево
    root = Node(1)
    root.left = Node(2, color="#FFFFFF")
    root.right = Node(3, color="#FFFFFF")
    root.left.left = Node(4, color="#FFFFFF")
    root.left.right = Node(5, color="#FFFFFF")
    root.right.left = Node(6, color="#FFFFFF")
    root.right.right = Node(7, color="#FFFFFF")

    # Для демонстрації спочатку викликаємо BFS
    visualize_bfs(root)

    # Скидаємо кольори перед DFS
    root.color = "#FFFFFF"; root.left.color = "#FFFFFF"; root.right.color = "#FFFFFF"
    root.left.left.color = "#FFFFFF"; root.left.right.color = "#FFFFFF"
    root.right.left.color = "#FFFFFF"; root.right.right.color = "#FFFFFF"

    visualize_dfs(root)
