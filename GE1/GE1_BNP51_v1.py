#!/usr/bin/python
import networkx as nx
import matplotlib.pyplot as plt

# Define an input filename.
filename = "input.txt"

with open(filename) as f:
    data = f.read().splitlines()


gene_dict = {} #Initialize a dictionary
count = 1
# fill dict, each key is a list of 0/1
for line in data:
    x = "Gene_" + str(count)    
    gene_dict[x] = line.split()
    count +=1

print("================================================")
print("Genes:")
print(gene_dict)
print("================================================")


#print("Create a new dict to store Going In(GI) and Going Out(GO) values for each node")
GI_GO = {}
# for each key in the dict read related pos i.e Gene_1 maps to pos 0, Gene to pos 1 etc i.e. read the columns iand find nonzero items this is GI 
for x in gene_dict:
   count = 0
   #pos in each list starts from 0 not 1
   pos = int(str(x).replace('Gene_', '')) - 1
   for y in gene_dict:
      if int(gene_dict[y][pos]) == 1:
          count +=1
          GI_GO[x] = [count]

for x in gene_dict:
   #arr = list(map(int, gene_dict[x]))
   # a rather complicated way: convert each list into a list of ints then filter nonzero elements of the list and find the length of the new list, this is GO
   result = len(list(filter(lambda x: x != 0, list(map(int, gene_dict[x])))))
   # append value to GI_Go dictionary
   GI_GO[x].append(result)

print("================================================")
print("Going In(GI) and Going Out(GO) values for each node")
print(GI_GO)
print("================================================")

#print("")
#print("Create a Di(rected) Graph object, adding nodes and edges")
#print("")

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
#

# 
print("Starting to plot ...")
plt.axis("off")
plt.show()
