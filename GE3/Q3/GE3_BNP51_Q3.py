"""
Script to solve Q3 for GE3
Usage: python GE3_BNP51_Q3.py -size1 <size 1> -size2 <size 2>
"""

from argparse import ArgumentParser
import networkx as nx
import matplotlib.pyplot as plt
#import xlrd
#import pandas as pd
#import itertools
from constants import Total_Nodes

def parse_input():
    """
    Parse the command line ARGUMENTS
    """
    parser = ArgumentParser()
    parser.add_argument('-s1', '--size1', action='store', help='size of first component')
    parser.add_argument('-s2', '--size2', action='store', help='size of second component')

    arguments = parser.parse_args()

    return arguments

def plot_graphs(Grph1, Grph2, Grph3):

    fig = plt.figure("Plot graphs", figsize=(9, 4))
    # Create a gridspec for adding subplots of different sizes
    axgrid = fig.add_gridspec(2, 8)

    # Graph 1
    ax0 = fig.add_subplot(axgrid[:, :2])
    pos = nx.circular_layout(Grph1)
    nx.draw_networkx_nodes(Grph1, pos, ax=ax0, node_size=20)
    nx.draw_networkx_edges(Grph1, pos, ax=ax0, alpha=0.4)
    ax0.set_title("Connected components of Graph 1")
    ax0.set_axis_off()

    # Graph 2
    ax0 = fig.add_subplot(axgrid[:, 3:5])
    pos = nx.circular_layout(Grph2)
    nx.draw_networkx_nodes(Grph2, pos, ax=ax0, node_size=20)
    nx.draw_networkx_edges(Grph2, pos, ax=ax0, alpha=0.4)
    ax0.set_title("Connected components of Graph 2")
    ax0.set_axis_off()

    # Graph 3
    ax0 = fig.add_subplot(axgrid[:, 6:8])
    pos = nx.circular_layout(Grph3)
    nx.draw_networkx_nodes(Grph3, pos, ax=ax0, node_size=20)
    nx.draw_networkx_edges(Grph3, pos, ax=ax0, alpha=0.4)
    ax0.set_title("Connected components of Graph 3")
    ax0.set_axis_off()

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    ARGS = parse_input()
    S1 = int(ARGS.size1)
    S2 = int(ARGS.size2)
    if (Total_Nodes - (S1+S2)) <= 0:
        print("There are not enough nodes to assign to the 3rd subgraph - please assign S1 & s2 do that s1+s2 < Total_Nodes (= 20))")
        exit(1)
 
    G=nx.Graph()

    for x in range(1,S1):
        G.add_edge(0,x)
    G.add_edge(0, S1)
    for x in range(S1+1,S1+S2):
        G.add_edge(S1, x)
    for x in range(S1+S2+1, Total_Nodes):
        G.add_edge(S1+S2, x)
    G.add_edge(S1+S2, S2)

    # create a copy Grph1 of the original G
    Grph1=G.copy()
    print("========================================================================")
    print("all nodes connected - there will be 1 connected component")
    for c in sorted(nx.connected_components(G), key=len, reverse=True):
        S = G.subgraph(c).copy()
        print(S)
        print("Number of nodes for connected subgraph component: {}".format(S.number_of_nodes()))
    print("========================================================================")
    print("removing one edge - there will be 2 connected components")
    G.remove_edge(S1+S2, S2)
    for c in sorted(nx.connected_components(G), key=len, reverse=True):
        S = G.subgraph(c).copy()
        print(S)
        print("Number of nodes for connected subgraph component: {}".format(S.number_of_nodes()))
   # create a copy Grph2 of the original G
    Grph2=G.copy()
    print("========================================================================")
    print("removing one more edge - there will be 3 connected components")
    G.remove_edge(0, S1)
    for c in sorted(nx.connected_components(G), key=len, reverse=True):
        S = G.subgraph(c).copy()
        print(S)
        print("Number of nodes for connected subgraph component: {}".format(S.number_of_nodes()))

    # create a copy Grph3 of the original G
    Grph3=G.copy()
    print("========================================================================")

    plot_graphs(Grph1, Grph2, Grph3)

    #nx.draw_circular(G, with_labels=True)
    #plt.show() # display
