import datetime
import pyEX as p
from django.utils import timezone
from .models import *
import os
import json
import time


KEY = 'pk_41f8cdb569f042dbaac272ca63ec855e'
C = p.Client(api_token=KEY, version="stable")


def get_symbols():
    cur_path = os.path.dirname(__file__)
    with open(cur_path+"/assets/symbols.JSON", 'r') as infile:
        data = json.load(infile)
    return data


def get_company(symbol):
    symbol = str(symbol).strip().lower()
    data = C.company(symbol)
    data['logo'] = C.logo(symbol)
    return data
# get_company("aapl")


def stats(symbol):
    data = C.chart(symbol, timeframe="1y")
    chart = [{
        'date': obj['date'],
        'close': obj['close']
    } for obj in data if obj['close']]
    last = datetime.datetime.now().strftime("%b %-d %Y, %-I:%M %p")
    latestPrice = chart[-1]['close']

    return {'chart': chart, 'lastUpdated': last, 'lastPrice': latestPrice}


def getDays(start):
    end = timezone.now()
    delta = end - start
    days = []
    for i in range(delta.days + 1):
        days.append((start + datetime.timedelta(days=i)).strftime("%b %-d"))
    return days


def quote(stockNames):
    seen = {}
    aggr = 0
    for name in stockNames:
        if name in seen:
            aggr += seen[name]
        else:
            price = C.quote(name)['latestPrice']
            seen[name] = price
            aggr += price
    return aggr


def getBalance(username):
    user = User.objects.get(username=username)
    stocks = user.serialize()['stocks']
    stock_names = [stock['symbol'] for stock in stocks]

    balance = quote(stock_names) + user.current_balance
    return balance
