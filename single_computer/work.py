#!/usr/bin/env python3

import os, requests, json, logging
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_download_dir():
    # create a log destination directory if it doesn’t already exist
    download_dir = Path('log')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir

