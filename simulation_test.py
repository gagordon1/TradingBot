from DataAnalysis import DataAnalysis as DA
from datetime import datetime as dt
from DatabaseAPI.PolygonDB import PolygonDB as pDB
import HelperFunctions as HF
import random
dA = DA()


def moving_avgs1(start, end, sym):
	from Algorithms.moving_avgs1 import init, strat
	from Simulators.StockSim import context, simulate
	timestep = '1m'
	cash = 10
	con = simulate(init, strat, start, end, timestep, cash, symbol = sym, verbose = False)
	return con

def snapshot():
	resp = pDB().snapshot()
	targets = []
	for info in resp:
		name = info['ticker']
		price = info['lastTrade']['p']
		if price > .5 and price < 3:
			targets.append(name)
	return targets

def BTC_moving_avgs(start, end, C1, C2):
	from Algorithms.CryptoMovAvgs1 import init, strat
	from Simulators.CryptoSim import simulate
	timestep = '1m'
	positions = {'BTC': .01, C1 : 0}
	con = simulate(init, strat, start, end, timestep, positions, C1, C2, verbose = False)
	return con

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

	con = BTC_moving_avgs(dt(2020, 5, 1), dt(2020, 5,3), 'XMR', 'BTC')
	print(con)
	dA.plot_sim_graph_data(con.graph_data, buys = con.buys, sells = con.sells)



