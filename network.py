import queue
import networkx as nx
import pickle
from reddit import get_subreddit_moderators, get_user_moderated_subreddits


def breath_first_search(start):
    graph = nx.Graph()
    graph.add_node(start)
    q = queue.Queue()
    q.put(start)
    visited = set()
    while not q.empty():
        u = q.get()
        if u not in visited:
            user_moderated_subreddits = get_user_moderated_subreddits(u)
            for subreddit in user_moderated_subreddits:
                for user in get_subreddit_moderators(subreddit):
                    if u != user:
                        graph.add_edge(u, user, subreddit=subreddit)
                        q.put(user)
        visited.add(u)
        print("Queue size after loop: {}".format(q.qsize()))
        if q.qsize() > 100000:
            break
    return graph

graph_popular_subreddits = breath_first_search('BWPhoenix')
with open('out/popular-subreddits.pickle', 'wb') as pickle_file:
    pickle.dump(graph_popular_subreddits, pickle_file)
