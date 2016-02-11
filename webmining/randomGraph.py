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


#print(G1.edges())
print(nx.diameter(G, e=None))# graph not connected
print(nx.density(G))
print("clustering coefficient",nx.average_clustering(G))
print("average degree ", nm.mean(G.degree()))
print("AVG",nx.average_shortest_path_length(G))

#nx.draw_random(G1)
print(bipartite.is_bipartite(G))
d = nx.degree(G)
nx.draw(G, nodelist=d.keys())
#nx.draw(G, nodelist=d.keys(), node_size=[v * 20 for v in d.values()])
#plt.savefig("./random/sameNodesize.png")
plt.show()

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

