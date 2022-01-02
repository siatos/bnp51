"""
Script to solve Q1 for GE3
Usage: python GE3_BNP51_Q1.py -m ppi_matrix.xlsx -n ppi_names.xlsx
"""
from argparse import ArgumentParser
import os
import logging
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from constants import LOGFILE, SIZE_OF_NODESLIST

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
    """
    Read an excel file and return a list of values
    The output of read is a pandas dataframe(df) that is converted into a list
    """
    df = pd.read_excel(fname, index_col=None, header=None)
    #print(df)
    value_list = df.values.tolist()
    #value_dict = df.to_dict()
    return value_list

def log2file(log_line, loglevel):
    """
    Simple logging facility. Possible an overkill here.
    """
    if loglevel.lower() == 'debug':
        logging.debug(log_line)
    elif loglevel.lower() == 'error':
        logging.error(log_line)
    elif loglevel.lower() == 'info':
        logging.info(log_line)
    else:
        logging.info('incoherent loglevel: ' + log_line)


def create_gene_dict(node_list, adj_matrix):
    """
    Read data from a list of nodes and its adjacency matrix (represented here as a list of rows
    and return a dictionary of nodes (each key is a node) and the number of nodes (a row having 1's and/or 0's )
    The dict should have a form like:
      Gene_x:[0, 1, ..., 1] 300 elements in each list. There will be 300 keys (genes) in the dictionary.
      To create the dictionary iterate through the two lists  created form tables (matrix and names) at the same time.
      There is no checking for incosistencies. Data are assumed to be correct.
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

    print("here")
    print(node_list)

    # iterate through the two lists simultaneously
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
         n: size of list, i.e. return only the top n nodes
    :return:
        degree_list: list of nodes sorted on their degree descending order
    """
    degree_list = list(Grph.degree())
    sorted_list = sorted(degree_list, key=take_second, reverse=True)
    #print("Degree for each node: {}".format(sorted_list))
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
    SGrph = sorted(nx.betweenness_centrality(Grph).items(), key=lambda item: item[1], reverse=True)
    print("The highest {} elements of list (betweeness centrality in descending order) are : {}".format(n, str(SGrph[:n])))
    return SGrph[:n]

def take_second(elem):
    """
    used to return the second element of an (element) tuple
    i could not make lambda expression work properly, sad ...
    """
    return elem[1]


if __name__ == '__main__':
    LOGFILE="log.txt"
    # remove possibly existing log file
    if os.path.isfile(LOGFILE):
        print("Removing file {}".format(LOGFILE))
        os.remove(LOGFILE)
    else:    # if there is no logfile display it and continue 
        print("{} file not found, ... it will be created, ok".format(LOGFILE))

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

    # add the nodes, all nodes will be in the form Gene_n, where n some integer
    for node in gene_dict:
        # print("Adding Node: {}".format(node))
        G.add_node(str(node))

    print("graph created with {} nodes".format(G.number_of_nodes()))

    # add the edges
    for node in gene_dict:
        # for each node create a list with the pos of nonzero elements of each row
        nonzero_vals = [i for i,x in enumerate(gene_dict[node]) if x == 1]
        end_nodes = []
        # find end node from pos in the list
        for pos in nonzero_vals:
            end_node = 'Gene_'+ str(nodes_list[pos][0])
            #print(end_node)
            end_nodes.append(end_node)
            #print("{} {}".format(nodes_list[pos][0], type(nodes_list[pos][0])))
            #G.add_edge(node, end_node)
        # print("found for node {} following nodes {}".format(node, end_nodes))
        for endnode in end_nodes:
            #we re usning undirected graphs so direction is not important
            if G.has_edge(node, endnode) or G.has_edge(endnode, node):
                print("Edge from {} to {} exists no adding".format(node, endnode))
            else:
                print("Adding Edge from {} to {} ".format(node, endnode))
                G.add_edge(node, endnode)



    #nx.draw_circular(G, with_labels=True)
    nx.draw(G, with_labels=True)

    print("============================ HIGHEST DEGREE NODES ===============================")
    print("Find Degree for each node ... show the highest {} nodes".format(SIZE_OF_NODESLIST))
    get_nodes_by_degree(G, SIZE_OF_NODESLIST)
    print("=================================================================================")


    print("======================== HIGHEST BETWENESS CENTRALITY NODES =====================")
    print("Find betweeness centrality ...show the highest {} nodes".format(SIZE_OF_NODESLIST))
    get_betweenness_centrality(G, SIZE_OF_NODESLIST)
    print("==================================================================================")


    log2file('Logging all nodes for each connected component', 'info')

    connected_components_count = 0
    for c in sorted(nx.connected_components(G), key=len, reverse=True):
        S = G.subgraph(c).copy()
        connected_components_count += 1
        logline = "for subgraph S with {} nodes: {}".format(S.number_of_nodes(), list(S.nodes()))
        log2file(logline, 'info')

    print("============================ CONNECTED COMPONENTS ================================")
    print("Found {} connected components ".format(connected_components_count))
    print("==================================================================================")

    print("Starting to plot ...")
    plt.axis("off")
    plt.show()
    logging.info('Finished')
