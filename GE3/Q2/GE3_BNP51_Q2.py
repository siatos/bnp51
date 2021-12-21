from argparse import ArgumentParser
import networkx as nx
import matplotlib.pyplot as plt
import xlrd
import pandas as pd
import itertools

def parse_input():
    """
    Parse the command line ARGUMENTS
    """
    parser = ArgumentParser()
    parser.add_argument('--nodes', action='store', help='number of nodes')

    arguments = parser.parse_args()

    return arguments

def plot_degree_dist(G):
    return [G.degree(n) for n in G.nodes()]
    #plt.hist(degrees)
    #plt.show()



def get_betweenness_centrality(Grph):
    #return nx.algorithms.centrality.betweenness_centrality(Grph)
    return sorted(nx.betweenness_centrality(Grph).items(), key=lambda item: item[1])


if __name__ == '__main__':
    ARGS = parse_input()
    NODES = int(ARGS.nodes)
    print("Create two graph networks using {} nodes for each".format(NODES))

    print("a small-world network using watts-stogatz algorithm ")
    GSW = nx.watts_strogatz_graph(n = NODES, k = 4, p = 0.5)
    GSW_layout = nx.circular_layout(GSW)

    print("and a scale-free network using barabasi-albert algorithm")
    GSF = nx.barabasi_albert_graph(NODES, 10)
    GSF_layout = nx.circular_layout(GSF)

    for k, v in GSF_layout.items():
    # Shift the x values of every GSF node by 2.1 to the right
    # number depends on the layout 
        v[0] = v[0] + 2.1 

   
    nx.draw(GSW, GSW_layout, node_size=int(NODES))
    nx.draw_networkx_labels(GSW, GSW_layout, labels={n: n for n in GSW}) 
    
    nx.draw(GSF, GSF_layout, node_size=int(NODES))
    nx.draw_networkx_labels(GSF, GSF_layout, labels={n: n for n in GSF}) 

    plt.show() # display

