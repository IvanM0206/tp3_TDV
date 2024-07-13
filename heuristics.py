from typing import List
import random
from graph_creator import create_graph
import statistics

BIG_NUMBER = 1e100


def travel_distance(graph: List[List[int]], path: List[int]) -> int:
    i = 0
    j = 1
    total_distance = 0
    while j < len(path):
        total_distance += graph[path[i]][path[j]]
        i += 1
        j += 1
    total_distance += graph[path[len(path) - 1]][path[0]]
    return total_distance


def random_first_node(graph: List[List[int]]) -> int:
    first_node = random.randint(0, len(graph) - 1)
    return first_node


def cheapest_first_node(graph: List[List[int]]) -> int:
    first_node = 0
    min_node_distance = BIG_NUMBER
    for node in range(len(graph)):
        for neighbor in range(len(graph)):
            if graph[node][neighbor] < min_node_distance:
                min_node_distance = graph[node][neighbor]
                first_node = node
    return first_node


def nearest_neighbor(v: int, graph: List[List[int]]) -> List[int]:
    path = [v]
    not_visited = list(range(len(graph)))
    not_visited.remove(v)
    next_node = 0

    while len(path) != len(graph):
        min_distance = BIG_NUMBER
        for neighbor in not_visited:
            if graph[v][neighbor] < min_distance:
                next_node = neighbor
                min_distance = graph[v][neighbor]
        path.append(next_node)
        not_visited.remove(next_node)
        v = neighbor

    return path


def mean_neighbor(v: int, graph: List[List[int]]) -> List[int]:
    path = [v]
    not_visited = list(range(len(graph)))
    not_visited.remove(v)
    next_node = 0

    # Encontrar la distancia promedio (asumiendo que ninguna es infinita más que las propias, ya que rompería la lógica)
    mean_distances = []
    i = 0
    for node_distances in graph:
        node_distances_without_self = node_distances.copy()
        node_distances_without_self.pop(i)
        mean_distances.append(statistics.mean(node_distances_without_self))
        i += 1

    mean_distance = statistics.mean(mean_distances)
    print(mean_distance)

    while len(path) != len(graph):
        min_diff = BIG_NUMBER
        for neighbor in not_visited:
            diff = abs(mean_distance - graph[v][neighbor])
            if diff < min_diff:
                next_node = neighbor
                min_diff = diff
        path.append(next_node)
        not_visited.remove(next_node)
        v = neighbor

    return path


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1
            return True
        return False


def greedy_min_edges_agm(graph: List[List[int]]) -> List[int]:
    n = len(graph)
    edges = []

    # Crear una lista de todas las aristas con sus pesos
    for i in range(n):
        for j in range(n):
            if i != j:
                edges.append((graph[i][j], i, j))

    # Ordenar las aristas por peso
    edges.sort()

    edges_path = []
    in_degree = [0] * n
    out_degree = [0] * n
    union_find = UnionFind(n)
    endpoints = {}

    for weight, u, v in edges:
        # Verificar si la arista (u, v) puede ser agregada sin formar un ciclo y sin romper la estructura hamiltoniana
        if out_degree[u] == 0 and in_degree[v] == 0:
            root_u = union_find.find(u)
            root_v = union_find.find(v)

            if root_u != root_v:
                # Verificar si agregar esta arista cerrará un subciclo prematuro
                if (
                    u in endpoints
                    and v in endpoints
                    and union_find.find(endpoints[u]) == union_find.find(endpoints[v])
                ):
                    continue

                edges_path.append((u, v))
                out_degree[u] += 1
                in_degree[v] += 1
                union_find.union(u, v)

                # Actualizar las puntas de los caminos
                if u in endpoints:
                    start = endpoints.pop(u)
                else:
                    start = u

                if v in endpoints:
                    end = endpoints.pop(v)
                else:
                    end = v

                if start != end:
                    endpoints[start] = end
                    endpoints[end] = start

                # Verificar si se ha completado el camino hamiltoniano
                if len(edges_path) == n - 1:
                    break

    # Convertir el conjunto de aristas en un camino
    for u in range(n):
        if in_degree[u] == 0:
            start_node = u

    path = []
    current_node = start_node
    visited = set()
    while len(path) < n:
        path.append(current_node)
        visited.add(current_node)
        for u, v in edges_path:
            if u == current_node:
                next_node = v

        current_node = next_node

    return path


def greedy_min_edges(graph: List[List[int]]) -> List[int]:
    path = []
    n = len(graph)
    edges = []
    not_visited = list(range(n))

    # Crear una lista de todas las aristas con sus pesos y sus nodos extremos
    for i in range(n):
        for j in range(n):
            if i != j:
                edges.append((graph[i][j], i, j))

    edges.sort()

    for distance, u, v in edges:
        if u not in path and v not in path:
            path.append(u)
            path.append(v)
            not_visited.remove(u)
            not_visited.remove(v)

    if len(path) < n:
        path.append(not_visited[0])

    return path


def swap(graph: List[List[int]], path: List[List[int]]) -> List[int]:
    swap = None
    best_improvement = 0
    n = len(path)

    # Almacena el siguiente y anterior nodo de cada nodo en el tour
    next_node = [0] * n
    prev_node = [0] * n

    for i in range(n):
        if i != n - 1:
            next_node[i] = path[i + 1]
        else:
            next_node[i] = path[0]

        if i != 0:
            prev_node[i] = path[i - 1]
        else:
            prev_node[i] = path[n - 1]

    # Para todo par de nodos en el camino
    for i in range(n):
        for j in range(n):
            # Condición de mejora
            current_distance = (
                graph[prev_node[i]][path[i]]
                + graph[path[i]][next_node[i]]
                + graph[prev_node[j]][path[j]]
                + graph[path[j]][next_node[j]]
            )
            new_distance = (
                graph[prev_node[i]][path[j]]
                + graph[path[j]][next_node[i]]
                + graph[prev_node[j]][path[i]]
                + graph[path[i]][next_node[j]]
            )

            improvement = current_distance - new_distance

            is_better = improvement > 0 and improvement > best_improvement

            if i != j and is_better:
                best_improvement = improvement
                swap = [i, j]

    # Ejecutar swap
    if swap is not None:
        temp = path[swap[0]]
        path[swap[0]] = path[swap[1]]
        path[swap[1]] = temp

    return path


def swap_continuous(graph: List[List[int]], path: List[List[int]]) -> List[int]:
    stop = False
    count = 0
    prev_improvement = 0
    prev_path = path.copy()

    while not stop:
        print(path)
        stop = True
        count += 1
        prev_path = path.copy()
        path = swap(graph, path)
        new_improvement = travel_distance(graph, prev_path) - travel_distance(
            graph, path
        )
        print("IMPROVEMENT:", new_improvement)
        if new_improvement > prev_improvement:
            stop = False
            prev_improvement = new_improvement

    print(count, "iteraciones completadas")

    return path


graph = create_graph(0)
print(graph)
path = nearest_neighbor(cheapest_first_node(graph), graph)
path = mean_neighbor(cheapest_first_node(graph), graph)
path = greedy_min_edges_agm(graph)
path = greedy_min_edges(graph)
print(path)
print("TRAVEL DISTANCE:", travel_distance(graph, path))
print(len(path))

path = swap_continuous(graph, path)
print(path)
print("TRAVEL DISTANCE:", travel_distance(graph, path))
