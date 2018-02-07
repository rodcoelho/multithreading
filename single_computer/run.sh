#!/usr/bin/env bash

rm log/results.txt

python3 single_thread.py


#python3 multi_threading.py
#
## not very efficient
python3 multi_processing.py

