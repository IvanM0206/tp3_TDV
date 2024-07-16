from typing import List, Dict, Tuple
import math


def norma(vector1: Tuple[float, float], vector2: Tuple[float, float]):
    return math.sqrt((vector1[0] - vector2[0]) ** 2 + (vector1[1] - vector2[1]) ** 2)


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

    target_line = False

    res: List[List[float]] = []

    nodes_coord: Dict[str, Tuple[float, float]] = dict()

    for line in file:

        if target_line and "EOF" not in line:

            values_line = search_values(line)
            res.append([0] * n)
            nodes_coord[values_line[0]] = (values_line[1], values_line[2])

        if "NODE_COORD_SECTION" in line:
            target_line = True

        if "DIMENSION" in line:
            n = int(search_values(line)[0])

    for node in range(n):
        for neighbor in range(n):
            distance = norma(
                nodes_coord[float(node + 1)], nodes_coord[float(neighbor + 1)]
            )
            res[node - 1][neighbor - 1] = distance
            res[node - 1][neighbor - 1] = distance

            res[node - 1][node - 1] = 0

    return res


print(len(convert_data()))
