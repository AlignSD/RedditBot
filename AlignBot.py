# CLIENT ID 778863238803619860
# 75840
# permissions int 215104
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

# @client.event # event decorator/wrappe check it out on pythonprogramming.net for a guide if needed
#async def on_ready():
#    print(f"we have logged in as {client.user}")


# @client.event
# async def on_message(message):
#     print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
#     my_guild = client.get_guild(173896742884999168)
# 
#     if "wowbot.member_count()" == message.content.lower():
#         await message.channel.send(f"```py\n{my_guild.member_count}```")
# 
#     elif"wowbot.community_report()" == message.content.lower():
#         online = 0
#         idle = 0
#         offline = 0
# 
#         for m in my_guild.members:
#             if str(m.status) == "online":
#                 online += 1
#             elif str(m.status) == "offline":
#                 offline += 1
#             else: 
#                 idle += 1
# 
#         await message.channel.send(f"```Online: {online}.\nIdle/busy/dnd: {idle}.\nOffline: {offline}```")
# 
#     elif "!search" in message.content.lower():
#         await message.channel.send("What would you like to search for?")
# 
#     elif "get outta here!!" in message.content.lower():
#         await message.channel.send("fuck off bitch")
#         await client.close()
#         sys.exit()
def bot_login():
    print("Loggin in.")
    r = praw.Reddit(username = config.username, password = config.password, client_id = config.client_id, client_secret = config.client_secret, user_agent = config.user_agent)
    print("Logged in.")
    return r

def run_bot(r):
    for sub in config.subreddits:
        submissions = r.subreddit(sub).hot(limit = config.limit)
        for submission in submissions:
            if submission not in blacklist:
                if submission.is_self == False and submission.is_video == False:                    
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

                    req = requests.post(config.webhook_url, data = json.dumps(data), headers={"Content-Type": "application/json"})
                    
                    if req.status_code == 204:
                        print("Found new hot Reddit post, sending it to Discord.")
                
                    blacklist.append(submission)
                    with open("blacklist.txt", "a") as f:
                        f.write(str(submission) + "\n")
                        f.close()

                    time.sleep(config.wait_time)

def outriders(r):
    for sub in config.outriders:
        submissions = r.subreddit(sub).hot(limit = config.limit)
        for submission in submissions:
            if submission not in blacklist:
                if submission.is_self == False and submission.is_video == False:                    
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

                    req = requests.post(config.outriders_webhook_url, data = json.dumps(data), headers={"Content-Type": "application/json"})
                    
                    if req.status_code == 204:
                        print("Found new hot Reddit post, sending it to Discord.")
                
                    blacklist.append(submission)
                    with open("blacklist.txt", "a") as f:
                        f.write(str(submission) + "\n")
                        f.close()

                    time.sleep(config.wait_time)


def blacklisted_posts():
    if not os.path.isfile("blacklist.txt"):
        blacklist = []
    else:
        with open("blacklist.txt", "r") as f:
            blacklist = f.read()
            blacklist = blacklist.split("\n")
            f.close()

    return blacklist

r = bot_login()
blacklist = blacklisted_posts()
while True:
    run_bot(r)
    outriders(r)  
    client.run(token)
 