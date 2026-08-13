import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
import numpy as np


def create_er_graph(p,N=1000):
    G = nx.Graph()

    G.add_nodes_from(range(N))


    for pair in itertools.combinations(range(N), 2):
        rng_ = random.uniform(0,1)
        if (rng_ <= (p)) and (pair[0] != pair[1]):
            G.add_edge(pair[0], pair[1])

    return G


def draw_graph(G,title=None):
    layout_ = nx.spring_layout(G, k=0.5, iterations=50)

    nx.draw(G, layout_)

    print(G.number_of_edges())

    if title:
        plt.title(title)

    plt.show()



def show_degree_distrib(G,title=None):
    degree_sequence = sorted((d for n, d in G.degree()), reverse=True)

    plt.hist(degree_sequence)

    if title:
        plt.title(title)

    plt.show()

def get_individual_connectivity(G: nx.Graph, node):

    shortest_paths = nx.shortest_path(G, node)
    shortest_path_sum = 0

    for n, path in shortest_paths.items():
        if n!=node:
            shortest_path_sum += len(path)

    c_i = 1/shortest_path_sum
    return c_i

def get_individual_clustering(G: nx.Graph, A_3, node):




    n_degree = G.degree[node]


    c_i = A_3[node][node]/(n_degree*(n_degree-1))

    return c_i

def get_avg_clustering(G: nx.Graph):
    total_coeff = 0

    A = (nx.adjacency_matrix(G)).toarray()

    A_3 = np.dot(A, np.dot(A, A))

    for node in G:
        total_coeff += get_individual_clustering(G, A_3, node)

    return total_coeff/(G.number_of_nodes())

def get_connected_components(G: nx.Graph):
    return list(nx.connected_components(G))

def graph_threshold(N):
    p_list = [p / 1000000 for p in range(1,15000,100)]

    results = {}
    for p in p_list:
        G = create_er_graph(p,N)

        connected_components = sorted(nx.connected_components(G), key=len, reverse=True)

        largest_comp = len(connected_components[0])

        results[p] = largest_comp

        print(f"Created graph for p={p}")

    return results


def plot_threshold(N):
    results = graph_threshold(N)

    threshold = np.log(N)/N

    plt.plot(list(results.keys()),list(results.values()))

    plt.axvline(threshold,color="red")
    plt.axvline(x=(1/N),color="green")

    plt.title(f"N={N} ; Threshold = {round(threshold,4)}")

    plt.xlabel("p value")
    plt.ylabel("Largest Component Size")

    plt.show()
        

p = 0.01
N = 1000
G = create_er_graph(p,N)

plot_threshold(N)

"""
avg_clustering = get_avg_clustering(G)
#print(nx.shortest_path(G, 1))
print("")
show_degree_distrib(G, f"p={p} ; N={N} ; Avg Clustering={round(avg_clustering,4)}")
draw_graph(G)
"""



