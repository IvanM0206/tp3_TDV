from typing import List, Dict
from nearest_neighbor import nearest_neighbor_algorithm
from utils import cost_of_solution, calculate_probability_to_visit_neighbor, Ant
import random

def create_initial_pheromonal_trail(distance_matrix: List[List[int]], cant_ants: int):
    
    res: List[List[int]] = []

    nearest_neighbor_solution = nearest_neighbor_algorithm(distance_matrix)
    nearest_neighbor_cost = cost_of_solution(nearest_neighbor_solution)

    for node_i in range(distance_matrix):
    
        res.append([])
    
        for node_j in range(distance_matrix[0]):
    
            res[node_i][node_j]  = cant_ants/nearest_neighbor_cost
    
    return res

# Las hormigas inician siempre desde el nodo 0

def establish_path_of_ant(ant: Ant, distance_matrix: List[List[int]], pheromonal_values: List[List[float]], alfa, beta):

    ant.add_node_to_memory(0)
    node_to_analize: int = 0

    probabilty_values_for_neighbor: Dict[int, float] = dict()

    for node in range(1, distance_matrix):
    
        for neighbor in range(distance_matrix[node_to_analize]):
            
            probabilty_values_for_neighbor[neighbor] = calculate_probability_to_visit_neighbor(ant, node, neighbor, pheromonal_values, alfa, beta)

        random_value: float = random.uniform(0, 1)
        # aplicar regla probabilistica




def establish_all_paths_for_ants(cant_ants: int, alfa, beta):

    for ant_number in range(1, cant_ants+1):
        
        ant_temp = Ant(ant_number)
        establish_path_of_ant(ant_temp, alfa, beta)

        #FALTA