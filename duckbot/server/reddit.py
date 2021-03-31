import urllib.request
import ujson

subreddit = "jokes"
response = urllib.request.urlopen(f"https://www.reddit.com/r/{subreddit}/hot/.json").read()

data = ujson.loads(response)["data"]["children"]

new_data = []
for post in data:
    if post["data"]["stickied"]:
        continue

def get_hot_posts(subreddit, count=25):

    # need to define a user agent so reddit doesn't rate limit us
    request = urllib.request.Request(
        f"https://www.reddit.com/r/{subreddit}/hot/.json?count={count}", 
        data=None, 
        headers={
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        }
    )

    # read json data and parse into a dict
    json_string = urllib.request.urlopen(request).read()
    posts = ujson.loads(json_string)["data"]["children"]

    # pull only the relevant information and ignore sticky posts
    data = []
    for post in posts:
        if post["data"]["stickied"]:
            continue
        else:
            data.append({
                "id": post["data"].get("name"),
                "title": post["data"].get("title"),
                "text": post["data"].get("selftext"),
                "url": post["data"].get("url")
            })

    return data


a = get_hot_posts("djdjdjdjdjdd", count=10)
print(a)

from discord.ext import commands

class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="joke")
    async def joke(self, context, *args):
        await context.send(response)
