from MagicDB import MagicDB
from DatabaseAPI.IexDB import IexDB as iDB
from DatabaseAPI.PolygonDB import PolygonDB as pDB
from DataAnalysis import DataAnalysis as DA
from datetime import datetime as dt
import pytz

def init(context, end_date, symbol):
	'''
	Stores initial values for each relevant variable
	'''
	mDB = MagicDB('1d', context.time, end_date, pDB())
	context.database = mDB
	first_20 = []
	for i in range(20):
		
		price = context.advance_to_valid_price(symbol)
		first_20.append(price)
	context.variables["Last20"] = first_20
	context.variables["20MA"] = sum(first_20)/20
	context.variables[symbol] = price
	context.positions[symbol] = 0
	context.buys[symbol] = []
	context.sells[symbol] = []
	context.graphs = [(symbol, "20MA")]


def strat(context, symbol):
	price = context.database.get_value(symbol, context.time, "Open")
	if type(price) != str:

		
		OldMA20 = context.variables["20MA"]

		context.variables["Last20"] = context.variables["Last20"][1:] + [price]
		context.variables["20MA"] = sum(context.variables["Last20"])/20
		context.variables[symbol] = price

		Last20 = context.variables["Last20"]
		MA20 = context.variables["20MA"]
		
		if Last20[-2] < OldMA20 and price > MA20 and context.cash - price > 0:
			context.buy_position(symbol, 1)
		elif Last20[-2] > OldMA20 and price < MA20 and context.positions[symbol] > 0:
			context.sell_position(symbol,1)

		
		