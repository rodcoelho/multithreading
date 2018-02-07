#!/usr/bin/env python3

from queue import Queue
from threading import Thread
import logging
from time import time
from work import setup_download_dir, aggregate_files_to_do_work_on, edb_work

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # get work from queue and expand the tuple
            file = self.queue.get()
            edb_work(file)
            self.queue.task_done()


def main():
    ts = time()

    # prep directory to store output
    download_dir = setup_download_dir()

    # get links for work
    files = aggregate_files_to_do_work_on()

    # Create a queue to communicate with the worker threads
    queue = Queue()

    # Create 8 worker threads
    for x in range(8):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()

    # Put the tasks into the queue as a tuple
    for file in files:
        logger.info('Queueing {}'.format(file))
        queue.put(file)

    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()

    print('Took {}'.format(time() - ts))


if __name__ == '__main__':
    print("Testing Multi Threading")
    main()
