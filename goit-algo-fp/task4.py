import uuid
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла

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

def draw_tree(tree_root):
    if tree_root is None:
        print("Дерево порожнє.")
        return

    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.title("Візуалізація бінарної купи")
    plt.show()

def build_heap_tree(heap, index=0):
    """
    Рекурсивно будує структуру дерева з масиву (купи).
    Індекси нащадків для i: лівий = 2*i + 1, правий = 2*i + 2.
    """
    if index < len(heap):
        node = Node(heap[index])
        node.left = build_heap_tree(heap, 2 * index + 1)
        node.right = build_heap_tree(heap, 2 * index + 2)
        return node
    return None

if __name__ == "__main__":
    # Приклад бінарної купи (наприклад, після heapq.heapify)
    # Представлення у вигляді масиву
    heap_list = [1, 3, 5, 7, 9, 10, 11, 15, 20]

    # Створення дерева з купи
    heap_root = build_heap_tree(heap_list)

    # Візуалізація
    draw_tree(heap_root)
