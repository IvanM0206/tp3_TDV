from typing import List


files_names = [
    "br17",
    "ft53",
    "ft70",
    "ftv33",
    "ftv35",
    "ftv38",
    "ftv44",
    "ftv47",
    "ftv70",
    "ftv170",
    "kro124p",
    "p43",
    "rbg323",
    "rbg358",
    "rbg403",
    "rbg443",
    "ry48p",
]


def search_numbers_in_txt(txt):

    res: List[int] = []
    caracter_to_analize = ""
    can_add = False

    for caracter in txt:

        try:

            int(caracter_to_analize + caracter)
            caracter_to_analize += caracter
            can_add = True

        except:

            if can_add:

                caracter_to_int = int(caracter_to_analize)
                res.append(caracter_to_int)
                can_add = False

            caracter_to_analize = caracter

    if can_add:
        res.append(int(caracter_to_analize))

    return res


def create_graph(index) -> List[List[int]]:
    file_chosen = files_names[index]

    file = open(
        f"./ALL_atsp/{file_chosen}.atsp/{file_chosen}.atsp", "r", encoding="UTF-8"
    )

    matrix_distance: List[List[int]] = [[]]
    weight_data = False
    i = 0
    cant_vertex = 0
    for line in file:

        if "DIMENSION" in line:
            list_dimension = search_numbers_in_txt(line)
            cant_vertex = list_dimension[0]
            print(cant_vertex)

        if weight_data:

            numbers_in_line = search_numbers_in_txt(line)

            cant_numbers_to_add = min(
                len(numbers_in_line), cant_vertex - len(matrix_distance[i])
            )

            if cant_numbers_to_add == cant_vertex - len(matrix_distance[i]):
                agregar = True
            else:
                agregar = False

            for number_pos in range(cant_numbers_to_add):
                matrix_distance[i].append(numbers_in_line[number_pos])

            if agregar:

                i += 1
                matrix_distance.append([])

            for number_pos in range(cant_numbers_to_add, len(numbers_in_line)):
                matrix_distance[i].append(numbers_in_line[number_pos])

        if "EDGE_WEIGHT_SECTION" in line:
            weight_data = True

    matrix_distance.pop()
    return matrix_distance
