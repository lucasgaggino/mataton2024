from dotenv import load_dotenv
import os
import tweepy


KEY_PATH = "./keys.env"
load_dotenv(dotenv_path=KEY_PATH)
consumer_key = os.environ.get("TWITTER_API_KEY")
consumer_secret = os.environ.get("TWITTER_API_SECRET_KEY")


access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

print(access_token)
client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret,bearer_token=bearer_token
)


response = client.search_all_tweets(query="python", max_results=10)
print(f"https://twitter.com/user/status/{response.data['id']}")