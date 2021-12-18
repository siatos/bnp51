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
    parser.add_argument('--xf', action='store', help='input excel file)')
    parser.add_argument('--nf', action='store', help='input nodes file)')

    arguments = parser.parse_args()

    return arguments

def read_xcel_file(fname):
    df = pd.read_excel(fname, index_col=None, header=None)
    #print(df)
    value_list = df.values.tolist()
    #value_dict = df.to_dict()
    return value_list

def create_gene_dict(node_list, adj_matrix):
    """
    Read data from a list of nodes and its adjacency matrix (represented here as a list of rows 
    and return a dictionary of nodes (each key is a node) and the number of nodes (a row having 1's and/or 0's )
    The dict should have a form like:
      Gene_x:[0, 1, ..., 1] 300 elements in each list. There will be 300 keys (genes) in the dictionary
    Essentialy this is the adjacency matrix of the graph  a 300x300 square matrix in a slightly different format 
    :param
         node_list: input node list
         adj_matrix: input list of lists (rows) 
    :return:
        return_dict: dictionary of nodes
        count: number of nodes
    There are no validation/consistency checks on the input data    
    """
    # Initialize local values
    return_dict = {}
    count = 0 
 
    # iterate through the lists simultaneously
    for (gene, row) in zip(node_list, adj_matrix):
        key = "Gene_" + str(gene[0]) #each member of node_list is a list 
        #print(key)
        return_dict[key] = row 
        count +=1
    return return_dict, count

def get_nodes_by_degree(Grph, n):
    """
    return a list of nodes of size n in acsending order based on degree sizes 
    :param
         Grph: graph 
         n: size of list 
    :return:
        degree_list: list of nodes sorted on their degree ascending order 
    """
    degree_list = list(Grph.degree())
    sorted_list = sorted(degree_list, key=take_second)
    print("Degree for each node: {}".format(sorted_list))
    print("")
    print("=============================")
    print("The highest {} elements of list (in ascending order) are : {}".format(n, str(sorted_list[-n:])))
    return  sorted_list[-n:]

def get_betweenness_centrality(Grph):
    #return nx.algorithms.centrality.betweenness_centrality(Grph)
    return sorted(nx.betweenness_centrality(Grph).items(), key=lambda item: item[1])

def take_second(elem):
    """
    used to return the second element of an element tuple
    i could not make lambdha expression work properly, sad ...
    """
    return elem[1]


if __name__ == '__main__':
    ARGS = parse_input()
    input_nodes = str(ARGS.nf)
    input_xcell = str(ARGS.xf)
    nodes_list = read_xcel_file(str(ARGS.nf))
    #print(nodes_list)
    adj_list   = read_xcel_file(str(ARGS.xf))
    # print(adj_list)
    gene_dict, no_of_nodes = create_gene_dict(nodes_list, adj_list)
    # print(gene_dict)

    # create a undirected graph based on above info. 
    G=nx.Graph()

    # add the nodes
    for node in gene_dict:
        #print("Adding Node: {}".format(node))
        G.add_node(str(node))

    # add the edges
    for node in gene_dict:
        #print("Node is: {}: {}".format(node, gene_dict[node]))
        for i, val in enumerate(gene_dict[node]):
        #print("pos {} value {}".format(i+1, val)) 
            if int(val):
                end="Gene_"+str(i + 1)
                #print("Adding EDGE: {} {}".format(node,end))
                G.add_edge(node, end)

    nx.draw_circular(G, with_labels=True)
    #nx.draw(G)


    print("Find Degree for each node ...")
    get_nodes_by_degree(G, 5)

    print("Find betweeness centrality ...")
    print(get_betweenness_centrality(G))

    #print("Find Degree for each node ...")
    #degree_list = list(G.degree())
    #sorted_list = sorted(degree_list, key=take_second)
    ##print("Degree {}".format(sorted_list))
    #print("============================")
    #print("The highest 5 elements of list (in ascending order) are : " + str(sorted_list[-5:]))

    for c in sorted(nx.connected_components(G), key=len, reverse=True): 
        S = G.subgraph(c).copy()
        print(S)
        print("Number of nodes for connected subgraph component S: {}".format(S.number_of_nodes()))


    print("Starting to plot ...")
    plt.axis("off")
    plt.show()
