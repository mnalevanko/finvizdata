import sys
import requests
from html.parser import HTMLParser
from pprint import PrettyPrinter

from finviz.parsers import FinvizCompanyInfoParser
from finviz.parsers import FinvizKeyStatsParser

pp = PrettyPrinter(indent=4)


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


if __name__ == '__main__':
    symbol = input('Enter symbol of the stock: ')
    symbol = symbol.upper()
    if len(symbol) == 0:
        print('No symbol was provided.')

    print('Getting data for {0}'.format(symbol))
    page = get_page(symbol)
    data = {}
    data['info'] = parse_info(page)
    data['key_stats'] = parse_keystats(page)
    pp.pprint(data)
