import sys
from graph_creator import *
from heuristics import *

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


def print_usage():
    usage_message = """
    Uso:
        main.py -CONSTRUCTOR (-OPERADOR) <instancia>
    
    Opciones:
        -CONSTRUCTOR    Constructores disponibles: ...
        -OPERADOR Operadores disponibles: ...
        <instancia> Instancias disponibles: {}
    """.format(
        ", ".join(INSTANCES)
    )

    print(usage_message)


def main():
    limitation = 0
    if (
        len(sys.argv) < 3
        or sys.argv[1] not in ("-i", "--instance")
        or sys.argv[2] in ("-h", "--help")
    ):
        print_usage()
        sys.exit(1)

    instance_name = sys.argv[2]

    if instance_name not in INSTANCES:
        print(f"Error: '{instance_name}' no es un nombre de instancia válido.")
        print_usage()
        sys.exit(1)

    instance = load_instance(instance_name)

    if len(sys.argv) == 6 and (
        sys.argv[3] in ("-l1", "--limitation1")
        or sys.argv[3]
        in (
            "-l2",
            "--limitation2",
        )
    ):
        if not (sys.argv[4].isnumeric() or sys.argv[5].isnumeric()):
            print(
                f"Error: las limitaciones toman la forma de  -l1/-l2 indice-estación limitación-unidades. Ej: -l1 1 30"
            )
            print_usage()
            sys.exit(1)

        # Definir valores para el upper_bound (capacidad) de la arista de trasnoche correspondiente a target_station (estación de cabecera)
        target_station = instance["stations"][int(sys.argv[4])]
        upper_bound = int(sys.argv[5])
        limitation = 1 if sys.argv[3] in ("-l1", "--limitation1") else 2

    elif len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    # Construimos el grafo con el cambio de variable necesario

    G, colors, pos, labels, border_colors, edge_colors, services_by_station = (
        add_services(instance)
    )

    G, night_edges = add_night_pass_edges(G, instance, edge_colors, services_by_station)

    # Agregamos una limitación de ser necesario.

    if limitation == 1:
        G = add_limitation(G, target_station, upper_bound)
    elif limitation == 2:
        G, pos, night_edges, colors, edge_colors, border_colors = add_limitation2(
            instance, G, target_station, upper_bound, colors, edge_colors, border_colors
        )

    # Ejecutamos el algoritmo para obtener el flujo de costo minimo satisfaciendo los imbalances
    minCostFlow = nx.min_cost_flow(
        G, demand="demand", capacity="upper_bound", weight="weight"
    )
    minCost = nx.cost_of_flow(G, minCostFlow)

    # Recuperamos el flujo en el grafo original (sin cambio de variable)
    for i in minCostFlow:
        for j in minCostFlow[i]:
            minCostFlow[i][j] += G[i][j]["amount_modified"]

    print("minCostFlow: {}\nminCost: {}".format(minCostFlow, minCost))

    # Mostramos el grafo
    visualize_graph(
        G,
        colors,
        pos,
        labels,
        border_colors,
        edge_colors,
        night_edges,
        minCostFlow,
    )


if __name__ == "__main__":
    main()
