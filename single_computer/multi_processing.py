#!/usr/bin/env python3

import logging, os
from time import time
from work import setup_download_dir, aggregate_files_to_do_work_on, edb_work
from functools import partial
from multiprocessing.pool import Pool

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

d = {}


def main():
    ts = time()

    # set up directory if DNE
    download_dir = setup_download_dir()

    # get links for work
    files = aggregate_files_to_do_work_on()

    # work prep
    work = partial(edb_work)                # download = partial(download_link, download_dir)

    # work - will spawn 4 new processes(pools)
    with Pool(4) as p:                      # with Pool(8) as p:
        # do work in parallel               # download the images in parallel
        p.map(work, files)                  # p.map(download, links)

    print('Took {}s'.format(time() - ts))


if __name__ == '__main__':
    print("Testing Multi Processing")
    main()

