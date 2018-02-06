#!/usr/bin/env python3

import logging, os
from time import time
from download import download_link, get_links, setup_download_dir
from functools import partial
from multiprocessing.pool import Pool

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

def main():
    ts = time()

    # set up directory if DNE
    download_dir = setup_download_dir()

    # get links for images
    links = [l for l in get_links() if l.endswith('.jpg')]
    download = partial(download_link, download_dir)

    # will spawn 8 new processes(pools)
    with Pool(8) as p:
        # download the images in parallel
        p.map(download, links)

    print('Took {}s'.format(time() - ts))


if __name__ == '__main__':
    print("Testing Multi Processing")
    main()

