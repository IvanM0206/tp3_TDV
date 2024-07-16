from graph_creator import *
from heuristics import *
import argparse
import arg_data_to_atsp
import time

INSTANCES = [
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
    "ar9152",
]


def main():
    parser = argparse.ArgumentParser(description="Heurísticas para ATSP")

    # Required arguments
    parser.add_argument(
        "-i",
        "--instancia",
        required=True,
        choices=INSTANCES,
        help="Se debe especificar el nombre de la instancia objetivo.",
    )
    parser.add_argument(
        "-c",
        "--constructor",
        choices=["nn", "mn", "mp", "r"],
        required=True,
        help="Por favor seleccionar alguno de los constructores disponibles. nn: nearest neighbor, mn: mean neighbor, mp: min distance pair, r: tour regular factible trivial.",
    )

    # Optional arguments (up to 3)
    parser.add_argument(
        "-o",
        "--operadores",
        nargs="+",
        choices=["r", "s", "2o"],
        help="Especificar los operadores de búsqueda local deseados. r: relocate, s: swap, 2o: 2-opt.",
    )

    args = parser.parse_args()

    instance = args.instancia
    print("Instancia cargada:", instance)
    if instance == "ar9152":
        graph = arg_data_to_atsp.convert_data()
    else:
        graph = create_graph(INSTANCES.index(instance))
    print("Dimensión del grafo:", len(graph))

    start = time.time()
    # Execute the chosen constructor function
    if args.constructor == "nn":
        print("Constructor: vecino más cercano")
        tour = nearest_neighbor(0, graph)
    elif args.constructor == "mn":
        print("Constructor: vecino promedio")
        tour = mean_neighbor(0, graph)
    elif args.constructor == "mp":
        print("Constructor: pares de distancia mínima")
        tour = greedy_min_edges(graph)
    elif args.constructor == "r":
        print("Constructor: trivial")
        tour = regular_tour(graph)

    # Execute the chosen operator functions if provided
    if args.operadores:
        for operador in args.operadores:
            if operador == "r":
                print("Operador: relocate")
                tour = local_search(graph, tour, relocate)
            elif operador == "s":
                print("Operador: swap")
                tour = local_search(graph, tour, swap)
            elif operador == "2o":
                print("Operador: 2-opt")
                tour = local_search(graph, tour, two_opt)
    end = time.time()

    # agregar print tour y resultado
    print("Camino:", tour)
    print("Distancia:", travel_distance(graph, tour))
    print("Tiempo de ejecución:", end - start)


if __name__ == "__main__":
    main()
