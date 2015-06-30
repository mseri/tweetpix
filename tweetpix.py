import tweepy
from requests import get
from json import json
from pixellize import pixellize
from random import choice, randint
from keys import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']
FLICKR_API_KEY = keys['flickr_key']

FLICKR_SEARCH_URL = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={}&text={}&license=1%2C2%2C9%2C10&sort=interestingness-desc&media=photos&format=json&nojsoncallback=1"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def get_random_image_with(topic):
    search_url = FLICKR_SEARCH_URL.format(FLICKR_API_KEY, topic)
    raw_data = get(search_url)
    decoded_data = str(raw_data.content, encoding="utf-8", errors="ignore")
    json_data = json.loads(decoded_data)
    random_picture = choice(json_data['photos']['photo'])
    
    pass

def get_random_parameters():
    randint()
    pass

def prepare_image(image):
    pixellize(image)
    pass

def publish_image(image):
    image
    keys
    pass

if __name__=="__main__":
    pass