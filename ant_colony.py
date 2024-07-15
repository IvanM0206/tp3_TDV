from typing import List, Dict
import random
from heuristics import nearest_neighbor, travel_distance


class Ant:

    def __init__(self, number) -> None:
        self.number = number
        self.memory: List[int] = []

    def add_node_to_memory(self, node):
        self.memory.append(node)

    def erase_memory(self):
        self.memory = []

    def get_memory(self):
        return self.memory


def calculate_probability_to_visit_neighbor(
    ant: Ant,
    node: int,
    neighbor: int,
    solution: List[int],
    pheromonal_values: List[List[float]],
    distance_matrix: List[List[int]],
    alfa,
    beta,
):

    inverse_distance_neighbor: float = 1 / distance_matrix[node][neighbor]
    value_of_denominator: float = (pheromonal_values[node][neighbor] ** alfa) * (
        inverse_distance_neighbor**beta
    )
    value_of_numerator = 0

    for neighbor_j in range(distance_matrix[node]):

        if not (neighbor_j in ant.get_memory()):
            inverse_distance_neighbor_j = 1 / distance_matrix[node][neighbor_j]
            value_to_add = (pheromonal_values[node][neighbor_j] ** alfa) * (
                inverse_distance_neighbor_j**beta
            )
            value_of_numerator += value_to_add

    return value_of_denominator / value_of_numerator


def create_initial_pheromonal_trail(distance_matrix: List[List[int]], cant_ants: int):

    res: List[List[int]] = []

    nearest_neighbor_solution = nearest_neighbor(distance_matrix)
    nearest_neighbor_cost = travel_distance(nearest_neighbor_solution)

    for node_i in range(distance_matrix):

        res.append([])

        for node_j in range(distance_matrix[0]):

            res[node_i][node_j] = cant_ants / nearest_neighbor_cost

    return res


# Las hormigas inician siempre desde el nodo 0


def establish_path_of_ant(
    ant: Ant,
    distance_matrix: List[List[int]],
    pheromonal_values: List[List[float]],
    alfa,
    beta,
):

    ant.add_node_to_memory(0)
    node_to_analize: int = 0

    probabilty_values_for_neighbor: Dict[int, float] = dict()

    for node in range(1, distance_matrix):

        for neighbor in range(distance_matrix[node_to_analize]):

            probabilty_values_for_neighbor[neighbor] = (
                calculate_probability_to_visit_neighbor(
                    ant, node, neighbor, pheromonal_values, alfa, beta
                )
            )

        random_value: float = random.uniform(0, 1)
        # aplicar regla probabilistica


def establish_all_paths_for_ants(cant_ants: int, alfa, beta):

    for ant_number in range(1, cant_ants + 1):

        ant_temp = Ant(ant_number)
        establish_path_of_ant(ant_temp, alfa, beta)

        # FALTA
