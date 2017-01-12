import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

plt.rcParams["font.size"] = 10

plt.figure(figsize=(8,3))

ax = plt.subplot(121)
x = np.arange(0,10,0.001)
ax.plot(x, np.sin(np.sinc(x)), 'r', lw=2)

ax = plt.subplot(122)
G = nx.random_geometric_graph(200,0.125)
pos=nx.spring_layout(G)
nx.draw_networkx_edges(G, pos, alpha=0.2)
nx.draw_networkx_nodes(G, pos, node_color='r', node_size=10, edge_color='g')

plt.show()