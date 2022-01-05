Script GE3_BNP51_Q3.py to solve Q3 of GE3
- call usage : python  ./GE3_BNP51_Q3.py -s1 "size1"  -s2 "size2" 
  - where s1="size1", s2="size2" are the sizes of the
    subgraphs. As long as s1+s2 < 20 program will assign
the rest to the 3rd subgraph

python packages required: matplotlib, networkx
    
The idea is to create 3 distinct (sub)graphs and then connect these with a minimum of 2 edges to create a graph that has a single connected component but can be easily dismantled into 3 distinct connected components by removing appropriate edges.
