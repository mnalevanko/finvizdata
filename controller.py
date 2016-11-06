import requests
from datetime import datetime
from datetime import timedelta

from parsers import FinvizCompanyInfoParser
from parsers import FinvizKeyStatsParser
from store import FinvizStore


def get_page(symbol):
    """
    Download page from finviz.com with symbol provided.
    """
    try:
        formated_symbol = str(symbol).upper()
    except:
        return ValueError('Bad symbol was provided.')
    url = 'http://finviz.com/quote.ashx?t={0}'.format(formated_symbol)
    res = requests.get(url)
    if res.status_code == 200:
        return res.text


def parse_info(page):
    info = FinvizCompanyInfoParser()
    info.feed(page)
    return info.datamap


def parse_keystats(page):
    stats = FinvizKeyStatsParser()
    stats.feed(page)
    return stats.datamap


class KeyStatsController(object):

    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.store = FinvizStore()

    def update(self):
        # Result
        result = self.store.find(self.symbol)
        if result.count() == 0:
            print('Cannot find statistics.')
            result = self.download_new_data()
            return result
        else:
            return list(result)[:1]

    def download_new_data(self):
        page = get_page(self.symbol)
        keystats = parse_keystats(page)
        print(keystats)
        result = self.store.create_keystats(keystats, self.symbol)
        return result
