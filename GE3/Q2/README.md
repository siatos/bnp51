# script GE3_BNP51_Q2.py to solve Q2 of GE3
# call: python  ./GE3_BNP51_Q2.py --nodes <number_of_nodes>
        number_of_nodes = the number of nodes each networl will have 
Both networks are drawn side-by-side in one pgae for comparison.
- On the left side the small-world network
- On the right side the scale-free (barabasi-albert) network

Parameters used:
- Nodes: 50 for both
- Small-world is using k=4 nearest nwighbors for each node and probability p=0.5 (For any existing (u,v) edge, p is the prbability to select a new node w randomly and rewiring so that edge becomes (u,w)). It seems that for an intermediate value of p, we would get an ideal Small World Network with small average distance and high clustering.  
- Scale-Free is using 
     
