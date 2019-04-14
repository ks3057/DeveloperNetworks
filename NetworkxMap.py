import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import collections

G = nx.Graph()
bc = cc = dc = {}
visited = {}


def build():
    df = pd.read_csv("filemap.csv")
    for idx, x in df['committers'].iteritems():
        committers = x.split()
        for committer in committers:
            first_committer = committer
            if not G.has_node(first_committer):
                G.add_node(first_committer)
                bc[first_committer] = 0
                dc[first_committer] = 0
            for other in committers:
                if first_committer != other:
                    if not G.has_node(other):
                        G.add_node(other)
                        bc[other] = 0
                        dc[other] = 0
                    if not G.has_edge(first_committer, other):
                        G.add_edge(first_committer, other)

    edges = list(map(lambda tup: tup[0]+":"+tup[1], G.edges()))
    with open('DevNetEdges.txt', mode='w') as myfile:
        myfile.write('\n'.join(edges))


def bfs(start_node, end_node):
    queue = collections.deque()
    predecessor = {}

    queue.append(start_node)
    predecessor[start_node] = None

    while queue and queue[0] != end_node:
        n = queue.popleft()
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


def degree_centrality():
    for edge in G.edges():
        dc[edge[0]] += 1
        dc[edge[1]] += 1

    sum = G.number_of_nodes() - 1
    for key, value in dc.items():
        dc[key] = value/sum


def closeness_centrality():
    for start_node in G.nodes():
        for end_node in G.nodes():
            if start_node != end_node and not visited.get((start_node,
                                                           end_node), None):
                path = bfs(start_node, end_node)
                visited[(start_node, end_node)] = True
                visited[(end_node, start_node)] = True
                cc[start_node] += len(path) - 1
                cc[end_node] += len(path) - 1

    sum = G.number_of_nodes() - 1
    for key, value in dc.items():
        dc[key] = sum / value


def display_network():
    print()
    print("total nodes in graph:", G.number_of_nodes())
    print("total edges in graph:", G.number_of_edges())
    # print(G.nodes())
    # print(G.edges())
    nx.draw(G)
    plt.savefig("path_graph.pdf")


def betweenness_centrality():
    path_counter = 0
    for start in G.nodes():
        for end in G.nodes():
            if start != end and not visited.get((start, end), None):
                visited[(start, end)] = True
                visited[(end, start)] = True
                for path in nx.all_shortest_paths(G, start, end):
                    if len(path) > 2:
                        for element in path[1:-1]:
                            bc[element] += 1
                            path_counter += 1
                    else:
                        path_counter += 1

    for k, v in bc.items():
        bc[k] = v / path_counter
    sum1 = sum(bc.values())
    for key, val in bc.items():
        bc[key] = val / sum1


def main():
    build()
    print("network built")

    betweenness_centrality()
    print("betweenness centrality calculated")
    degree_centrality()
    print("degree centrality calculated")
    closeness_centrality()
    print("closeness centrality calculated")
    display_network()
    print("check path_graph.pdf for node display")


if __name__ == '__main__':
    main()