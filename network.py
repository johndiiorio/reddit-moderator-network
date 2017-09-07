import queue
import networkx as nx
import pickle
from reddit import get_subreddit_moderators, get_user_moderated_subreddits


def breath_first_search(start):
    graph = nx.DiGraph()
    graph.add_node(start)
    q = queue.Queue()
    q.put(start)
    visited = set()
    while not q.empty():
        u = q.get()
        if u not in visited:
            user_moderated_subreddits = get_user_moderated_subreddits(u)
            for subreddit in user_moderated_subreddits:
                moderators = get_subreddit_moderators(subreddit)
                for user in moderators:
                    if u != user[0] and not (u in graph and user[0] in graph[u] and graph[u][user[0]]['weight'] > user[1]):
                        graph.add_edge(u, user[0], attr_dict={"subreddit": subreddit, "weight": user[1]})
                        q.put(user[0])
        visited.add(u)
        print("Queue size after loop: {}".format(q.qsize()))
    return graph


network_graph = breath_first_search('BWPhoenix')
with open('out/graph.pickle', 'wb') as pickle_file:
    pickle.dump(network_graph, pickle_file)
