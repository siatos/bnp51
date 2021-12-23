from argparse import ArgumentParser
import networkx as nx
import matplotlib.pyplot as plt
#import xlrd
#import pandas as pd
#import itertools

def parse_input():
    """
    Parse the command line ARGUMENTS
    """
    parser = ArgumentParser()
    parser.add_argument('--s1', action='store', help='size of first component')
    parser.add_argument('--s2', action='store', help='size of second component')
    parser.add_argument('--s3', action='store', help='size of third component')

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


def get_betweenness_centrality(Grph):
    #return nx.algorithms.centrality.betweenness_centrality(Grph)
    return sorted(nx.betweenness_centrality(Grph).items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    ARGS = parse_input()
    S1 = int(ARGS.s1)
    S2 = int(ARGS.s2)
    S3 = int(ARGS.s3)
   #plot_distribution(GSW)
    G=nx.Graph()

    #G=nx.complete_multipartite_graph(int(S1), int(S2), int(S3))
    print(G.edges())
    for x in range(1,5):
        G.add_edge(0,x)
    for x in range(6,11):
        G.add_edge(5, x)
    for x in range(12,20):
        G.add_edge(11, x)
    G.add_edge(0, 5)
    G.add_edge(11, 5)


    for c in sorted(nx.connected_components(G), key=len, reverse=True): 
        S = G.subgraph(c).copy()
        print(S)
        print("Number of nodes for connected subgraph component S: {}".format(S.number_of_nodes()))


    nx.draw_circular(G, with_labels=True)
    plt.show() # display


