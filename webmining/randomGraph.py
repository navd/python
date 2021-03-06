# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 19:40:10 2016

@author: hp
"""
import csv
import re
import matplotlib.pyplot as plt
import networkx as nx
from operator import itemgetter
from networkx.algorithms import bipartite
from networkx.utils import (powerlaw_sequence, create_degree_sequence)
#from igraph import Graph, mean
import numpy as nm

#G=nx.gnm_random_graph(2939,30501,directed=True)
D = nx.gnr_graph(49, 0.09083)  # the GNR graph
G = D.to_undirected()  # the undirected version


#nx.draw_random(G1)
print(bipartite.is_bipartite(G))
d = nx.degree(G)
nx.draw(G, nodelist=d.keys())
#nx.draw(G, nodelist=d.keys(), node_size=[v * 20 for v in d.values()])
#plt.savefig("./random/sameNodesize.png")
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



pager=nx.pagerank(G)
print('Page rank',pager )

plt.bar(range(len(pager)), pager.values(), align='center')
plt.xticks(range(len(pager)), pager.keys())
plt.show()

centrality = nx.eigenvector_centrality(G,100000)
print(['%s %0.2f'%(node,centrality[node]) for node in centrality])
#plt.plot(node,centrality[node])

plt.bar(range(len(centrality)), centrality.values(), align='center')
plt.xticks(range(len(centrality)), centrality.keys())
plt.show()

#plt.savefig("./assignment3/eigenvectorcentralityRG.png")
kz=nx.katz_centrality_numpy(G,0.62)
print('Katz centrality', kz)
plt.bar(range(len(kz)), kz.values(), align='center')
plt.xticks(range(len(kz)), kz.keys())
plt.show()

loops = G.selfloop_edges()
# remove parallel edges and self-loops
graph = nx.Graph(G)
graph.remove_edges_from(loops)
# get largest connected component
# unfortunately, the iterator over the components is not guaranteed to be sorted by size
components = sorted(nx.connected_components(graph), key=len, reverse=True)
lcc = graph.subgraph(components[0])
pos=nx.spring_layout(lcc)
d = nx.degree(lcc)
#nx.draw(lcc, nodelist=d.keys(), node_size=[v * 20 for v in d.values()])
#nx.draw_networkx_labels(lcc,pos=nx.spring_layout(lcc))
#plt.show()
# code for histogram

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
nx.draw_networkx_nodes(Gcc,pos,node_size=20)
nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

plt.savefig("./USA/degree_histogram_usa.png")
plt.show()
print(nx.average_neighbor_degree(G, source='in', target='in'))

