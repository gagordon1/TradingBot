from Simulators.CryptoSim import context
from MagicDB import MagicDB
from DatabaseAPI.BinanceDB import BinanceDB as bDB
from DataAnalysis import DataAnalysis as DA
from datetime import datetime as dt
import HelperFunctions as HF

def init(context, end_date, C1, C2):
	'''
	Stores initial values for each relevant variable
	'''
	symbol = C1 + C2
	context.database = MagicDB(context.timestep, context.time, end_date, bDB())
	first_50 = []
	timestep = HF.get_timestep_as_timedelta('1m')
	for i in range(50):
		price = context.get_historical_open_rate(symbol, context.time)
		context.step(timestep)
		first_50.append(price)

	first_20 = first_50[30:]
	context.buys[symbol] = []
	context.sells[symbol] = []
	context.variables[symbol + ' 20'] = first_20
	context.variables[symbol + ' 50'] = first_50
	context.variables[symbol + ' MA1'] = sum(first_20)/20
	context.variables[symbol + ' MA2'] = sum(first_50)/50
	context.variables[symbol] = price
	context.graphs = [(symbol, symbol + ' MA1', symbol + ' MA2')]


def strat(context, C1, C2):
	symbol = C1 + C2
	price = context.database.get_value(symbol, context.time, "Open")
	if type(price) != str:
		first_20 = context.variables[symbol + ' 20']
		first_50 = context.variables[symbol + ' 50']
		MA1 = context.variables[symbol + ' MA1']
		MA2 = context.variables[symbol + ' MA2']
		C1amount = context.positions[C1]
		C2amount = context.positions[C2]
		

		if MA2 > MA1*1.002 and C2amount - .001 >0:
			# BUY
			context.buy(C1, C2, .001)

		elif MA1 > MA2*1.002 and C1amount - .001/price >0:
			#SELL
			context.sell(C1, C2, .001/price)

		first_20 = first_20[1:] + [price]
		first_50 = first_50[1:] + [price]
		context.variables[symbol + ' MA1'] = sum(first_20)/20
		context.variables[symbol + ' MA2'] = sum(first_50)/50
		context.variables[symbol + ' 20'] = first_20
		context.variables[symbol + ' 50'] = first_50
		context.variables[symbol] = price