from graph_creator import *
from heuristics import *
import argparse

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
        choices=["nn", "mn", "gme", "r"],
        required=True,
        help="Por favor seleccionar alguno de los constructores disponibles. nn: nearest neighbor, mn: mean neighbor, gme: greedy min edges, r: tour regular factible trivial.",
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
    graph = create_graph(INSTANCES.index(instance))

    # Execute the chosen constructor function
    if args.constructor == "nn":
        tour = nearest_neighbor(graph)
    elif args.constructor == "mn":
        tour = mean_neighbor(graph)
    elif args.constructor == "gme":
        tour = greedy_min_edges(graph)
    elif args.constructor == "r":
        tour = regular_tour(graph)

    # Execute the chosen operator functions if provided
    if args.operadores:
        for operador in args.operadores:
            if operador == "r":
                tour = relocate_continuous(graph, tour)
            elif operador == "s":
                tour = swap_continuous(graph, tour)
            elif operador == "2o":
                tour = two_opt_continuous(graph, tour)

    # agregar print tour y resultado
    print(tour)
    print(travel_distance(graph, tour))


if __name__ == "__main__":
    main()
