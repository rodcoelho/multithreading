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
    return [x.link for x in items]


def download_link(directory,link):
    logger.info('Downloading {}'.format(link))
    download_path = directory / os.path.basename(link)
    with requests.get(link) as image, download_path.open('wb') as f:
        f.write(image.readall())


def setup_download_dir():
    # create a download destination directory if it doesn’t already exist
    download_dir = Path('images')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir



