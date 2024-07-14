from typing import List
import random
from graph_creator import create_graph
import statistics

BIG_NUMBER = 1e100


def travel_distance(graph: List[List[int]], tour: List[int]) -> int:
    i = 0
    total_distance = 0
    while i < len(tour) - 1:
        total_distance += graph[tour[i]][tour[i + 1]]
        i += 1
    total_distance += graph[tour[len(tour) - 1]][tour[0]]
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
    tour = [v]
    not_visited = list(range(len(graph)))
    not_visited.remove(v)
    next_node = 0

    while len(tour) != len(graph):
        min_distance = BIG_NUMBER
        for neighbor in not_visited:
            if graph[v][neighbor] < min_distance:
                next_node = neighbor
                min_distance = graph[v][neighbor]
        tour.append(next_node)
        not_visited.remove(next_node)
        v = neighbor

    return tour


def mean_neighbor(v: int, graph: List[List[int]]) -> List[int]:
    tour = [v]
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

    while len(tour) != len(graph):
        min_diff = BIG_NUMBER
        for neighbor in not_visited:
            diff = abs(mean_distance - graph[v][neighbor])
            if diff < min_diff:
                next_node = neighbor
                min_diff = diff
        tour.append(next_node)
        not_visited.remove(next_node)
        v = neighbor

    return tour


def greedy_min_edges(graph: List[List[int]]) -> List[int]:
    tour = []
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
        if u not in tour and v not in tour:
            tour.append(u)
            tour.append(v)
            not_visited.remove(u)
            not_visited.remove(v)

    if len(tour) < n:
        tour.append(not_visited[0])

    return tour


def swap(graph: List[List[int]], tour: List[List[int]]) -> List[int]:
    swap = None
    best_improvement = 0
    n = len(tour)

    # Almacena el siguiente y anterior nodo de cada nodo en el tour
    next_node = [0] * n
    prev_node = [0] * n

    for i in range(n):
        if i != n - 1:
            next_node[i] = tour[i + 1]
        else:
            next_node[i] = tour[0]

        if i != 0:
            prev_node[i] = tour[i - 1]
        else:
            prev_node[i] = tour[n - 1]

    # Para todo par de nodos en el camino
    for i in range(n - 1):
        for j in range(i, n):
            # Condición de mejora
            if next_node[i] == tour[j]:
                current_distance = (
                    graph[prev_node[i]][tour[i]]
                    + graph[tour[i]][tour[j]]
                    + graph[tour[j]][next_node[j]]
                )
                new_distance = (
                    graph[prev_node[i]][tour[j]]
                    + graph[tour[j]][tour[i]]
                    + graph[tour[i]][next_node[j]]
                )
            elif next_node[j] == tour[i]:
                current_distance = (
                    graph[prev_node[j]][tour[j]]
                    + graph[tour[j]][tour[i]]
                    + graph[tour[i]][next_node[i]]
                )
                new_distance = (
                    graph[prev_node[j]][tour[i]]
                    + graph[tour[i]][tour[j]]
                    + graph[tour[j]][next_node[i]]
                )

            else:
                current_distance = (
                    graph[prev_node[i]][tour[i]]
                    + graph[tour[i]][next_node[i]]
                    + graph[prev_node[j]][tour[j]]
                    + graph[tour[j]][next_node[j]]
                )
                new_distance = (
                    graph[prev_node[i]][tour[j]]
                    + graph[tour[j]][next_node[i]]
                    + graph[prev_node[j]][tour[i]]
                    + graph[tour[i]][next_node[j]]
                )

            improvement = current_distance - new_distance

            is_better = improvement > 0 and improvement > best_improvement

            if i != j and is_better:
                best_improvement = improvement
                swap = [i, j]

    # Ejecutar swap
    if swap is not None:
        temp = tour[swap[0]]
        tour[swap[0]] = tour[swap[1]]
        tour[swap[1]] = temp

    return tour


def swap_continuous(graph: List[List[int]], tour: List[List[int]]) -> List[int]:
    stop = False
    count = 0
    total_improvement = 0
    prev_tour = tour.copy()

    while not stop:
        print(tour)
        stop = True
        count += 1
        tour = swap(graph, tour)
        new_improvement = travel_distance(graph, prev_tour) - travel_distance(
            graph, tour
        )
        print("IMPROVEMENT:", new_improvement)
        if new_improvement > 0:
            stop = False
            total_improvement += new_improvement
            prev_tour = tour.copy()

    print(count, "iteraciones completadas")

    return tour


def relocate(graph: List[List[int]], tour: List[List[int]]) -> List[int]:
    n = len(tour)
    best_improvement = 0
    relocation = None

    # Almacena el siguiente y anterior nodo de cada nodo en el tour
    next_node = [0] * n
    prev_node = [0] * n

    for i in range(n):
        if i != n - 1:
            next_node[i] = tour[i + 1]
        else:
            next_node[i] = tour[0]

        if i != 0:
            prev_node[i] = tour[i - 1]
        else:
            prev_node[i] = tour[n - 1]

    # Para todo par de nodos en el camino
    for i in range(n):
        for j in range(n):
            # Condición de mejora

            current_distance = (
                graph[prev_node[j]][tour[j]]
                + graph[prev_node[i]][tour[i]]
                + graph[tour[i]][next_node[i]]
            )

            new_distance = (
                graph[prev_node[i]][next_node[i]]
                + graph[prev_node[j]][tour[i]]
                + graph[tour[i]][tour[j]]
            )

            improvement = current_distance - new_distance

            is_better = improvement > 0 and improvement > best_improvement

            if i != j and is_better:
                best_improvement = improvement
                relocation = [i, j]

    # Ejecutar relocate
    if relocation is not None:
        target = tour[relocation[0]]
        tour.pop(relocation[0])
        tour.insert(relocation[1], target)

    return tour


def relocate_continuous(graph: List[List[int]], tour: List[List[int]]) -> List[int]:
    stop = False
    count = 0
    total_improvement = 0
    prev_tour = tour.copy()

    while not stop:
        stop = True
        count += 1
        tour = relocate(graph, tour)
        new_improvement = travel_distance(graph, prev_tour) - travel_distance(
            graph, tour
        )
        print("IMPROVEMENT:", new_improvement)
        if new_improvement > 0:
            stop = False
            total_improvement += new_improvement
            prev_tour = tour.copy()

    print(count, "iteraciones completadas")

    return prev_tour


def two_opt(graph: List[List[int]], tour: List[List[int]]) -> List[int]:
    n = len(tour)
    s = [0] * n
    two_change = None
    best_improvement = 0

    for i in range(1, n):
        s[i] = s[i - 1] + graph[tour[i - 1]][tour[i]]

    rev_s = [0] * n
    for i in range(1, n - 1):
        rev_s[n - i - 1] = rev_s[n - i] + graph[tour[n - i]][tour[n - i - 1]]

    for i in range(n - 3):
        j = i + 1
        for k in range(i + 2, n - 1):
            l = k + 1

            different = i != j != k != l

            current_distance = (
                graph[tour[i]][tour[j]] + s[k] - s[j] + graph[tour[k]][tour[l]]
            )

            new_distance = (
                graph[tour[i]][tour[k]] + rev_s[j] - rev_s[k] + graph[tour[j]][tour[l]]
            )

            improvement = current_distance - new_distance

            is_better = improvement > 0 and improvement > best_improvement

            if different and is_better:
                best_improvement = improvement
                two_change = [j, k]

    if two_change is not None:
        tour = (
            tour[0 : two_change[0]]
            + tour[two_change[0] : two_change[1] + 1][::-1]
            + tour[two_change[1] + 1 :]
        )
    return tour


def two_opt_continuous(graph: List[List[int]], tour: List[List[int]]) -> List[int]:
    stop = False
    count = 0
    total_improvement = 0
    prev_tour = tour.copy()

    while not stop:
        print(tour)
        stop = True
        count += 1
        tour = two_opt(graph, tour)
        new_improvement = travel_distance(graph, prev_tour) - travel_distance(
            graph, tour
        )

        if new_improvement > 0:
            stop = False
            total_improvement += new_improvement
            prev_tour = tour.copy()

    print(count, "iteraciones completadas")
    print("IMPROVEMENT:", total_improvement)

    return prev_tour


graph = create_graph(18)
tour = nearest_neighbor(cheapest_first_node(graph), graph)
# tour = mean_neighbor(cheapest_first_node(graph), graph)
# tour = greedy_min_edges(graph)
print(tour)
print("TRAVEL DISTANCE:", travel_distance(graph, tour))

# tour = relocate_continuous(graph, tour)
# tour = swap_continuous(graph, tour)
tour = two_opt_continuous(graph, tour)
print(tour)
print("TRAVEL DISTANCE:", travel_distance(graph, tour))
