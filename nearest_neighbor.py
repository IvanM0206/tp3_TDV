from typing import List

# Se inicia siempre desde el nodo 0

def nearest_neighbor_algorithm(distance_matrix: List[List[int]]):
    
    node_to_analize: int = 0
    closest_neighbor: int = None
    solution_path: List[int] = [0]

    for node in range(1, distance_matrix):
        
        for neighbor in range(distance_matrix[node_to_analize]):
            distance_to_neighbor = distance_matrix[node_to_analize][neighbor]
        
            if (closest_neighbor is None or distance_to_neighbor < distance_matrix[node_to_analize][closest_neighbor]) and not(neighbor in solution_path):
                closest_neighbor = neighbor
        
        solution_path.append(closest_neighbor)
    
    return solution_path