#!/usr/bin/env python3

import logging
from time import time

from work import setup_download_dir, aggregate_files_to_do_work_on, edb_work

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)


def main():
    ts = time()

    # prep directory to store output
    download_dir = setup_download_dir()

    # get list of work to do
    files = aggregate_files_to_do_work_on()

    # iterate over list
    # ACTUAL WORK
    for file in files:
        edb_work(file)

    # prints time it took to do work
    print("Took {}s".format(time()-ts))


if __name__ == '__main__':
    print("Testing Single Threading")
    main()
