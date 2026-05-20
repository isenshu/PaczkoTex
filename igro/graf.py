import networkx as nx
from dane import points, edges


def buildGraph():
    G = nx.MultiGraph()

    for point in points:
        G.add_node(
            point["id"],
            name=point["name"],
            lat=point["lat"],
            lon=point["lon"]
        )

    for edge in edges:
        G.add_edge(
            edge["from"],
            edge["to"],
            czas=edge["czas"],
            km=edge["km"],
            droga=edge["droga"],
            predkoscMax=edge["predkoscMax"],
            predkoscSrednia=edge["predkoscSrednia"],
            natezenieRuchu=edge["natezenieRuchu"],
            jakoscDrogi=edge["jakoscDrogi"]
        )

    return G