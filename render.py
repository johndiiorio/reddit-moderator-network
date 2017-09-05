import pickle
import graphviz

with open('out/graph.pickle', 'rb') as pickle_file:
    graph = pickle.load(pickle_file)


def render(g, name, output_format):
    node_attr = {'color': 'red', 'shape': 'circle'}
    edge_attr = {'len': '8'}
    graph_attr = {'overlap': 'false'}
    gv_graph = graphviz.Digraph(name, engine='neato', node_attr=node_attr, edge_attr=edge_attr, graph_attr=graph_attr)
    for node in g.nodes_iter():
        gv_graph.node(node)
    for from_node, to_node in g.edges_iter():
        weight = str(g[to_node][from_node]['weight'])
        gv_graph.edge(from_node, to_node, weight=weight)
    with open(f'out/{name}.{output_format}', 'wb') as graph_file:
        graph_file.write(gv_graph.pipe(output_format))


render(graph, 'graph', 'png')
