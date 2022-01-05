Script GE3_BNP51_Q2.py to solve Q2 of GE3

- usage call: "python  ./GE3_BNP51_Q2.py --nodes <number_of_nodes>"
    - number_of_nodes = the number of nodes each network will have 

python packages required: matplot lib, numpy, networkx

Both networks are drawn side-by-side in one page for comparison.
- On the left side the small-world network
- On the right side the scale-free (barabasi-albert) network

Parameters used:
- Nodes: 50 for both
- Small-world is using k=4 nearest neighbors for each node and probability p=0.5 (For any existing (u,v) edge, p is the probability to select a new node w, randomly and rewiring, so that edge becomes (u,w)). It seems that for an intermediate value of p, we would get an ideal Small World Network with small average distance and high clustering. A small world network is characterized by a small average shortest path length, and a large clustering coefficient.
- Scale Free using Barabasi-Albert algorithm construct a scale-free 
	- a minority of modes have the majority of edges
        - degree distibution folows power law
        - uses a preferential attachment process thats is edges are distibuted anong nodews according to how much thay already (the rich get richer)  
     
