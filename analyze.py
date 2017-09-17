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


degree_centrality = sort_dict_by_key(nx.degree_centrality(graph))
betweeness_centrality = sort_dict_by_key(nx.betweenness_centrality(graph))
closeness_centrality = sort_dict_by_key(nx.closeness_centrality(graph))
eigenvector_centrality = sort_dict_by_key(nx.eigenvector_centrality_numpy(graph))

d_c_dict = dict(degree_centrality)
b_c_dict = dict(betweeness_centrality)
c_c_dict = dict(closeness_centrality)
e_c_dict = dict(eigenvector_centrality)

scores = []
for el in zip(d_c_dict, b_c_dict, c_c_dict, e_c_dict):
    username = el[0]
    scores.append((username, get_node_score(d_c_dict[username], b_c_dict[username], c_c_dict[username], e_c_dict[username])))


with open('out/analysis.csv', 'w') as output_file:
    header = 'username, score, degree centrality, betweeness centrality, closeness centrality, eigenvector centrality\n'
    output_file.write(header)
    for i, j in sorted(scores, key=lambda x: x[1]):
        output_file.write(f'{i},{j},{d_c_dict[i]},{b_c_dict[i]},{c_c_dict[i]},{e_c_dict[i]}\n')
