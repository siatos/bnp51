from argparse import ArgumentParser
import networkx as nx
import matplotlib.pyplot as plt
import xlrd
import pandas as pd
import itertools
import logging
import os

def parse_input():
    """
    Parse the command line ARGUMENTS
    """
    parser = ArgumentParser()
    parser.add_argument('-m', '--matrixfile', action='store', help='input matrix excel file')
    parser.add_argument('-n', '--nodesfile', action='store', help='input nodes excel file')

    arguments = parser.parse_args()

    return arguments

def read_xcel_file(fname):
    df = pd.read_excel(fname, index_col=None, header=None)
    #print(df)
    value_list = df.values.tolist()
    #value_dict = df.to_dict()
    return value_list

def log2file(logline, loglevel):
    if loglevel.lower() == 'debug':
       logging.debug(logline)
    elif loglevel.lower() == 'error':  
       logging.error(logline)
    elif loglevel.lower() == 'info':  
       logging.info(logline)
    else:
        logging.info('incoherent loglevel: ' + logline)


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
    return a list of nodes depending on degree size in descending order 
    :param
         Grph: graph 
         n: size of list 
    :return:
        degree_list: list of nodes sorted on their degree descending order 
    """
    degree_list = list(Grph.degree())
    sorted_list = sorted(degree_list, key=take_second, reverse=True)
    #print("Degree for each node: {}".format(sorted_list))
    print("=============================")
    print("The highest {} elements of list (in descending order) are : {}".format(n, str(sorted_list[:n])))
    return  sorted_list[:n]

def get_betweenness_centrality(Grph, n):
    """
    return a list of nodes depending on betweenes centrality in descending order 
    :param
         Grph: graph 
         n: size of list 
    :return:
        degree_list: list of nodes sorted on their betweeness centrality in descending order 
    """
    S = sorted(nx.betweenness_centrality(Grph).items(), key=lambda item: item[1], reverse=True)
    print("=============================")
    print("The highest {} elements of list (betweeness centrality in descending order) are : {}".format(n, str(S[:n])))
    return S[:n]

def take_second(elem):
    """
    used to return the second element of an (element) tuple
    i could not make lambdha expression work properly, sad ...
    """
    return elem[1]


if __name__ == '__main__':
    LOGFILE="log.txt"
    # remove possibly existing log file
    if os.path.isfile(LOGFILE):
        print("Removing file {}".format(LOGFILE))
        os.remove(LOGFILE)
    else:    # if there is no logfile show an error and continue ##
        print("Error: {} file not found, ...ok".format(LOGFILE))
    
    logging.basicConfig(filename=LOGFILE, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info('Started')

    ARGS = parse_input()
    #input_nodes = str(ARGS.n)
    #input_xcell = str(ARGS.m)

    nodes_list = read_xcel_file(str(ARGS.nodesfile))
    # print("Read {} nodes".format(len(nodes_list)))
    adj_list   = read_xcel_file(str(ARGS.matrixfile))
    # print(adj_list)
    gene_dict, no_of_nodes = create_gene_dict(nodes_list, adj_list)
    # print(gene_dict)

    # create a undirected graph based on above info. 
    G=nx.Graph()

    # add the nodes
    for node in gene_dict:
        #print("Adding Node: {}".format(node))
        G.add_node(str(node))

    print("graph created with {} nodes".format(G.number_of_nodes()))

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


    print("Find Degree for each node ... show the highest 5 nodes")
    get_nodes_by_degree(G, 10)

    print("Find betweeness centrality ...")
    get_betweenness_centrality(G, 10)

    #print("Find Degree for each node ...")
    #degree_list = list(G.degree())
    #sorted_list = sorted(degree_list, key=take_second)
    ##print("Degree {}".format(sorted_list))
    #print("============================")
    #print("The highest 5 elements of list (in ascending order) are : " + str(sorted_list[-5:]))


    #largest_cc = max(nx.connected_components(G), key=len)
    #S = G.subgraph(largest_cc).copy()
    #print("Number of nodes for connected subgraph component S: {}".format(S.number_of_nodes()))
    #print(S)

    log2file('Logging all nodes for each connected component', 'info')
    
    for c in sorted(nx.connected_components(G), key=len, reverse=True): 
        S = G.subgraph(c).copy()
        logline = print(list(S.nodes()))
        log2file(logline, 'info')
        logline = print("Number of nodes for connected subgraph component S: {}".format(S.number_of_nodes()))
        log2file(logline, 'info')


    print("Starting to plot ...")
    plt.axis("off")
    plt.show()
    logging.info('Finished')

