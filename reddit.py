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

with open('popular-subreddits.txt') as f:
    popular_subreddits = f.readlines()
popular_subreddits = set([x.strip() for x in popular_subreddits])


def get_subreddit_moderators(subreddit):
    if subreddit not in subreddit_moderators:
        moderators = list(map(lambda mod: mod.name, reddit.subreddit(subreddit).moderator()))
        # Edge case
        try:
            moderators.remove('AutoModerator')
        except:
            pass
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
