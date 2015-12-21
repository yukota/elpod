# -*- coding: utf-8 -*-

import networkx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print("start")
    graph = networkx.DiGraph()
    node = set(["a", "b", "c", "d", "e"])
    print(node)
    graph.add_nodes_from(node)
    edge_weight = [("a", "b", 1), ("b", "d", 3), ("a", "c", 1), ("c", "e", 1), ("e", "d",5 )]
    graph.add_weighted_edges_from(edge_weight)

    edgewidth = []
    for (u, v, d) in graph.edges(data=True):
        print(d)
        edgewidth.append(d.get('weight'))

    networkx.draw_spring(graph, iterations=20, with_labels=True, width=edgewidth)
    path = networkx.bidirectional_dijkstra(graph, "a", "d")
    print("path")
    print(path)

    plt.show()

