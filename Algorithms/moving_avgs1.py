from Simulators.StockSim import context
from MagicDB import MagicDB
from DatabaseAPI.IexDB import IexDB as iDB
from DatabaseAPI.PolygonDB import PolygonDB as pDB
from DataAnalysis import DataAnalysis as DA
from datetime import datetime as dt

def init(context, end_date, symbol):
	'''
	Stores initial values for each relevant variable
	'''
	mDB = MagicDB(context.timestep, context.time, end_date, pDB())
	context.database = mDB
	first_50 = []
	for i in range(50):
		price = context.advance_to_valid_price(symbol)
		first_50.append(price)

	first_20 = first_50[30:]
	context.buys[symbol] = []
	context.sells[symbol] = []
	context.variables[symbol + ' 20'] = first_20
	context.variables[symbol + ' 50'] = first_50
	context.variables[symbol + ' MA1'] = sum(first_20)/20
	context.variables[symbol + ' MA2'] = sum(first_50)/50
	context.variables[symbol] = price
	context.positions[symbol] = 0
	context.graphs = [(symbol, symbol + ' MA1', symbol + ' MA2')]


def strat(context, symbol):
	price = context.database.get_value(symbol, context.time, "Open")
	if type(price) != str:
		first_20 = context.variables[symbol + ' 20']
		first_50 = context.variables[symbol + ' 50']
		MA1 = context.variables[symbol + ' MA1']
		MA2 = context.variables[symbol + ' MA2']

		if MA2 > MA1*1.001 and context.cash > price:
			context.buy_position(symbol, 1)

		elif MA1 > MA2*1.001 and context.positions[symbol] > 0:
			context.sell_position(symbol,1)

		first_20 = first_20[1:] + [price]
		first_50 = first_50[1:] + [price]
		context.variables[symbol + ' MA1'] = sum(first_20)/20
		context.variables[symbol + ' MA2'] = sum(first_50)/50
		context.variables[symbol + ' 20'] = first_20
		context.variables[symbol + ' 50'] = first_50
		context.variables[symbol] = price

