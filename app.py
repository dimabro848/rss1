import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from flask import Flask, Response
import snscrape.modules.twitter as sntwitter
from feedgen.feed import FeedGenerator

app = Flask(__name__)

TWITTER_USERNAME = "UPvestorChain"
MAX_TWEETS = 20

def generate_rss():
    fg = FeedGenerator()
    fg.title(f'Tweets by @{TWITTER_USERNAME}')
    fg.link(href=f'https://twitter.com/{TWITTER_USERNAME}', rel='alternate')
    fg.description(f'Latest tweets from Twitter user @{TWITTER_USERNAME}')
    fg.language('en')

    for i, tweet in enumerate(sntwitter.TwitterUserScraper(TWITTER_USERNAME).get_items()):
        if i >= MAX_TWEETS:
            break
        fe = fg.add_entry()
        fe.id(tweet.url)
        fe.title(tweet.content[:50] + ('...' if len(tweet.content) > 50 else ''))
        fe.link(href=tweet.url)
        fe.pubDate(tweet.date)
        fe.description(tweet.content)

    return fg.rss_str(pretty=True)

@app.route('/')
def rss_feed():
    rss = generate_rss()
    return Response(rss, mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run()