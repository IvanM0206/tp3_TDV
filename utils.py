from typing import List
from utils import Ant

def cost_of_solution(solution: List[int], distance_matrix: List[List[int]]):

    cost: float = 0
    i: int = 0
    
    while i < len(solution)-1:

        cost += distance_matrix[i][i+1]
        i += 1
    
    return cost

def calculate_probability_to_visit_neighbor(ant: Ant, node: int, neighbor: int, solution: List[int], pheromonal_values: List[List[float]], distance_matrix: List[List[int]], alfa, beta):

    inverse_distance_neighbor: float = 1/distance_matrix[node][neighbor]
    value_of_denominator: float = (pheromonal_values[node][neighbor]**alfa) * (inverse_distance_neighbor**beta)
    value_of_numerator = 0
    
    for neighbor_j in range(distance_matrix[node]):

        if not(neighbor_j in ant.get_memory()):
            inverse_distance_neighbor_j = 1/distance_matrix[node][neighbor_j]
            value_to_add = (pheromonal_values[node][neighbor_j]**alfa) * (inverse_distance_neighbor_j**beta)
            value_of_numerator += value_to_add
    
    return value_of_denominator/value_of_numerator

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