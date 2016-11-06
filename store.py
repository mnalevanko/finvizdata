from datetime import datetime
from datetime import timedelta

from db import db


class FinvizStore(object):

    def __init__(self):
        self.stocks = db["stocks"]
        self.keystats = db["keystats"]

    def find(self, symbol):
        # Refresh data when last update is older more 1 day.
        gt_date = datetime.utcnow() - timedelta(days=1)
        # Query
        q_recent_record = {
            "symbol": symbol,
            "update_date": {"$gt": gt_date}
        }
        res = self.stocks.find(q_recent_record)
        return res

    def create_stock(self, stock):
        try:
            res = self.stocks.insert_one(stock)
            stock["_id"] = str(res.inserted_id)
            return stock
        except Exception as e:
            print(e)

    def create_keystats(self, stats, symbol):
        try:
            stats["symbol"] = symbol.upper()
            stats["create_date"] = datetime.utcnow()
            stats["update_date"] = datetime.utcnow()
            res = self.keystats.insert_one(stats)
        except Exception as e:
            print(e)
