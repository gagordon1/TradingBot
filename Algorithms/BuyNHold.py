from GuapBot.Simulators.CryptoSim import context
from GuapBot.MagicDB import MagicDB
from GuapBot.DatabaseAPI.BinanceDB import BinanceDB as bDB
from datetime import datetime as dt
import GuapBot.HelperFunctions as HF

def init(context, end_date, C1, C2):
	'''
	Stores initial values for each relevant variable
	'''
	symbol = C1 + C2
	context.database = MagicDB(context.timestep, context.time, end_date, bDB())
	context.graphs = [(symbol,)]
	price = context.get_historical_open_rate(symbol, context.time)
	context.buys[symbol] = []
	context.sells[symbol] = []
	context.buy(C1,C2, context.positions[C2])
	context.variables[symbol] = price
	


def strat(context, C1, C2):
	symbol = C1+C2
	context.variables[symbol] = context.get_historical_open_rate(symbol, context.time)

	