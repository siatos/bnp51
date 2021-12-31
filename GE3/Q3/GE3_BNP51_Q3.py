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


if __name__ == '__main__':
    ARGS = parse_input()
    S1 = int(ARGS.size1)
    S2 = int(ARGS.size2)
    Total_Nodes= 20

    G=nx.Graph()

    #G=nx.complete_multipartite_graph(int(S1), int(S2), int(S3))
    print(G.edges())
    for x in range(1,S1):
        G.add_edge(0,x)
    G.add_edge(0, S1)
    for x in range(S1+1,S1+S2):
        G.add_edge(S1, x)
    if (Total_Nodes - (S1+S2)) <= 0:
        print("There are not enough nodes to assign to the 3rd subgraph - only two will be used)")
    else:
        for x in range(S1+S2+1, Total_Nodes):
            G.add_edge(S1+S2, x)
        G.add_edge(S1+S2, S2)


    print("all nodes connected")
    for c in sorted(nx.connected_components(G), key=len, reverse=True):
        S = G.subgraph(c).copy()
        print(S)
        print("Number of nodes for connected subgraph component S: {}".format(S.number_of_nodes()))

    print("removing one edge")
    G.remove_edge(S1+S2, S2)
    for c in sorted(nx.connected_components(G), key=len, reverse=True):
        S = G.subgraph(c).copy()
        print(S)
        print("Number of nodes for connected subgraph component S: {}".format(S.number_of_nodes()))

    print("removing one more edge")
    G.remove_edge(0, S1)
    for c in sorted(nx.connected_components(G), key=len, reverse=True):
        S = G.subgraph(c).copy()
        print(S)
        print("Number of nodes for connected subgraph component S: {}".format(S.number_of_nodes()))

    nx.draw_circular(G, with_labels=True)
    plt.show() # display
