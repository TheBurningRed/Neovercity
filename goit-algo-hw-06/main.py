
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
from collections import deque
import heapq
import time

@dataclass
class PowerSubstation:
    """Представляє електричну підстанцію у мережі"""
    id: str
    name: str
    district: str
    voltage: str
    capacity_mw: float

@dataclass
class PowerLine:
    """Представляє лінію передачі між підстанціями"""
    from_station: str
    to_station: str
    voltage: str
    capacity_mw: float
    length_km: float

class MoscowPowerGrid:
    """Представляє електричну мережу Москви як граф"""

    def __init__(self):
        self.graph = nx.Graph()
        self.substations: Dict[str, PowerSubstation] = {}
        self.power_lines: List[PowerLine] = []
        self._initialize_grid()

    def _initialize_grid(self):
        """Ініціалізувати мережу з основними підстанціями та лініями"""

        substations = [
            PowerSubstation("SS_1", "Лужники", "Центр", "500кВ", 300),
            PowerSubstation("SS_2", "Одинцово", "Захід", "220кВ", 250),
            PowerSubstation("SS_3", "Химки", "Північний", "220кВ", 280),
            PowerSubstation("SS_4", "Люберцы", "Схід", "110кВ", 200),
            PowerSubstation("SS_5", "Балашиха", "Північний схід", "220кВ", 270),
            PowerSubstation("SS_6", "Зеленоград", "Північний захід", "110кВ", 150),
            PowerSubstation("SS_7", "Домодєдово", "Південний", "220кВ", 260),
            PowerSubstation("SS_8", "Ясенево", "Південно-західний", "110кВ", 180),
            PowerSubstation("SS_9", "Косино", "Південний схід", "110кВ", 170),
            PowerSubstation("SS_10", "GRES-2", "Центр", "500кВ", 400),
        ]

        for station in substations:
            self.substations[station.id] = station
            self.graph.add_node(station.id,
                                name=station.name,
                                voltage=station.voltage,
                                capacity=station.capacity_mw)

        power_lines = [
            PowerLine("SS_1", "SS_10", "500кВ", 500, 5.2),
            PowerLine("SS_10", "SS_3", "220кВ", 350, 12.5),
            PowerLine("SS_10", "SS_5", "220кВ", 350, 15.3),
            PowerLine("SS_1", "SS_2", "220кВ", 300, 18.7),
            PowerLine("SS_2", "SS_6", "110кВ", 200, 42.3),
            PowerLine("SS_3", "SS_6", "110кВ", 200, 28.5),
            PowerLine("SS_1", "SS_8", "110кВ", 250, 8.9),
            PowerLine("SS_8", "SS_7", "220кВ", 320, 35.2),
            PowerLine("SS_7", "SS_9", "110кВ", 180, 42.1),
            PowerLine("SS_4", "SS_5", "110кВ", 200, 18.6),
            PowerLine("SS_4", "SS_9", "110кВ", 190, 25.4),
            PowerLine("SS_5", "SS_3", "220кВ", 350, 22.1),
            PowerLine("SS_1", "SS_4", "220кВ", 330, 25.8),
        ]

        for line in power_lines:
            self.power_lines.append(line)
            self.graph.add_edge(line.from_station, line.to_station,
                                voltage=line.voltage,
                                capacity=line.capacity_mw,
                                weight=line.length_km,
                                length=line.length_km)

class PathFindingAnalyzer:
    """Аналізує алгоритми DFS, BFS та Дейкстри для пошуку шляхів у мережі"""

    def __init__(self, grid: MoscowPowerGrid):
        self.grid = grid
        self.graph = grid.graph

    def dfs(self, start: str, end: str) -> Tuple[List[str], Dict]:
        """
        Алгоритм пошуку в глибину (DFS)
        Знаходить шлях, досліджуючи якомога далі кожну гілку перед поверненням
        """
        visited = set()
        path = []
        stats = {"nodes_visited": 0, "edges_explored": 0}

        def dfs_recursive(node, target, current_path):
            visited.add(node)
            current_path.append(node)
            stats["nodes_visited"] += 1

            if node == target:
                return list(current_path)

            for neighbor in self.graph.neighbors(node):
                stats["edges_explored"] += 1
                if neighbor not in visited:
                    result = dfs_recursive(neighbor, target, current_path)
                    if result:
                        return result

            current_path.pop()
            return None

        found_path = dfs_recursive(start, end, path)
        stats["path_found"] = found_path is not None
        stats["path_length"] = len(found_path) if found_path else 0

        return found_path if found_path else [], stats

    def bfs(self, start: str, end: str) -> Tuple[List[str], Dict]:
        """
        Алгоритм пошуку в ширину (BFS)
        Знаходить найкоротший шлях, досліджуючи всіх сусідів на одному рівні
        """
        visited = {start}
        queue = deque([(start, [start])])
        stats = {"nodes_visited": 0, "edges_explored": 0}

        while queue:
            node, path = queue.popleft()
            stats["nodes_visited"] += 1

            if node == end:
                stats["path_found"] = True
                stats["path_length"] = len(path)
                return path, stats

            for neighbor in self.graph.neighbors(node):
                stats["edges_explored"] += 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        stats["path_found"] = False
        stats["path_length"] = 0
        return [], stats

    def dijkstra(self, start: str, end: str = None) -> Tuple[Dict, Dict]:
        """
        Алгоритм Дейкстри для знаходження найкоротших шляхів
        Враховує ваги ребер (довжину ліній передачі)
        Якщо end = None, знаходить найкоротші шляхи до всіх вершин
        """
        distances = {node: float('inf') for node in self.graph.nodes()}
        distances[start] = 0
        previous = {node: None for node in self.graph.nodes()}
        visited = set()
        stats = {"nodes_visited": 0, "edges_explored": 0}

        # Мінімальна черга пріоритету
        pq = [(0, start)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)
            stats["nodes_visited"] += 1

            # Пропустити, якщо вже відвідано
            if current_node in visited:
                continue

            visited.add(current_node)

            # Якщо знаходимо конкретний вузол, можемо зупинитися
            if end and current_node == end:
                break

            # Розслабити сусідні вузли
            for neighbor in self.graph.neighbors(current_node):
                stats["edges_explored"] += 1
                edge_weight = self.graph[current_node][neighbor]['weight']
                new_distance = current_distance + edge_weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))

        # Побудувати шляхи
        paths = {}
        for node in self.graph.nodes():
            if distances[node] != float('inf'):
                path = []
                current = node
                while current is not None:
                    path.append(current)
                    current = previous[current]
                paths[node] = path[::-1]
            else:
                paths[node] = []

        return distances, paths, stats, previous

    def dijkstra_single_path(self, start: str, end: str) -> Tuple[List[str], float, Dict]:
        """
        Знайти найкоротший шлях від start до end використовуючи алгоритм Дейкстри
        """
        distances, paths, stats, _ = self.dijkstra(start, end)

        if paths[end]:
            return paths[end], distances[end], stats
        else:
            return [], float('inf'), stats

    def find_critical_nodes(self) -> List[Tuple[str, int]]:
        """
        Знайти критичні вузли (точки зчленування)
        Це найважливіші підстанції для контролю
        """
        articulation_points = list(nx.articulation_points(self.graph))

        # Сортувати за степенем (кількість зв'язків)
        critical = [(node, self.graph.degree(node)) for node in articulation_points]
        critical.sort(key=lambda x: x[1], reverse=True)

        return critical

    def find_minimum_shutdown_strategy(self, max_stations: int = 3) -> Dict:
        """
        Знайти стратегію для відключення максимальної кількості електростанцій
        з мінімальними ресурсами
        """
        critical_nodes = self.find_critical_nodes()

        result = {
            "critical_nodes": critical_nodes,
            "strategy": [],
            "affected_stations": set(),
            "total_capacity_affected_mw": 0,
        }

        if not critical_nodes:
            return result

        # Імітувати вимкнення критичних вузлів по одному
        temp_graph = self.graph.copy()

        for i, (node, degree) in enumerate(critical_nodes[:max_stations]):
            station = self.grid.substations[node]
            temp_graph.remove_node(node)

            # Знайти всі розділені компоненти
            components = list(nx.connected_components(temp_graph))
            affected = []
            total_capacity = 0

            for component in components:
                # Порахувати підстанції в кожній компоненті
                capacity = sum(self.grid.substations[s].capacity_mw for s in component)
                affected.append({
                    "stations": list(component),
                    "capacity_mw": capacity,
                    "count": len(component)
                })
                total_capacity += capacity

            result["strategy"].append({
                "step": i + 1,
                "shutdown_station": node,
                "station_name": station.name,
                "voltage": station.voltage,
                "num_connections": degree,
                "disconnected_components": affected,
                "total_affected_capacity": total_capacity
            })

        return result

    def compare_algorithms(self, start: str, end: str) -> Dict:
        """Порівняти DFS, BFS та Дейкстри на одній і тій самій задачі пошуку шляху"""

        dfs_path, dfs_stats = self.dfs(start, end)
        bfs_path, bfs_stats = self.bfs(start, end)
        dijkstra_path, dijkstra_distance, dijkstra_stats = self.dijkstra_single_path(start, end)

        start_station = self.grid.substations[start].name
        end_station = self.grid.substations[end].name

        # Обчислити загальну відстань для DFS та BFS
        dfs_distance = sum(self.graph[dfs_path[i]][dfs_path[i+1]]['weight']
                           for i in range(len(dfs_path)-1)) if len(dfs_path) > 1 else 0
        bfs_distance = sum(self.graph[bfs_path[i]][bfs_path[i+1]]['weight']
                           for i in range(len(bfs_path)-1)) if len(bfs_path) > 1 else 0

        comparison = {
            "start": start,
            "end": end,
            "start_name": start_station,
            "end_name": end_station,
            "dfs": {
                "path": dfs_path,
                "path_names": [self.grid.substations[s].name for s in dfs_path],
                "distance": dfs_distance,
                "stats": dfs_stats,
            },
            "bfs": {
                "path": bfs_path,
                "path_names": [self.grid.substations[s].name for s in bfs_path],
                "distance": bfs_distance,
                "stats": bfs_stats,
            },
            "dijkstra": {
                "path": dijkstra_path,
                "path_names": [self.grid.substations[s].name for s in dijkstra_path],
                "distance": dijkstra_distance,
                "stats": dijkstra_stats,
            }
        }

        return comparison

def print_comparison_report(comparison: Dict):
    """Надрукувати детальний звіт порівняння DFS, BFS та Дейкстри"""

    print("\n" + "="*80)
    print("ЗВІТ ПОРІВНЯННЯ DFS, BFS ТА ДЕЙКСТРИ".center(80))
    print("="*80)
    print(f"\nЗавдання: Знайти шлях від {comparison['start_name']} до {comparison['end_name']}")
    print(f"({comparison['start']} → {comparison['end']})")

    # Результати DFS
    print("\n" + "-"*80)
    print("ПОШУК В ГЛИБИНУ (DFS)")
    print("-"*80)
    print(f"Шлях знайдено: {comparison['dfs']['stats']['path_found']}")
    print(f"Довжина шляху: {len(comparison['dfs']['path'])} підстанцій")
    print(f"Загальна відстань: {comparison['dfs']['distance']:.1f} км")
    print(f"Вузлів відвідано: {comparison['dfs']['stats']['nodes_visited']}")
    print(f"Ребер досліджено: {comparison['dfs']['stats']['edges_explored']}")

    if comparison['dfs']['path']:
        print("\nШлях (DFS):")
        for i, station_id in enumerate(comparison['dfs']['path']):
            print(f"  {i+1}. {comparison['dfs']['path_names'][i]} ({station_id})")

    # Результати BFS
    print("\n" + "-"*80)
    print("ПОШУК В ШИРИНУ (BFS)")
    print("-"*80)
    print(f"Шлях знайдено: {comparison['bfs']['stats']['path_found']}")
    print(f"Довжина шляху: {len(comparison['bfs']['path'])} підстанцій")
    print(f"Загальна відстань: {comparison['bfs']['distance']:.1f} км")
    print(f"Вузлів відвідано: {comparison['bfs']['stats']['nodes_visited']}")
    print(f"Ребер досліджено: {comparison['bfs']['stats']['edges_explored']}")

    if comparison['bfs']['path']:
        print("\nШлях (BFS):")
        for i, station_id in enumerate(comparison['bfs']['path']):
            print(f"  {i+1}. {comparison['bfs']['path_names'][i]} ({station_id})")

    # Результати Дейкстри
    print("\n" + "-"*80)
    print("АЛГОРИТМ ДЕЙКСТРИ (НАЙОПТИМАЛЬНІШИЙ ШЛЯХ)")
    print("-"*80)
    print(f"Шлях знайдено: {len(comparison['dijkstra']['path']) > 0}")
    print(f"Довжина шляху: {len(comparison['dijkstra']['path'])} підстанцій")
    print(f"Загальна відстань: {comparison['dijkstra']['distance']:.1f} км")
    print(f"Вузлів відвідано: {comparison['dijkstra']['stats']['nodes_visited']}")
    print(f"Ребер досліджено: {comparison['dijkstra']['stats']['edges_explored']}")

    if comparison['dijkstra']['path']:
        print("\nОптимальний шлях (Дейкстра):")
        for i, station_id in enumerate(comparison['dijkstra']['path']):
            print(f"  {i+1}. {comparison['dijkstra']['path_names'][i]} ({station_id})")

    # Аналіз
    print("\n" + "-"*80)
    print("АНАЛІЗ І ПОРІВНЯННЯ")
    print("-"*80)

    print(f"\nРізниця в довжині шляху (кількість підстанцій):")
    print(f"  DFS: {len(comparison['dfs']['path'])} підстанцій")
    print(f"  BFS: {len(comparison['bfs']['path'])} підстанцій")
    print(f"  Дейкстра: {len(comparison['dijkstra']['path'])} підстанцій")

    print(f"\nРізниця в дистанції (км):")
    print(f"  DFS: {comparison['dfs']['distance']:.1f} км")
    print(f"  BFS: {comparison['bfs']['distance']:.1f} км")
    print(f"  Дейкстра: {comparison['dijkstra']['distance']:.1f} км")

    print(f"\n✓ Дейкстра знайшов найкоротший шлях: {comparison['dijkstra']['distance']:.1f} км")

    print("\nКлючові різниці:")
    print(f"  • DFS: Не гарантує оптимальність, залежить від порядку дослідження")
    print(f"  • BFS: Знаходить найкоротший по кількості вершин, але не по вазі")
    print(f"  • Дейкстра: ЗАВЖДИ знаходить оптимальний шлях за загальною вагою")

def print_dijkstra_all_paths(analyzer: PathFindingAnalyzer):
    """Надрукувати найкоротші шляхи від однієї вершини до всіх інших"""

    print("\n" + "="*80)
    print("ДЕЙКСТРА: НАЙКОРОТШІ ШЛЯХИ ВІД SS_1 (ЛУЖНИКИ) ДО ВСІХ ІНШИХ ПІДСТАНЦІЙ".center(80))
    print("="*80)

    start_station = "SS_1"
    distances, paths, stats, _ = analyzer.dijkstra(start_station)

    # Створити список для сортування
    results = []
    for node in sorted(distances.keys()):
        if node != start_station:
            distance = distances[node]
            path = paths[node]
            station_name = analyzer.grid.substations[node].name
            results.append((node, station_name, distance, path))

    # Сортувати за відстанню
    results.sort(key=lambda x: x[2])

    print(f"\nВихідна станція: {analyzer.grid.substations[start_station].name} ({start_station})\n")

    for i, (node, name, distance, path) in enumerate(results, 1):
        print(f"{i}. До {name} ({node})")
        print(f"   Відстань: {distance:.1f} км")
        print(f"   Шлях ({len(path)} станцій):")

        path_str = " → ".join([analyzer.grid.substations[s].name for s in path])
        if len(path_str) > 75:
            # Розбити довгий шлях на кілька рядків
            path_display = ""
            current_line = ""
            stations = [analyzer.grid.substations[s].name for s in path]
            for j, station in enumerate(stations):
                if j < len(stations) - 1:
                    test_line = current_line + station + " → "
                else:
                    test_line = current_line + station

                if len(test_line) > 70:
                    path_display += "     " + current_line + "\n"
                    current_line = station + (" → " if j < len(stations) - 1 else "")
                else:
                    current_line = test_line

            path_display += "     " + current_line
            print(path_display)
        else:
            print(f"     {path_str}")

        print()

    print(f"Загальна статистика пошуку:")
    print(f"  Вузлів відвідано: {stats['nodes_visited']}")
    print(f"  Ребер досліджено: {stats['edges_explored']}")

def main():
    """Головна функція"""

    print("\n" + "="*80)
    print("ЕНЕРГОМЕРЕЖА МОСКВИ - АНАЛІЗ ПОШУКУ ШЛЯХІВ".center(80))
    print("="*80)

    # Ініціалізувати мережу
    grid = MoscowPowerGrid()
    analyzer = PathFindingAnalyzer(grid)

    # Тестові випадки для пошуку шляху
    test_cases = [
        ("SS_6", "SS_7"),  # Зеленоград до Домодєдово
        ("SS_2", "SS_9"),  # Одинцово до Косино
        ("SS_1", "SS_5"),  # Лужники до Балашихи
    ]

    print("\n1. ПОРІВНЯННЯ АЛГОРИТМІВ DFS, BFS ТА ДЕЙКСТРИ")
    print("="*80)

    for start, end in test_cases:
        comparison = analyzer.compare_algorithms(start, end)
        print_comparison_report(comparison)

    # Дейкстра: найкоротші шляхи від однієї вершини до всіх інших
    print("\n\n2. АЛГОРИТМ ДЕЙКСТРИ: НАЙКОРОТШІ ШЛЯХИ ВІД ОДНІЄЇ ВЕРШИНИ")
    print("="*80)

    print_dijkstra_all_paths(analyzer)

    # Резюме
    print("\n" + "="*80)
    print("РЕЗЮМЕ І ВИСНОВКИ".center(80))
    print("="*80)
    print("""
КЛЮЧОВІ ЗНАХІДКИ:

1. DFS vs BFS vs Дейкстра:
   ✓ DFS: Не враховує ваги, може знайти довгі шляхи
   ✓ BFS: Найкоротший по кількості вершин, але не по вазі ребер
   ✓ Дейкстра: ЗАВЖДИ знаходить оптимальний шлях за загальною вагою

2. Практичне застосування для енергомережи:
   ✓ Дейкстра ідеальна для планування маршрутів електроенергії
   ✓ Враховує реальну відстань (довжину ліній) між підстанціями
   ✓ Мінімізує втрати в лініях передачі
   ✓ Оптимізує використання інфраструктури

3. Обчислювальна складність:
   ✓ DFS: O(V + E) - лінійна за кількістю вершин і ребер
   ✓ BFS: O(V + E) - лінійна за кількістю вершин і ребер
   ✓ Дейкстра: O((V + E) log V) - логарифмічна за кількістю вершин

4. Коли використовувати:
   ✓ DFS: Виявлення циклів, топологічне сортування
   ✓ BFS: Найкоротший шлях у невзважених графах
   ✓ Дейскстра: Найкоротший шлях у взважених графах (без негативних ваг)

5. Ваги в енергомережі:
   ✓ Довжина ліній передачі - основна вага в нашій моделі
   ✓ Можна додати інші ваги: вартість електроенергії, опір лінії, надійність
   ✓ Дейкстра легко адаптується до різних критеріїв оптимізації
    """)

if __name__ == "__main__":
    main()
