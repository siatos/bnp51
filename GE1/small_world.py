from argparse import ArgumentParser
import networkx as nx
import matplotlib.pyplot as plt


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



if __name__ == '__main__':
    ARGS = parse_input()
    NODES = int(ARGS.nodes)

    G = nx.watts_strogatz_graph(n = NODES, k = 4, p = 0.5)
    #nx.draw(G)
    # get degree distribution for later use
    degrees = plot_degree_dist(G)
    print("Starting to plot ...")

    nx.draw_circular(G)

    plt.axis("on")
    plt.show()
