import json
import tweepy

from io import BytesIO
from keys import keys
from PIL import Image
from pixellize import pixellize, scaled_size
from random import choice, randint
from requests import get


CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

FLICKR_API_KEY = keys['flickr_key']
# https://www.flickr.com/services/api/flickr.photos.search.html
FLICKR_SEARCH_URL = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={}&text={}&license=1%2C2%2C9%2C10&sort=interestingness-desc&media=photos&format=json&nojsoncallback=1"
# https://www.flickr.com/services/api/misc.urls.html
FLICKR_PHOTO_URL = "farm{farm}.staticflickr.com/{server}/{id}_{secret}_b.jpg"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def generate_url_for(topic):
    search_url = FLICKR_SEARCH_URL.format(FLICKR_API_KEY, topic)
    raw_data = get(search_url)
    decoded_data = str(raw_data.content, encoding="utf-8", errors="ignore")
    json_data = json.loads(decoded_data)
    rpic = choice(json_data['photos']['photo'])

    return FLICKR_PHOTO_URL.format(**rpic)


def get_random_image_from(photo_url):

    image_data = get("https://" + photo_url).content
    stream = BytesIO(image_data)
    image = Image.open(stream).convert("RGB")

    return image


def get_random_parameters():
    randint(1, 2)
    pass


def prepare_image(image):
    uniform_size = scaled_size(1600 / max(image.size), image.size)
    pixellated = pixellize(image.resize(uniform_size)).convert("RGB")

    return pixellated


def publish_image(image):
    pass


if __name__=="__main__":
    photo_url = generate_url_for("panorama")
    image = get_random_image_from(photo_url)
    pixellatedimage = prepare_image(image)

    pixellatedimage.save(photo_url.replace("/", "."))
