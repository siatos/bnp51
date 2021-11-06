from argparse import ArgumentParser
import networkx as nx
import matplotlib.pyplot as plt


def parse_input():
    """
    Parse the command line ARGUMENTS
    """
    parser = ArgumentParser()
    parser.add_argument('--file', action='store', help='input txt file)')

    arguments = parser.parse_args()

    return arguments

def read_from_file_to_create_dict(fname):
    """
    Read data from an input file that has rows of 0/1's space delimited
    and return a dictionary of nodes (each key is a node) and the number of nodes (rows in file read)
    :param
         fname: input filename
    :return:
        return_dict: dictionary of nodes
        count: number of nodes
    """
    with open(fname) as f:
        data = f.read().splitlines()
    return_dict = {}
    count = 1
    # fill dict, each key is a list of 0/1
    for line in data:
        x = "Gene_" + str(count)
        return_dict[x] = line.split()
        count +=1
    return return_dict, count

def create_DI_DO(nodes_dict):
    """
    create a dictionary to hold degree in/out for each node
    DI (Degree In:  number of edges that come into  the node i.e. columns in the adjacency matrix)
    DO (Degree Out: number of edges that go out from the node i.e rows in the adjacency matrix)
    :param
         node_dict:
    :return:
        DI_DO_dict: dictionary that  holds DI/Do for each node (keys of dict)
    """
    di_do = {}
    # fill DI values
    for x in nodes_dict:
        count = 0
        #pos in each list starts from 0 not 1
        pos = int(str(x).replace('Gene_', '')) - 1
        for y in nodes_dict:
            if int(nodes_dict[y][pos]) == 1:
                count += 1
                di_do[x] = [count]
    # fill DO values        
    for x in gene_dict:
        result = len(list(filter(lambda x: x != 0, list(map(int, gene_dict[x])))))
        di_do[x].append(result)
    return di_do


if __name__ == '__main__':
    # EXIT_STATUS = 0
    ARGS = parse_input()
    input_fname = str(ARGS.file)
    gene_dict, no_of_nodes = read_from_file_to_create_dict(input_fname)

    print("================================================")
    print("Genes:")
    print(gene_dict)
    print("================================================")

    DI_DO =   create_DI_DO(gene_dict) # create a dictionary to hold degree in/out for each node

    print("================================================")
    print("Going In(GI) and Going Out(GO) values for each node")
    print(DI_DO)
    print("================================================")




    # create a (directed) graph based on above info. An undirected graph could also be used
    G=nx.DiGraph()

    for node in gene_dict:
        #print("Adding Node: {}".format(node))
        G.add_node(str(node))


    for node in gene_dict:
        #print("Node is: {}: {}".format(node, gene_dict[node]))
        for i, val in enumerate(gene_dict[node]):
        #print("pos {} value {}".format(i+1, val)) 
            if int(val):
                end="Gene_"+str(i + 1)
                #print("Adding EDGE: {} {}".format(node,end))
                G.add_edge(node, end)

    print("================================================")
    for nd1 in G.nodes:
        print("==== Finding shortest path from node {} ====".format(nd1))
        for nd2 in G.nodes:
            if nd1 != nd2:
                print("... to node {}: {}".format(nd2, nx.shortest_path(G, source=nd1, target=nd2)))
    print("================================================")



    #nx.draw_networkx(G)
    nx.draw_circular(G, with_labels=True)
    #nx.draw(G)

    print("Starting to plot ...")
    plt.axis("off")
    plt.show()

