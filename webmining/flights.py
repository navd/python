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


G=nx.DiGraph()


with open('/home/navdeep/python/data/out.opsahl-openflights', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
            nodes=re.split(r' +', row[0])
            G.add_edge(nodes[0],nodes[1])

'''
#print(G1.edges())
#print(nx.diameter(G1, e=None))# graph not connected
#nx.draw_random(G1)
print(bipartite.is_bipartite(G))
d = nx.degree(G)
#nx.draw(G, nodelist=d.keys())
nx.draw(G, nodelist=d.keys(), node_size=[v * 20 for v in d.values()])
plt.savefig("sameNodesize.png")
plt.show()
'''

loops = G.selfloop_edges()
# remove parallel edges and self-loops
graph = nx.Graph(G)
graph.remove_edges_from(loops)
# get largest connected component
# unfortunately, the iterator over the components is not guaranteed to be sorted by size
components = sorted(nx.connected_components(graph), key=len, reverse=True)
lcc = graph.subgraph(components[0])
print(nx.density(lcc))
print(nx.number_of_nodes(lcc))
print(nx.number_of_nodes(G))
print(nx.degree_histogram(G))
print(lcc)
pos=nx.spring_layout(lcc)
d = nx.degree(lcc)
#nx.draw(lcc, nodelist=d.keys(), node_size=[v * 20 for v in d.values()])
#nx.draw_networkx_labels(lcc,pos=nx.spring_layout(lcc))
#plt.show()
# code for histogram

degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence
#print "Degree sequence", degree_sequence
dmax=max(degree_sequence)
print(dmax)
plt.hist(degree_sequence,bins=dmax)
plt.title("Degree histogram")
plt.ylabel("count")
plt.xlabel("degree")
plt.axes([0.45,0.45,0.45,0.45])
#Gc = max(nx.connected_component_subgraphs(G), key=len)
#Gcc=nx.connected_component_subgraphs(G)[0]


loops = G.selfloop_edges()
# remove parallel edges and self-loops
graph = nx.Graph(G)
graph.remove_edges_from(loops)
# get largest connected component
# unfortunately, the iterator over the components is not guaranteed to be sorted by size
components = sorted(nx.connected_components(graph), key=len, reverse=True)
lcc = graph.subgraph(components[0])
pos=nx.spring_layout(lcc)
plt.axis('off')

nx.draw_networkx_nodes(lcc,pos,node_size=20)
nx.draw_networkx_edges(lcc,pos,alpha=0.4)

plt.savefig("degree_histogram.png")
plt.show()

