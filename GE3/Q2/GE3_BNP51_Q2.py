from argparse import ArgumentParser
import networkx as nx
import matplotlib.pyplot as plt
#import xlrd
#import pandas as pd
#import itertools
from constants import SIZE_OF_NODESLIST, \
                      KAPA, \
                      PROB, \
                      NEW_EDGES

def parse_input():
    """
    Parse the command line ARGUMENTS
    """
    parser = ArgumentParser()
    parser.add_argument('-n', '--nodes', action='store', help='number of nodes')

    arguments = parser.parse_args()

    return arguments

#def plot_degree_dist(G):
#    return [G.degree(n) for n in G.nodes()]
#    #plt.hist(degrees)
#    #plt.show()

def take_second(elem):
    """
    used to return the second element of an (element) tuple
    i could not make lambdha expression work properly, sad ...
    """
    return elem[1]

#def plot_distribution(Grph):
#
#    degree_freq = nx.degree_histogram(Grph)
#    degrees = range(len(degree_freq))
#    plt.figure(figsize=(12, 8)) 
#    plt.loglog(degrees[3:], degree_freq[3:],'go-') 
#    plt.xlabel('Degree')
#    plt.ylabel('Frequency')
#    plt.show()


def get_betweenness_centrality(Grph, n):
    #return nx.algorithms.centrality.betweenness_centrality(Grph)
    #return sorted(nx.betweenness_centrality(Grph).items(), key=lambda x: x[1], reverse=True)
    SGrph = sorted(nx.betweenness_centrality(Grph).items(), key=lambda item: item[1], reverse=True)
    print("The highest {} elements of list (betweeness centrality in descending order) are : {}".format(n, str(SGrph[:n])))
    return SGrph[:n]



if __name__ == '__main__':
    ARGS = parse_input()
    NODES = int(ARGS.nodes)
    print("Create two graph networks using {} nodes for each".format(NODES))

    print("a small-world network using watts-stogatz algorithm ")
    GSW = nx.watts_strogatz_graph(n = NODES, k = KAPA, p = PROB)
    GSW_layout = nx.circular_layout(GSW)

    print("and a scale-free network using barabasi-albert algorithm")
    GSF = nx.barabasi_albert_graph(NODES, NEW_EDGES)
    #GSF = nx.scale_free_graph(NODES)
    GSF_layout = nx.circular_layout(GSF)


    print("============================================================")
    degree_list = list(GSW.degree())
    sorted_list = sorted(degree_list, key=take_second, reverse=True)
    print("Degree for each node of small-world: {}".format(sorted_list))
    print("============================================================")
    print("Find betweeness centrality for small-world network ...")
    print(get_betweenness_centrality(GSW, SIZE_OF_NODESLIST))
    print("============================================================")
    degree_list = list(GSF.degree())
    sorted_list = sorted(degree_list, key=take_second, reverse=True)
    print("Degree for each node of scale-free: {}".format(sorted_list))
    print("============================================================")
    print("Find betweeness centrality for scale-free network ...")
    print(get_betweenness_centrality(GSF, SIZE_OF_NODESLIST))
    print("============================================================")


    print('average path length: {}'.format(nx.average_shortest_path_length(GSW)))
    print('average diameter: {}'.format(nx.diameter(GSW)))
    G_cluster = sorted(list(nx.clustering(GSW).values()))
    print('average clustering coefficient: {}'.format(sum(G_cluster) / len(G_cluster)))

    print('average path length: {}'.format(nx.average_shortest_path_length(GSF)))
    print('average diameter: {}'.format(nx.diameter(GSF)))
    G_cluster = sorted(list(nx.clustering(GSF).values()))
    print('average clustering coefficient: {}'.format(sum(G_cluster) / len(G_cluster)))



    for k, v in GSF_layout.items():
    # Shift the x values of every GSF node by 2.1 to the right
    # number depends on the layout
        v[0] = v[0] + 2.1

    nx.draw(GSW, GSW_layout, node_size=int(NODES))
    nx.draw_networkx_labels(GSW, GSW_layout, labels={n: n for n in GSW})
    #
    nx.draw(GSF, GSF_layout, node_size=int(NODES))
    nx.draw_networkx_labels(GSF, GSF_layout, labels={n: n for n in GSF})
    #plot_distribution(GSW)
    plt.show() # display


