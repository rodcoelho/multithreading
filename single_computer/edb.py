#!/usr/bin/env python3

import math

def update_cash_buy(portfolio,price):                                   # Employing a "Buy Logic" strategy
    cash_to_spend = portfolio['cash']/2.0                               # where each buy signal
    portfolio['cash'] = cash_to_spend                                   # we will spend 50% of our total cash holdings
    quantity_shares_to_buy = math.floor(cash_to_spend/float(price))
    return float(quantity_shares_to_buy)

def update_shares_buy(portfolio, price, quantity):                      # Here we take the VWAP to know the
    price_VWAP = float(portfolio['wilshire']['VWAP'])                   # average price we paid per share
    if price_VWAP == 0.0:
        portfolio['wilshire']['VWAP'] = float(price)
        portfolio['wilshire']['shares'] = quantity
    else:
        quantity_VWAP = float(portfolio['wilshire']['shares'])
        new_VWAPtop = (float(price) * float(quantity)) + (float(price_VWAP) * float(quantity_VWAP))
        newVWAPbottom = (float(quantity_VWAP) + float(quantity))
        portfolio['wilshire']['VWAP'] = float(new_VWAPtop) / float(newVWAPbottom)
        portfolio['wilshire']['shares'] = newVWAPbottom