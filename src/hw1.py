import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab

G = nx.Graph()
G.add_edges_from([('1','2'),('1','4'),('2','3'),('2','4'),('3','4'),('4','5'),('5','6'),('5','7'),('6','7')])  # create the graph 
print G.nodes(), '\n', G.edges(), '\n', G.degree().values()  # check graph is correct


adj = nx.adj_matrix(G)
print "adjency matrix: \n", adj.todense() # print adjency matrix
k_ij = np.outer(G.degree().values(), G.degree().values())
mod = adj - k_ij / (2.*len(G.edges()))
print "modularity matrix: \n", mod

# suppose we only have 2 communities, we can iterate all the possible situations
# and get the optimum partition
modval_opt = -100000
z_opt = np.zeros((len(G.nodes()), 2))
for i in range(0, 2**(len(G.nodes())-1)):   # iterate all the possible membership
    partition = np.matrix(map(int, list('{0:07b}'.format(i))))  # get a membership vector directly from the bits of an interger
                                                                # e.g. i = 2, list('{0:07b}'.format(i)) will give a list 
                                                                # ['0', '0', '0', '0', '0','1','0']
                                                                # map(int, list) will change it to be a int list [..., 1, 0]
    Z = np.transpose(np.concatenate((partition, 1-partition)))  # this is a 7x2 membership matrix
#    print Z, "\n"
    modval_partition = np.trace(Z.transpose() * mod * Z) / (2*len(G.edges()))
    if modval_opt < modval_partition:
        modval_opt = modval_partition
        z_opt = Z
        
print "\n optimal community membership: \n", z_opt, "\n corresponds to maximum modularity value:\n", modval_opt


# print the graph with community in different color and node size propotional to
# its degree
plt.figure(figsize=(8,6))
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color=np.array(z_opt.transpose())[0], 
    node_size=400*np.array(G.degree().values()), alpha=0.8, linewidths=0)
labels = {}
for node in G.nodes():
    labels[node] = r'$'+node+'$'
    
nx.draw_networkx_labels(G, pos, labels, font_size=24)
nx.draw_networkx_edges(G, pos, width=16, edge_color='g', alpha=0.5)

plt.axis('off')
plt.show()


# for problem 3, to plot your facebook network. For me you can clearly see my
#friends is divided into 2 communities.

import codecs

with codecs.open('myFacebook.gml','r', 'utf8') as f:        # don't use networkx.read_gml() functions, it will have
    lines = f.readlines()                                   # UnicodeDecodeError, use these three lines to load gml
    fbG = nx.readwrite.gml.parse_gml(lines, relabel=True)   # into a networkx graph
    
plt.figure(figsize=(18,12))

pos = nx.spring_layout(fbG)
gender = []
wallcount = []
ids = {}
deg = []
DegDict = fbG.degree()

for name,attr in fbG.node.iteritems():
    gender.append(0 if attr['sex'] == 'male' else 1)
    wallcount.append(attr['wallcount'])
    ids[name] = attr['id']
    deg.append(DegDict[name])
    
nx.draw_networkx_nodes(fbG, pos, node_color=gender, node_size=200+40*np.array(deg), 
                       alpha=0.8, linewidths=0)
nx.draw_networkx_edges(fbG, pos, width=1.8, edge_color='black', alpha=0.3)
nx.draw_networkx_labels(fbG, pos, labels=ids, font_size=14, font_family='DejaVu Sans')  # remove labels=ids will use name as labels


plt.axis('off')
plt.show()