from simulation import simulate
from DataAnalysis import DataAnalysis as DA
from datetime import datetime as dt
from DatabaseAPI.PolygonDB import PolygonDB as pDB
from Algorithms.moving_avgs1 import init, strat

import HelperFunctions as HF
import random
dA = DA()


def moving_avgs1(start, end, sym):
	timestep = '1m'
	cash = 10
	con = simulate(init, strat, start, end, timestep, cash, positions = {}, market = 'NYSE', symbol = sym, verbose = False)
	return con.total_asset_value() - cash

def snapshot():
	resp = pDB().snapshot()
	targets = []
	for info in resp:
		name = info['ticker']
		price = info['lastTrade']['p']
		if price > .5 and price < 3:
			targets.append(name)
	return targets


def Test_Daily_Strategy(tickers, start, end, strat):
	'''
	Given strategies that run during the day and sell remaining positions at the end,
	test the strategy for each day between two dates for a given set of tickers
	returns dictionary mapping tickers to list of contexts.
	''' 
	from datetime import timedelta
	d = HF.get_weekdays(start, end)
	profits = {}
	for ticker in tickers:
		profits[ticker] = 0
	for ticker in tickers:
		profit = 0
		for weekday in d:
			try:
				val = strat(weekday, weekday + timedelta(1), ticker)
			except:
				print("Issue on day {}".format(weekday))
				val = 0
			profit += val 
		print('Profit for {}:'.format(ticker), profit)
		profits[ticker] += profit
	return profits


		

if __name__ == "__main__":
	
	p = Test_Daily_Strategy(['OCN', 'TOPS', 'EXK'], dt(2020,3,3), dt(2020,5,8), moving_avgs1)





