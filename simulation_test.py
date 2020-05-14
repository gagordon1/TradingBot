import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from DataAnalysis import DataAnalysis as DA
from datetime import timedelta, datetime as dt
from DatabaseAPI.PolygonDB import PolygonDB as pDB
import HelperFunctions as HF
from Algorithms.CryptoMovAvgs1 import init, strat
from Simulators.CryptoSim import simulate
import json
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

def BTC_moving_avgs(start, end, C1):
	
	timestep = '1m'
	positions = {'BTC': .01, C1 : 0}
	con = simulate(init, strat, start, end, timestep, positions, C1, 'BTC', verbose = False)
	
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


		
def AVG_PROFIT(strategy):
	
	
	import time
	with open("JSON_Data/HighVolumeMarkets.json", "r") as file:
		HighVol = json.load(file)
	i=0
	total_profit = 0
	while i < 20:
		start = HF.random_date(dt(2020, 3, 3), dt(2020, 5,12))
		end = start +timedelta(1)
		j=0
		while j < 4:
			tstart = time.time()
			C1 = random.choice(HighVol)
			print('---'*10)
			print('simulating {}/BTC from {} to {}'.format(C1, start, end))
			con = strategy(start, end, C1)
			print(con)
			profit = con.get_BTC_value() - .01
			print('Profit:', profit)
			total_profit += profit
			tend = time.time()
			print('time for simulation: {} seconds'.format(tend-tstart))
			j+=1
		i+=1
	print('Average Profit:', total_profit/80)
if __name__ == "__main__":
	
	AVG_PROFIT(BTC_moving_avgs)
	start = HF.random_date(dt(2020, 3, 3), dt(2020, 5,12))
	end = start +timedelta(1)
	with open("JSON_Data/HighVolumeMarkets.json", "r") as file:
		HighVol = json.load(file)
	C1 = random.choice(HighVol)
	C1 = 'BCH'
	con = BTC_moving_avgs(start,end,C1)	
	print(con)
	# dA.plot_sim_graph_data(con.graph_data, buys = con.buys, sells = con.sells)


	# start = HF.random_date(dt(2020, 3, 4), dt(2020, 5,12))
	# end = start +timedelta(1)
	# C1 = 'OCN'
	# con = moving_avgs1(dt(2020, 5, 11),dt(2020, 5, 12),C1)	
	# print(con)
	# dA.plot_sim_graph_data(con.graph_data, buys = con.buys, sells = con.sells)
