import pickle
import networkx as nx

with open('out/popular-subreddits.pickle', 'rb') as pickle_file:
    graph_popular_subreddits = pickle.load(pickle_file)

print(f'Number of nodes: {nx.number_of_nodes(graph_popular_subreddits)}')
print(f'Number of edges: {nx.number_of_edges(graph_popular_subreddits)}')
