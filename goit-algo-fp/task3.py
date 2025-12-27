import heapq

class Graph:
    def __init__(self):
        # Використовуємо список суміжності для представлення графа
        self.adj_list = {}

    def add_edge(self, u, v, weight):
        """Додає зважене ребро до графа (орієнтованого)."""
        if u not in self.adj_list:
            self.adj_list[u] = []
        self.adj_list[u].append((v, weight))

        # Якщо граф неорієнтований, розкоментуйте наступні рядки:
        # if v not in self.adj_list:
        #     self.adj_list[v] = []
        # self.adj_list[v].append((u, weight))

    def dijkstra(self, start_node):
        """Знаходить найкоротші шляхи від start_node до всіх інших вершин."""
        # Відстані до всіх вершин ініціалізуємо нескінченністю
        distances = {node: float('inf') for node in self.adj_list}
        # Якщо в графі є вершини без вихідних ребер, додамо їх теж
        for neighbors in self.adj_list.values():
            for neighbor, _ in neighbors:
                if neighbor not in distances:
                    distances[neighbor] = float('inf')

        distances[start_node] = 0

        # Бінарна купа (пріоритетна черга)
        # Зберігає кортежі (відстань, вершина)
        priority_queue = [(0, start_node)]

        while priority_queue:
            # Витягуємо вершину з найменшою поточною відстанню
            current_distance, current_node = heapq.heappop(priority_queue)

            # Якщо знайдена відстань більша за вже збережену, ігноруємо (застарілий запис)
            if current_distance > distances[current_node]:
                continue

            # Перевіряємо всіх сусідів поточної вершини
            for neighbor, weight in self.adj_list.get(current_node, []):
                distance = current_distance + weight

                # Якщо знайдено коротший шлях до сусіда
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances

# Приклад використання:
if __name__ == "__main__":
    g = Graph()
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'C', 5)
    g.add_edge('B', 'D', 10)
    g.add_edge('C', 'D', 3)
    g.add_edge('D', 'E', 7)
    g.add_edge('E', 'A', 8)

    start = 'A'
    shortest_paths = g.dijkstra(start)

    print(f"Найкоротші відстані від вершини {start}:")
    for node, dist in shortest_paths.items():
        print(f"До {node}: {dist}")
