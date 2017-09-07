import pickle
import networkx as nx
from collections import OrderedDict
from operator import itemgetter
import math

with open('out/graph.pickle', 'rb') as pickle_file:
    graph = pickle.load(pickle_file)


def top_from_dict(d, reverse=True, num=10):
    for k, v in list(OrderedDict(sorted(d.items(), key=itemgetter(1), reverse=reverse)).items())[:num]:
        print(k, v)
    print()


def sort_dict_by_key(d):
    return ((k, v) for k, v in sorted(d.items(), key=lambda item: item[0]))


def get_node_score(degree, betweenness, closeness, eigenvector):
    return math.sqrt((1 - degree)**2 + (1 - betweenness)**2 + (1 - closeness)**2 + (1 - eigenvector)**2)


print(f'Number of nodes: {nx.number_of_nodes(graph)}\n')
print(f'Number of edges: {nx.number_of_edges(graph)}\n')

degree_centrality = sort_dict_by_key(nx.degree_centrality(graph))
betweeness_centrality = sort_dict_by_key(nx.betweenness_centrality(graph))
closeness_centrality = sort_dict_by_key(nx.closeness_centrality(graph))
eigenvector_centrality = sort_dict_by_key(nx.eigenvector_centrality_numpy(graph))

scores = []
for d, b, c, e in zip(degree_centrality, betweeness_centrality, closeness_centrality, eigenvector_centrality):
    scores.append((d[0], get_node_score(d[1], b[1], c[1], d[1])))

for i, j in sorted(scores, key=lambda x: x[1]):
    print(i, j)

print('Top 10 nodes with highest degree centrality:')
print(top_from_dict(degree_centrality))

print('Top 10 nodes with highest betweenness centrality')
print(top_from_dict(betweeness_centrality))

print('Top 10 nodes with highest closeness centrality:')
print(top_from_dict(closeness_centrality))

print('Top 10 nodes with highest eigenvector centrality')
print(top_from_dict(eigenvector_centrality))
