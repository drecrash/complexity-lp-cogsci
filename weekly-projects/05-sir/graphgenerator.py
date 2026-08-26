import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
import numpy as np

class GraphGenerator():
    def create_er_graph(self,p,N=1000,attr = {}):
        G = nx.Graph()

        G.add_nodes_from(range(N), **attr)


        for pair in itertools.combinations(range(N), 2):
            rng_ = random.uniform(0,1)
            if (rng_ <= (p)) and (pair[0] != pair[1]):
                G.add_edge(pair[0], pair[1])

        return G

    def create_ba_graph(self,m, T=1000,attr = {}):
        G = nx.complete_graph(m)

        for node in G.nodes():
            for key, val in attr.items():
                G.nodes[node][key] = val

        for t in range(T):
            new_node = m+t
            G.add_node(new_node, **attr)

            p = []

            degree_sum = sum(d for n, d in G.degree())

            for n, d in G.degree():
                p.append(d/degree_sum)

            connections = np.random.choice(list(G.nodes), size=m, p=p)

            for node_index in connections:
                G.add_edge(new_node, node_index)

        return G


            
    def get_degree_seq(self,G):
        degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
        return degree_sequence


    def show_degree_distrib(self,G,title=None):
        
        plt.hist(self.get_degree_seq(G))

        if title:
            plt.title(title)

        plt.show()

    def get_individual_connectivity(self,G: nx.Graph, node):

        shortest_paths = nx.shortest_path(G, node)
        shortest_path_sum = 0

        for n, path in shortest_paths.items():
            if n!=node:
                shortest_path_sum += len(path)

        c_i = 1/shortest_path_sum
        return c_i

    def get_individual_clustering(self,G: nx.Graph, A_3, node):




        n_degree = G.degree[node]


        c_i = A_3[node][node]/(n_degree*(n_degree-1))

        return c_i

    def get_avg_clustering(self, G: nx.Graph):
        total_coeff = 0

        A = (nx.adjacency_matrix(G)).toarray()

        A_3 = np.dot(A, np.dot(A, A))

        for node in G:
            total_coeff += self.get_individual_clustering(G, A_3, node)

        return total_coeff/(G.number_of_nodes())

    def get_connected_components(self, G: nx.Graph):
        return list(nx.connected_components(G))

    def graph_threshold(self, N, graph_type: function):
        p_list = [p / 1000000 for p in range(1,15000,100)]

        results = {}
        for p in p_list:
            G = graph_type(p,N)

            connected_components = sorted(nx.connected_components(G), key=len, reverse=True)

            largest_comp = len(connected_components[0])

            results[p] = largest_comp

            print(f"Created graph for p={p}")

        return results


    def plot_threshold(self,N):
        results = self.graph_threshold(N, self.create_er_graph)

        threshold = np.log(N)/N

        plt.plot(list(results.keys()),list(results.values()))

        plt.axvline(threshold,color="red")
        plt.axvline(x=(1/N),color="green")

        plt.title(f"N={N} ; Threshold = {round(threshold,4)}")

        plt.xlabel("p value")
        plt.ylabel("Largest Component Size")

        plt.show()




