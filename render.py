import pickle
import graphviz

with open('out/popular-subreddits.pickle', 'rb') as pickle_file:
    graph_popular_subreddits = pickle.load(pickle_file)

with open('out/popular-subreddits5000.pickle', 'rb') as pickle_file:
    graph_popular_subreddits5000 = pickle.load(pickle_file)


def render(graph, name, output_format):
    node_attr = {'color': 'red', 'shape': 'circle'}
    edge_attr = {'len': '8'}
    graph_attr = {'overlap': 'false'}
    gv_graph = graphviz.Graph(name, engine='neato', node_attr=node_attr, edge_attr=edge_attr, graph_attr=graph_attr)
    for node in graph.nodes_iter():
        gv_graph.node(node)
    for from_node, to_node in graph.edges_iter():
        gv_graph.edge(from_node, to_node)
    with open(f'out/{name}.{output_format}', 'wb') as graph_file:
        graph_file.write(gv_graph.pipe(output_format))

render(graph_popular_subreddits5000, 'graph', 'png')
