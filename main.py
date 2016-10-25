import sys
import requests
from html.parser import HTMLParser


class FinvizKeyStatsParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.datamap = {}
        self.last_indicator = None
        self.indicators = ['P/E', 'EPS (ttm)', 'Insider Own', 'Shs Outstand',
                           'Perf Week', 'Market Cap', 'Forward P/E', 'EPS next Y', 'Insider Trans',
                           'Shs Float', 'Perf Month', 'Income', 'PEG', 'EPS next Q', 'Inst Own',
                           'Short Float', 'Perf Quarter', 'Sales', 'P/S', 'EPS this Y', 'Inst Trans',
                           'Short Ratio', 'Perf Half Y', 'Book/sh', 'P/B', 'EPS next Y', 'ROA', 'Target Price',
                           'Perf Year', 'Cash/sh', 'P/C', 'EPS next 5Y', 'ROE', '52W Range', 'Perf YTD', 'Dividend',
                           'P/FCF', 'EPS past 5Y', 'ROI', '52W High', 'Beta', 'Dividend', 'Quick Ratio', 'Sales past 5Y',
                           'Gross Margin', '52W Low', 'ATR', 'Employees', 'Current Ratio', 'Sales Q/Q', 'Oper. Margin',
                           'RSI (14)', 'Volatility', 'Optionable', 'Debt/Eq', 'EPS Q/Q', 'Profit Margin', 'Rel Volume',
                           'Prev Close', 'Shortable', 'LT Debt/Eq', 'Earnings', 'Payout', 'Avg Volume', 'Price',
                           'Recom', 'SMA20', 'SMA50', 'SMA200', 'Volume', 'Change']

    def handle_data(self, data):
        if data in self.indicators:
            self.last_indicator = data
            # We just set title of indicator, so value will be in next data
            # point. So we need to return after we set last_indicator
            return

        if self.last_indicator is not None:
            self.datamap[self.last_indicator] = data
            # After save of corresponding data point set last indicator
            # to None.
            self.last_indicator = None


class FinvizCompanyInfoParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.datamap = {}
        self.datalist = []
        self.fields = ['Ticker', 'Exchange',
                       'Name', 'Sector', 'Industry', 'Country']

    def handle_endtag(self, tag):
        if str(tag) == 'html':
            data = self.extract_data()
            for key, field in enumerate(self.fields):
                self.datamap[field] = data[key]

    def extract_data(self):
        data = []
        settings = False
        financial_highlights = False
        for row in self.datalist:
            row = row.strip()
            if row == 'Settings':
                settings = True
                continue
            if row == 'financial highlights':
                financial_highlights = True
            if settings == False:
                continue
            if financial_highlights == True:
                break
            data.append(row)
        return data

    def handle_data(self, data):
        data = data.strip()
        if len(data) != 0 and data != '|':
            self.datalist.append(data)


class MyHTMLParser(HTMLParser):

    def __init__(self, file):
        super().__init__()
        self.datalist = []
        self.fname = file

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if str(tag) == 'html':
            with open(self.fname, 'wb') as db:
                for row in self.extract_data():
                    if len(row) != 0:
                        db.write(row.encode('utf-8'))

    def extract_data(self):
        data = []
        settings = False
        financial_highlights = False
        for row in self.datalist:
            row = row.strip()
            if row == 'Settings':
                settings = True
                continue
            if row == 'financial highlights':
                financial_highlights = True
            if settings == False:
                continue
            if financial_highlights == True:
                break
            data.append(row + '\n')
        return data

    def handle_data(self, data):
        data = data.strip()
        if len(data) != 0 and data != '|':
            self.datalist.append(data + '\n')


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


def parse_file(fname):
    parser = FinvizCompanyInfoParser()
    with open(fname) as f:
        strdata = f.read()
        parser.feed(strdata)
    return parser


if __name__ == '__main__':
    symbol = input('Enter symbol of the stock: ')
    symbol = symbol.upper()
    if len(symbol) == 0:
        print('No symbol was provided.')

    print('Getting data for {0}'.format(symbol))

    parser = parse_file('aapl.txt')
    print(parser.datamap)
