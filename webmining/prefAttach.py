# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 14:15:49 2016

@author: navdeep
"""

#import csv
#import re
import matplotlib.pyplot as plt
import networkx as nx
#from operator import itemgetter
from networkx.algorithms import bipartite
#from networkx.utils import (powerlaw_sequence, create_degree_sequence)
import numpy as nm
#import plotly.plotly as py



G=nx.barabasi_albert_graph(49,4)

#print(G1.edges())
#print(nx.diameter(G1, e=None))# graph not connected
#nx.draw_random(G1)
print(bipartite.is_bipartite(G))
d = nx.degree(G)
#nx.draw(G, nodelist=d.keys())
#print(nx.diameter(G, e=None))
nx.draw(G, nodelist=d.keys(), node_size=[v * 20 for v in d.values()])
plt.savefig("plotprefAttach.png")
plt.show()
print('diameter ',nx.diameter(G, e=None))# graph not connected
print('debsity', nx.density(G))
print("clustering coefficient",nx.average_clustering(G))
#print("average degree ", nm.mean(G.degree()))
print("AVG",nx.average_shortest_path_length(G))
print(" Clique ",len(list(nx.find_cliques(G))))

L = nx.normalized_laplacian_matrix(G)
e = nm.linalg.eigvals(L.A)

print("Largest eigenvalue:", max(e))
print("Smallest eigenvalue:", min(e))

centrality = nx.eigenvector_centrality(G)
print(['%s %0.2f'%(node,centrality[node]) for node in centrality])
#plt.plot(node,centrality[node])

plt.bar(range(len(centrality)), centrality.values(), align='center')
plt.xticks(range(len(centrality)), centrality.keys())
plt.show()
pager=nx.pagerank(G)
print('Page rank',pager )

plt.bar(range(len(pager)), pager.values(), align='center')
plt.xticks(range(len(pager)), pager.keys())
plt.show()

kz=nx.katz_centrality_numpy(G,0.62)
print('Katz centrality', kz)
plt.bar(range(len(kz)), kz.values(), align='center')
plt.xticks(range(len(kz)), kz.keys())
plt.show()

#plt.savefig("eigenvectorcentralityPA.png")

#print(nx.degree_centrality(G))
#code for degree distribution

degree_sequence=sorted(nx.degree(G).values(),reverse=True)
dmax=max(degree_sequence)
plt.loglog(degree_sequence,'b-',marker='o')
plt.title("Degree rank plot")
plt.ylabel("degree")
plt.xlabel("rank")
plt.axes([0.45,0.45,0.45,0.45])
Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
pos=nx.spring_layout(Gcc)
plt.axis('off')
print("Diameter", nx.diameter(Gcc, e=None))
nx.draw_networkx_nodes(Gcc,pos,node_size=20)
nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

#plt.savefig("degreeprefAttach.png")
plt.show()
#print(nx.average_neighbor_degree(G, source='in', target='in'))

