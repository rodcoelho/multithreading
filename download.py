#!usr/bin/env python3

import os, requests, json, logging

from pathlib import Path

from imgurpython import ImgurClient

logger = logging.getLogger(__name__)

url = 'https://api.imgur.com/3/gallery/'
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
client_id = open(os.path.join(__location__, 'client_id.txt')).read()
client_secret = open(os.path.join(__location__, 'client_secret.txt')).read()
client = ImgurClient(client_id, client_secret)


def get_links():
    items = client.gallery(section='top', sort='time', page=3, window='week', show_viral=False)
    return [[x.title, x.link] for x in items]


def download_link(directory,link):
    logger.info('Downloading')


def setup_download_dir():
    pass

