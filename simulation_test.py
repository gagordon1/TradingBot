import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from GuapBot.DataAnalysis import DataAnalysis as DA
from GuapBot.DatabaseAPI.PolygonDB import PolygonDB as pDB
import GuapBot.HelperFunctions as HF
from GuapBot.Simulators.CryptoSim import simulate
from matplotlib import style, pyplot as plt
from datetime import timedelta, datetime as dt
import numpy as np
import json
import random
import torch
import time
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
	from Algorithms.CryptoMovAvgs1 import init, strat
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


def Test_NN_Strategy(start, end):
	'''
	Samples the NN strategy over some random dates
	'''
	# from GuapBot.Algorithms.NN1 import init, strat
	# from GuapBot.Algorithms.SigmoidPicker1 import init, strat
	# from GuapBot.Algorithms.BuyNHold import init,strat
	from GuapBot.Algorithms.NN2 import init, strat
	with open("JSON_Data/HighVolumeMarkets.json", "r") as file:
		coins = json.load(file)
	time_step = '1m'
	initialize = init
	strategy = strat
	C2 = "BTC"
	values = []
	s = time.time()
	for i in range(100):
		C1 = random.choice(coins)
		start_date = HF.random_date(start, end)
		end_date = start_date + timedelta(1)
		positions = {'BTC': .05, C1: 0}
		print("Market: {}{} Date: {}".format(C1,C2,start_date))
		try:
			con = simulate(initialize, strategy, start_date, end_date,
				time_step, positions, C1, "BTC", verbose = False)
			print(con)
			value = con.get_BTC_value()
			values.append(value)
		except:
			print("DATA ISSUE")
		print('---'*20)

	e = time.time()

	avg_value = (sum(values)/100)/.05
	print("AVG PERCENT RETURN: {}%".format((avg_value - 1)*100))
	print("TIME FOR TEST: {}".format(e-s))
	# dA.plot_sim_graph_data(con.graph_data, buys = con.buys, sells = con.sells)
	v = np.array(values)
	v = (v/.05 - 1)*100
	style.use("seaborn")
	plt.title("Percent Returns Over 100 Trials")
	plt.hist(v, bins = 15)
	plt.show()

def NN_Strategy(start, end, C1):
	# from Algorithms.NN1 import init, strat
	# from Algorithms.SigmoidPicker1 import init,strat
	# from Algorithms.BuyNHold import init, strat
	from Algorithms.NN2 import init, strat
	time_step = '1m'
	initialize = init
	strategy = strat
	positions = {'BTC': .05, C1: 0}
	con = simulate(initialize, strategy, start, end, time_step, positions, C1, "BTC", verbose = False)
	print(con)
	print("Buys:", len(con.buys["{}BTC".format(C1)]))
	print("Sells:", len(con.sells["{}BTC".format(C1)]))
	dA.plot_sim_graph_data(con.graph_data, buys = con.buys, sells = con.sells)

def mean_reverse(start,end,sym):
	from Algorithms.reversionstrat1 import init, strat
	from Simulators.StockSim import context, simulate
	timestep = '1d'
	cash = 1000
	con = simulate(init, strat, start, end, timestep, cash, symbol = sym, verbose = True)
	return con

if __name__ == "__main__":
	start = dt(2016, 3, 4)
	end = dt(2020, 7,2)
	sym = "UAL"
	con = moving_avgs1(start, end, sym)
	print(con)
	dA.plot_sim_graph_data(con.graph_data, buys = con.buys, sells = con.sells)
