import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

G = nx.Graph()
dc = bc = cc = {}


def build():
    df = pd.read_csv("temp.csv")

    for idx, x in df['committers'].iteritems():
        commiters = x.split()
        # first_committer = commiters.pop(0)
        # G.add_node(first_committer)
        # # G.add_node(first_committer, distance=9999, visited=False)
        # for committer in commiters:
        #     G.add_node(committer)
        #     G.add_edge(first_committer, committer)

        for _ in commiters:
            first_committer = commiters.pop(0)
            if not G.has_node(first_committer):
                G.add_node(first_committer)
            for other in commiters:
                if not G.has_node(other):
                    G.add_node(other)
                if not G.has_edge(first_committer, other):
                    G.add_edge(first_committer, other)

    edges = list(map(lambda tup: tup[0]+":"+tup[1], G.edges()))
    with open('DevNetEdges.txt', mode='w') as myfile:
        myfile.write('\n'.join(edges))


def bfs(start_node, end_node):
    queue = list()
    predecessor = {}

    if start_node == end_node:
        return []

    queue.append(start_node)
    predecessor[start_node] = None

    while queue and queue[0] != end_node:
        n = queue.pop(0)
        for neighbor in list(G.neighbors(n)):
            if neighbor not in predecessor:
                predecessor[neighbor] = n
                queue.append(neighbor)

    if not queue:
        return None

    else:
        path = list()
        path.append(end_node)
        pred = predecessor[end_node]
        while pred is not None:
            path.append(pred)
            pred = predecessor[pred]

        return path


def display_network():
    print(G.number_of_edges())
    print(G.number_of_nodes())
    print(G.nodes())
    print(G.edges())
    nx.draw(G)
    plt.savefig("path_graph.pdf")


def main():
    build()
    for start_node in G.nodes():
        for end_node in G.nodes():
            if start_node != end_node:
                print("start node is", start_node)
                print("end_node is", end_node)
                print(bfs(start_node, end_node))
                print()

    # display_network()


if __name__ == '__main__':
    main()