#!/usr/bin/env python3
"""Tweetpix, one day it will be a tweetbot for pixellize :)
"""
import json
import tweepy

from io import BytesIO
import click
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
FLICKR_PHOTOPAGE_URL = "www.flickr.com/photos/{owner}/{id}"


def generate_urls_for(topic):
    """Takes a "topic" string and returns a tuple containing two urls.
    They are respectively the photo url and photo page url of a random picture. 
    The picture is chosen among the result of searching "topic" in flickr with
    a suitable constraint on the licenses.
    """
    search_url = FLICKR_SEARCH_URL.format(FLICKR_API_KEY, topic)
    raw_data = get(search_url)
    decoded_data = str(raw_data.content, encoding="utf-8", errors="ignore")
    json_data = json.loads(decoded_data)
    rpic = choice(json_data['photos']['photo'])

    return FLICKR_PHOTO_URL.format(**rpic), FLICKR_PHOTOPAGE_URL.format(**rpic)


def get_image_from(photo_url):
    """Thakes a photo url and returns it as a PIL.Image
    """
    image_data = get("https://" + photo_url).content
    stream = BytesIO(image_data)
    image = Image.open(stream).convert("RGB")

    return image

#TODO
def get_random_parameters():
    """
    Generate random parameters for the pixellize function.
    """
    pass


def prepare_image(image):
    """Pixellise and suitably convert a PIL.Image, then returns it.
    """
    # pixellize(image, max_pixels=72, rescale=4.0, ncols=20, minv=14, maxv=181, gamma=1.51)
    pixellated = pixellize(image).convert("RGB")

    return pixellated


def publish_image(image_file, status_message):
    """Takes a PIL.Image and a status_message and publishes it on your
    twitter account. The parameters are stateful and taken from the keys.py file
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_with_media(image_file, status=status_message)

# TODO: decide if add an optional message
@click.command()
@click.argument("search_string", nargs=1)
def tweetpix(search_string="panorama"):
    """Takes a search string to use on flickr, 
    grabs a random picture from the search results, 
    pixellizes the picture,
    finally publishes it on twitter.
    """
    photo_url, page_url = generate_urls_for(search_string)
    flickr_image = get_image_from(photo_url)
    pixellatedimage = prepare_image(flickr_image)

    uniform_size = scaled_size(1200 / max(flickr_image.size),
                               flickr_image.size)
    print(uniform_size)
    photo_file = photo_url.replace("/", ".").replace(".jpg", ".png")
    pixellatedimage.resize(uniform_size).save(photo_file)

    message = "#pixellized version of {}. Search '{}', baseline 72px, long side 1200px".format(
        page_url, search_string)

    print(message)
    publish_image(photo_file, message)


if __name__ == "__main__":
    tweetpix()
