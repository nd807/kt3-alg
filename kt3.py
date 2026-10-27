import heapq


class TransportGraph:
    def __init__(self, directed=False):
        self.graph = {}
        self.routes = []
        self.directed = directed

    def add_station(self, name):
        if name not in self.graph:
            self.graph[name] = []

    def add_route(self, source, target, weight):
        self.add_station(source)
        self.add_station(target)
        self.graph[source].append((target, weight))
        if not self.directed:
            self.graph[target].append((source, weight))
        self.routes.append((source, target, weight))

    def shortest_path_Dijkstra(self, start):
        if start not in self.graph:
            raise ValueError("Станция не найдена")
        if any(weight < 0 for source, target, weight in self.routes):
            raise ValueError("Дейкстра не работает с отрицательными весами")
        distance = dict.fromkeys(self.graph, float("inf"))
        distance[start] = 0
        queue = [(0, start)]
        while queue:
            current_distance, station = heapq.heappop(queue)
            if current_distance > distance[station]:
                continue
            for neighbor, weight in self.graph[station]:
                new_distance = current_distance + weight
                if new_distance < distance[neighbor]:
                    distance[neighbor] = new_distance
                    heapq.heappush(queue, (new_distance, neighbor))
        return distance

    def shortest_path_BellmanFord(self, start):
        if start not in self.graph:
            raise ValueError("Станция не найдена")
        distance = dict.fromkeys(self.graph, float("inf"))
        distance[start] = 0
        for _ in range(len(self.graph) - 1):
            changed = False
            for station in self.graph:
                for neighbor, weight in self.graph[station]:
                    if distance[station] + weight < distance[neighbor]:
                        distance[neighbor] = distance[station] + weight
                        changed = True
            if not changed:
                break
        for station in self.graph:
            for neighbor, weight in self.graph[station]:
                if distance[station] + weight < distance[neighbor]:
                    raise ValueError("Обнаружен отрицательный цикл")
        return distance

    def all_pairs_shortest_paths_FloydWarshall(self):
        stations = list(self.graph)
        index = {station: i for i, station in enumerate(stations)}
        size = len(stations)
        distance = [[float("inf")] * size for _ in range(size)]
        for station in stations:
            i = index[station]
            distance[i][i] = 0
            for neighbor, weight in self.graph[station]:
                j = index[neighbor]
                distance[i][j] = min(distance[i][j], weight)
        for k in range(size):
            for i in range(size):
                for j in range(size):
                    distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
        if any(distance[i][i] < 0 for i in range(size)):
            raise ValueError("Обнаружен отрицательный цикл")
        return distance


class NetworkOptimizer:
    def __init__(self, graph):
        if graph.directed:
            raise ValueError("Для остовного дерева нужен неориентированный граф")
        self.graph = graph

    def minimum_spanning_tree_Kruskal(self):
        parent = {station: station for station in self.graph.graph}

        def find(station):
            while station != parent[station]:
                parent[station] = parent[parent[station]]
                station = parent[station]
            return station

        result = []
        total = 0
        for source, target, weight in sorted(self.graph.routes, key=lambda route: route[2]):
            first = find(source)
            second = find(target)
            if first != second:
                parent[first] = second
                result.append((source, target, weight))
                total += weight
        if self.graph.graph and len(result) != len(self.graph.graph) - 1:
            raise ValueError("Сеть не связна")
        return result, round(total, 10)

    def minimum_spanning_tree_Prim(self):
        if not self.graph.graph:
            return [], 0
        start = next(iter(self.graph.graph))
        visited = {start}
        queue = []
        for neighbor, weight in self.graph.graph[start]:
            heapq.heappush(queue, (weight, start, neighbor))
        result = []
        total = 0
        while queue:
            weight, source, target = heapq.heappop(queue)
            if target in visited:
                continue
            visited.add(target)
            result.append((source, target, weight))
            total += weight
            for neighbor, cost in self.graph.graph[target]:
                if neighbor not in visited:
                    heapq.heappush(queue, (cost, target, neighbor))
        if len(visited) != len(self.graph.graph):
            raise ValueError("Сеть не связна")
        return result, round(total, 10)


def main():
    stations = ["Центр. вокзал", "Пл. Ленина", "Автостанция-1", "Университет",
                "Вокзал-Северный", "Автостанция-2", "Парковая", "Портовая"]
    routes = [(0, 1, 1.2), (0, 2, 3.5), (0, 4, 4.0), (1, 2, 2.1),
              (1, 3, 0.8), (1, 5, 3.0), (1, 6, 1.5), (2, 5, 5.4),
              (2, 7, 4.2), (3, 4, 2.7), (3, 5, 1.9), (4, 6, 3.3),
              (4, 7, 6.0), (5, 6, 2.5)]
    graph = TransportGraph()
    for station in stations:
        graph.add_station(station)
    for source, target, weight in routes:
        graph.add_route(stations[source], stations[target], weight)
    for title, result in [("Дейкстра", graph.shortest_path_Dijkstra(stations[0])),
                          ("Беллман-Форд", graph.shortest_path_BellmanFord(stations[0]))]:
        print(title)
        for station, distance in result.items():
            print(station, ":", round(distance, 2))
    print("Флойд-Уоршелл. Порядок станций:", stations)
    for row in graph.all_pairs_shortest_paths_FloydWarshall():
        print([round(value, 2) for value in row])
    optimizer = NetworkOptimizer(graph)
    print("Крускал:", optimizer.minimum_spanning_tree_Kruskal())
    print("Прим:", optimizer.minimum_spanning_tree_Prim())
    bus = TransportGraph(directed=True)
    bus.add_route("A", "B", 4)
    bus.add_route("A", "C", 5)
    bus.add_route("B", "C", -2)
    print("Маршруты с отрицательным весом:", bus.shortest_path_BellmanFord("A"))
    bus.add_route("C", "B", 1)
    try:
        bus.shortest_path_BellmanFord("A")
    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()
