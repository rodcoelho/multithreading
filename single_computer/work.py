#!/usr/bin/env python3

import os, requests, json, logging
from pathlib import Path
import pandas as pd

from edb import update_cash_buy, update_shares_buy

logger = logging.getLogger(__name__)


def setup_download_dir():
    # create a log destination directory if it doesn’t already exist
    download_dir = Path('files')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir


def aggregate_files_to_do_work_on():
    files = os.listdir("files")
    return files

def edb_work(file):
    file = 'files/' + file
    strats = {'5.10': [0, 5, 10], '5.20': [0, 5, 20], '5.30': [0, 5, 30],
              '10.20': [0, 10, 20], '10.30': [0, 10, 30], '10.40': [0, 10, 40],
              '15.20': [0, 15, 20], '15.30': [0, 15, 30], '15.45': [0, 15, 45]}
    for key, value in strats.items():
        portfolio = {'cash': 1000000.0,
                     'wilshire': {'shares': 0, 'VWAP': 0.0}}
        # ex: file = 'files/WILL5000INDFC.csv'  # File Location
        data = pd.read_csv(file, names=['date', 'price'])  # Create DataFrame
        data = data[data.price > '0.20']  # Get rid of rows with prices == 0 (holidays)
        data['MA-A'] = data['price'].rolling(value[1]).mean()  # MA1
        data['MA-B'] = data['price'].rolling(value[2]).mean()  # MA2
        data['ratio'] = data['MA-A'] / data['MA-B']  # MA1 / MA2 Ratio
        data = data.dropna()  # Drop Non-Real Numbers
        num_of_rows = (data.shape)[0]  # Number of rows (to iterate over later)
        dbuy = data[data.ratio > 1.01]  # if ratio > 1, it's a buy signal
        dsell = data[data.ratio < 0.99]  # if ratio < 1, it's a sell signal

        last_transaction = 'SELL'  # keeps track of last transaction
        for i, (index, row) in enumerate(data.iterrows()):
            # BUY signal
            if row['ratio'] > 1.01 and last_transaction == 'SELL':
                # subtract cash and get quantity to buy
                quantity = float(update_cash_buy(portfolio, row['price']))
                # update portfolio - add quantity and get new VWAP in portfolio
                update_shares_buy(portfolio, float(row['price']), quantity)
                last_transaction = 'BUY'

            # SELL signal
            elif row['ratio'] < .999 and last_transaction == 'BUY':
                # get rid of half of shares
                share_quantity_to_sell = portfolio['wilshire']['shares'] // 2
                portfolio['wilshire']['shares'] = share_quantity_to_sell
                # add cash
                current_cash = float(portfolio['cash'])
                new_income = share_quantity_to_sell * float(row['price'])
                current_cash += float(new_income)
                portfolio['cash'] = float(current_cash)
                last_transaction = 'SELL'

            # if last item in dataframe, sell everything to see returns
            elif i == len(data) - 1:
                share_quantity_to_sell = portfolio['wilshire']['shares']
                current_cash = float(portfolio['cash'])
                new_income = share_quantity_to_sell * float(row['price'])
                current_cash += new_income
                portfolio['cash'] = float(current_cash)
                portfolio['wilshire']['shares'] = 0
                strats[key][0] = (portfolio['cash'] - 1000000.0) / 1000000.0
    strategy_returns_sort = []
    result = {}
    for keys, values in strats.items():
        result[keys] = values[0]*100
    return result
