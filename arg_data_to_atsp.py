from typing import List, Dict, Tuple
import math

def norma(vector1: Tuple[float, float], vector2: Tuple[float, float]):
    return math.sqrt((vector1[0] - vector2[0])**2 + (vector1[1] - vector2[1])**2)

def search_values(txt):

    res: List[int] = []
    caracter_to_analize = ""
    can_add = False

    for caracter in txt:

        try:

            float(caracter_to_analize + caracter)
            caracter_to_analize += caracter
            can_add = True

        except:

            if can_add:

                caracter_to_int = float(caracter_to_analize)
                res.append(caracter_to_int)
                can_add = False

            caracter_to_analize = caracter

    if can_add:
        res.append(float(caracter_to_analize))

    return res

def convert_data():
    
    file = open("./ar9152.tsp", "r", encoding="UTF-8")

    nodes_coord = False

    res: List[List[float]] = []

    nodes_coord: Dict[str, Tuple[float, float]] = dict()

    for line in file:

        if nodes_coord:

            values_line = search_values(line)
            res.append([])
            nodes_coord[str(values_line[0])] = (values_line[1], values_line[2])

            for neighbor in range(1, values_line[0]):
                distance = norma(nodes_coord[values_line[0]], nodes_coord[neighbor])
                res[values_line[0]-1][neighbor-1] = distance
                res[values_line[0]-1][neighbor-1] = distance


            res[values_line[0]-1][values_line[0]-1] = 0

        if "NODE_COORD_SECTION" in line:
            nodes_coord = True

    return res

print(convert_data())