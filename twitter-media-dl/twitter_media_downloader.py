import tweepy
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

def authenticate_twitter_app():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def download_media(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")

def get_media_urls(api, tweet_url):
    tweet_id = tweet_url.split('/')[-1]
    tweet = api.get_status(tweet_id, tweet_mode='extended')
    media_urls = []
    if 'media' in tweet.entities:
        for media in tweet.entities['media']:
            media_urls.append(media['media_url'])
    return media_urls

def main():
    api = authenticate_twitter_app()
    tweet_url = input("Enter the tweet URL: ")
    media_urls = get_media_urls(api, tweet_url)
    if not media_urls:
        print("No media found in the tweet.")
        return
    for i, media_url in enumerate(media_urls):
        filename = f"media_{i}.jpg"
        download_media(media_url, filename)

if __name__ == "__main__":
    main()