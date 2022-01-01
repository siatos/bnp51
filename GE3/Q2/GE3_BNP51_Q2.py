"""
Script to solve Q2 for GE3
Usage: python GE3_BNP51_Q2.py --nodes <nodes>
"""

from argparse import ArgumentParser
import networkx as nx
import numpy as np
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

def plot_graph_and_distribution(Grph1, Grph2):
    degree_sequence1 = sorted([d for n, d in Grph1.degree()], reverse=True)
    dmax1 = max(degree_sequence1)

    degree_sequence2 = sorted([d for n, d in Grph2.degree()], reverse=True)
    dmax2 = max(degree_sequence2)

    fig = plt.figure("Compare small-world & B-A scale-free graphs", figsize=(12, 14))
    # Create a gridspec for adding subplots of different sizes
    axgrid = fig.add_gridspec(5, 8)

    # Graph 1
    ax0 = fig.add_subplot(axgrid[0:3, :4])
    Gcc1 = Grph1.subgraph(sorted(nx.connected_components(Grph1), key=len, reverse=True)[0])
    pos = nx.spring_layout(Gcc1, seed=10396953)
    nx.draw_networkx_nodes(Gcc1, pos, ax=ax0, node_size=20)
    nx.draw_networkx_edges(Gcc1, pos, ax=ax0, alpha=0.4)
    ax0.set_title("Connected components of Small-World")
    ax0.set_axis_off()

    # Graph 2
    ax0 = fig.add_subplot(axgrid[0:3, 4:])
    Gcc2 = Grph2.subgraph(sorted(nx.connected_components(Grph2), key=len, reverse=True)[0])
    pos = nx.spring_layout(Gcc2, seed=10396953)
    nx.draw_networkx_nodes(Gcc2, pos, ax=ax0, node_size=20)
    nx.draw_networkx_edges(Gcc2, pos, ax=ax0, alpha=0.4)
    ax0.set_title("Connected components of Scale-Free BA")
    ax0.set_axis_off()

    # Graph 1
    ax1 = fig.add_subplot(axgrid[3:, :2])
    ax1.plot(degree_sequence1, "b-", marker="o")
    ax1.set_title("Degree Rank Plot")
    ax1.set_ylabel("Degree")
    ax1.set_xlabel("Rank")

    ax2 = fig.add_subplot(axgrid[3:, 2:4])
    ax2.bar(*np.unique(degree_sequence1, return_counts=True))
    ax2.set_title("Degree histogram")
    ax2.set_xlabel("Degree")
    ax2.set_ylabel("# of Nodes")

    # Graph 2 
    ax1 = fig.add_subplot(axgrid[3:, 4:6])
    ax1.plot(degree_sequence2, "b-", marker="o")
    ax1.set_title("Degree Rank Plot")
    ax1.set_ylabel("Degree")
    ax1.set_xlabel("Rank")

    ax2 = fig.add_subplot(axgrid[3:, 6:8])
    ax2.bar(*np.unique(degree_sequence2, return_counts=True))
    ax2.set_title("Degree histogram")
    ax2.set_xlabel("Degree")
    ax2.set_ylabel("# of Nodes")

    fig.tight_layout()
    plt.show()



def take_second(elem):
    """
    used to return the second element of an (element) tuple
    i could not make lambda expression work properly, sad ...
    """
    return elem[1]


def get_betweenness_centrality(Grph, n):
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


    print("====================== small-world =========================")
    degree_list = list(GSW.degree())
    sorted_list = sorted(degree_list, key=take_second, reverse=True)
    print("Degree for each node of small-world: {}".format(sorted_list))
    print("============================================================")
    print("Find betweeness centrality for small-world network ...")
    get_betweenness_centrality(GSW, SIZE_OF_NODESLIST)
    print("============================================================")
    print("")
    print("==================== scale-free ============================")
    degree_list = list(GSF.degree())
    sorted_list = sorted(degree_list, key=take_second, reverse=True)
    print("Degree for each node of scale-free: {}".format(sorted_list))
    print("============================================================")
    print("Find betweeness centrality for scale-free network ...")
    get_betweenness_centrality(GSF, SIZE_OF_NODESLIST)
    print("============================================================")
    print("")
    print("Additional metrics for small-world")
    print('average path length: {}'.format(nx.average_shortest_path_length(GSW)))
    print('average diameter: {}'.format(nx.diameter(GSW)))
    G_cluster = sorted(list(nx.clustering(GSW).values()))
    print('average clustering coefficient: {}'.format(sum(G_cluster) / len(G_cluster)))
    print("")
    print("Additional metrics for scale-free")
    print('average path length: {}'.format(nx.average_shortest_path_length(GSF)))
    print('average diameter: {}'.format(nx.diameter(GSF)))
    G_cluster = sorted(list(nx.clustering(GSF).values()))
    print('average clustering coefficient: {}'.format(sum(G_cluster) / len(G_cluster)))



#    for k, v in GSF_layout.items():
#    # Shift the x values of every GSF node by 2.1 to the right
#    # number depends on the layout
#        v[0] = v[0] + 2.1
##
##    nx.draw(GSW, GSW_layout, node_size=int(NODES))
#    nx.draw_networkx_labels(GSW, GSW_layout, labels={n: n for n in GSW})
#    #
#    nx.draw(GSF, GSF_layout, node_size=int(NODES))
#    nx.draw_networkx_labels(GSF, GSF_layout, labels={n: n for n in GSF})
#    plt.show() # display

    plot_graph_and_distribution(GSW, GSF)
    #plot_graph_and_distribution(GSF)

