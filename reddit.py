import praw
import requests
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

reddit = praw.Reddit(client_id=os.environ.get("client_id"),
                     client_secret=os.environ.get("client_secret"),
                     username=os.environ.get('username'),
                     password=os.environ.get('password'),
                     user_agent='my user agent')

subreddit_moderators = {}
user_moderated_subreddits = {}
subreddit_size = {}

with open('popular-subreddits.txt') as f:
    popular_subreddits = f.readlines()
popular_subreddits = set([x.strip() for x in popular_subreddits])

largest_subreddit_size = reddit.get('/r/announcements/about.json').subscribers


def get_subreddit_moderators(subreddit):
    if subreddit not in subreddit_moderators:
        moderators = list(map(lambda mod: (mod.name, get_edge_weight(subreddit, mod.mod_permissions)), reddit.subreddit(subreddit).moderator()))
        # Remove AutoModerator edge case
        moderators = list(filter(lambda mod: mod[0] != 'AutoModerator', moderators))
        subreddit_moderators[subreddit] = moderators
        return moderators
    return subreddit_moderators[subreddit]


def get_user_moderated_subreddits(username):
    if username not in user_moderated_subreddits:
        res = requests.get("https://www.reddit.com/user/" + username + "/moderated_subreddits.json", headers={'User-Agent':'Reddit Network Agent'})
        if res.status_code != 200:
            raise Exception('Error requesting user moderated subreddits: Status code {}'.format(res.status_code))
        res_json = json.loads(res.text)
        subreddits = list(map(lambda el: el['sr'], res_json['data']))
        subreddits = list(filter(lambda i: i in popular_subreddits, subreddits))
        user_moderated_subreddits[username] = subreddits
        return subreddits
    return user_moderated_subreddits[username]


def get_subreddit_size(subreddit):
    if subreddit not in subreddit_size:
        size = reddit.get(f'/r/{subreddit}/about.json').subscribers
        subreddit_size[subreddit] = size
        return size
    else:
        return subreddit_size[subreddit]


def get_edge_weight(subreddit, mod_permissions, scalar=100):
    if len(mod_permissions) == 0:
        return 0
    size = get_subreddit_size(subreddit)

    total_possible_points = scalar * size / largest_subreddit_size
    percentage_points = 0
    if 'all' in mod_permissions:
        return total_possible_points
    if 'access' in mod_permissions:
        percentage_points += 20
    if 'config' in mod_permissions:
        percentage_points += 10
    if 'flair' in mod_permissions:
        percentage_points += 5
    if 'mail' in mod_permissions:
        percentage_points += 10
    if 'posts' in mod_permissions:
        percentage_points += 20
    if 'wiki' in mod_permissions:
        percentage_points += 10
    if percentage_points == 0:
        raise Exception(f'Error calculating mod permissions: {mod_permissions}, {subreddit}')
    return percentage_points * total_possible_points / 100
