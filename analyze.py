import pickle
import networkx as nx
from collections import OrderedDict
from operator import itemgetter

with open('out/graph.pickle', 'rb') as pickle_file:
    graph = pickle.load(pickle_file)


def top_from_dict(d, num=10):
    for k, v in list(OrderedDict(sorted(d.items(), key=itemgetter(1), reverse=True)).items())[:num]:
        print(k, v)
    print()


print(f'Number of nodes: {nx.number_of_nodes(graph)}\n')
print(f'Number of edges: {nx.number_of_edges(graph)}\n')

print('Top 10 nodes with most degrees:')
top_from_dict(nx.degree(graph))

print('Top 10 nodes with highest degree centrality:')
top_from_dict(nx.degree_centrality(graph))

print('Top 10 nodes with highest eigenvector centrality')
top_from_dict(nx.eigenvector_centrality_numpy(graph))

print('Top 10 nodes with highest betweenness centrality')
top_from_dict(nx.betweenness_centrality(graph))
