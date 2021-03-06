
import discord
import praw
import time
import os
import requests
import json
import config
intents = discord.Intents.all()
client = discord.Client(intents=intents)
token = open("token.txt", "r").read()


def bot_login():
    print("Loggin in.")
    r = praw.Reddit(username=config.username, password=config.password, client_id=config.client_id,  # reddit login
                    client_secret=config.client_secret, user_agent=config.user_agent)
    print("Logged in.")
    return r


r = bot_login()


def run_bot(r):
    for sub in config.subreddits:
        submissions = r.subreddit(sub).hot(limit=config.limit)
        for submission in submissions:
            if submission not in blacklist:
                if submission.is_self == False and submission.is_video == False:
                    if submission.score > 5000:
                        data = {}
                        data["embeds"] = []
                        embed = {
                            "title": config.embed_title,
                            "author": {
                                "name": "posted by u/{} at r/{}".format(str(submission.author), str(submission.subreddit)),
                                "url": "https://reddit.com/r/{}/comments/{}".format(str(submission.subreddit), str(submission)),
                                "icon_url": submission.author.icon_img
                            },
                            "image": {
                                "url": submission.url
                            },
                            "fields": [
                                {
                                    "name": "Post Title",
                                    "value": submission.title,
                                    "inline": False
                                },
                                {
                                    "name": "Author",
                                    "value": "u/{}".format(str(submission.author)),
                                    "inline": True
                                },
                                {
                                    "name": "Subreddit",
                                    "value": "r/{}".format(str(submission.subreddit)),
                                    "inline": True
                                },
                                {
                                    "name": "Score",
                                    "value": submission.score,
                                    "inline": False
                                }
                            ]
                        }
                        data["embeds"].append(embed)

                        req = requests.post(config.webhook_url, data=json.dumps(
                            data), headers={"Content-Type": "application/json"})

                        if req.status_code == 204:
                            print(
                                "Found new hot Reddit post, sending it to Discord.")

                        blacklist.append(submission)
                        with open("blacklist.txt", "a") as f:
                            f.write(str(submission) + "\n")
                            # f.close()

                        time.sleep(config.wait_time)
                        run_bot(r)


# def outriders(r):
#     for sub in config.outriders:
#         submissions = r.subreddit(sub).hot(limit=config.limit)
#         for submission in submissions:
#             if submission not in blacklist:
#                 if submission.is_self == False and submission.is_video == False:
#                     if submission.score > 900:
#                         data = {}
#                         data["embeds"] = []
#                         embed = {
#                             "title": config.embed_title,
#                             "author": {
#                                 "name": "posted by u/{} at r/{}".format(str(submission.author), str(submission.subreddit)),
#                                 "url": "https://reddit.com/r/{}/comments/{}".format(str(submission.subreddit), str(submission)),
#                                 "icon_url": submission.author.icon_img
#                             },
#                             "image": {
#                                 "url": submission.url
#                             },
#                             "fields": [
#                                 {
#                                     "name": "Post Title",
#                                     "value": submission.title,
#                                     "inline": False
#                                 },
#                                 {
#                                     "name": "Author",
#                                     "value": "u/{}".format(str(submission.author)),
#                                     "inline": True
#                                 },
#                                 {
#                                     "name": "Subreddit",
#                                     "value": "r/{}".format(str(submission.subreddit)),
#                                     "inline": True
#                                 },
#                                 {
#                                     "name": "Score",
#                                     "value": submission.score,
#                                     "inline": False
#                                 }
#                             ]
#                         }
#                         data["embeds"].append(embed)

#                         req = requests.post(config.outriders_webhook_url, data=json.dumps(
#                             data), headers={"Content-Type": "application/json"})

#                         if req.status_code == 204:
#                             print(
#                                 "Found new hot Reddit post, sending it to Discord.")

#                         blacklist.append(submission)
#                         with open("blacklist.txt", "a") as f:
#                             f.write(str(submission) + "\n")
#                             # f.close()

#                         time.sleep(config.wait_time)
#                         # print('Functions are calling themselves every 3 mins')
#                         # outriders(r)


def blacklisted_posts():
    if not os.path.isfile("blacklist.txt"):
        blacklist = []
    else:
        with open("blacklist.txt", "r") as f:
            blacklist = f.read()
            blacklist = blacklist.split("\n")
            # f.close()

    return blacklist


blacklist = blacklisted_posts()

while True:
    run_bot(r)
    outriders(r)
    time.sleep(60)
    True
