from GuapBot.Algorithms.NeuralNets.Nets import load_NN
from GuapBot.Simulators.CryptoSim import context
from GuapBot.MagicDB import MagicDB
from GuapBot.DatabaseAPI.BinanceDB import BinanceDB as bDB
from datetime import datetime as dt
import GuapBot.HelperFunctions as HF
import numpy as np
import os,sys
import torch

def init(context, end_date, C1, C2):
	'''
	Stores initial values for each relevant variable
	'''
	symbol = C1 + C2
	context.database = MagicDB(context.timestep, context.time, end_date, bDB())
	first_100 = []
	first_100V = []
	timestep = HF.get_timestep_as_timedelta('1m')
	for i in range(100):
		price = context.get_historical_open_rate(symbol, context.time)
		volume = context.get_historical_volume(symbol, context.time)
		context.step(timestep)
		first_100.append(price)
		first_100V.append(volume)
	for num in ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]:
		val = int(num)
		context.variables["P{}".format(num)] = first_100[-val:]
		if val <= 50:
			context.variables["V{}".format(num)] = first_100V[-val:]
	context.buys[symbol] = []
	context.sells[symbol] = []
	context.variables[symbol] = price
	context.variables["NN"] = load_NN('Algorithms/NeuralNets/NET4.pth')
	context.graphs = [(symbol,)]


def strat(context, C1, C2):
	symbol = C1 + C2
	price = context.get_historical_open_rate(symbol, context.time)
	volume = context.get_historical_volume(symbol, context.time)
	if isinstance(price, float):
		
		vec = [price]
		mavgs = [sum(context.variables["P{}".format(num)])/int(num) 
					for num in ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]]
		vec.extend(mavgs)
		vec = normalize(vec)
		vavgs = normalize([sum(context.variables["V{}".format(num)])/int(num)
					for num in ["10", "20", "30", "40", "50"]])
		vec.extend(vavgs)
		NN = context.variables["NN"]
		xi = torch.from_numpy(np.array(vec)).float()
		pred = NN(xi)
		selection = pred.max(0)[1].item()

		if selection == 0 and pred[0].item() > .9997 and context.positions[C1] >0:
			context.sell(C1,C2, .3*context.positions[C1])
		elif selection == 1 and pred[1].item() > .9996 and context.positions[C2] >0:
			context.buy(C1,C2, .3*context.positions[C2])

		for num in ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]:
			last = context.variables['P{}'.format(num)][1:]
			last.append(price)
			context.variables['P{}'.format(num)] = last
			if int(num) <= 50:
				last = context.variables['V{}'.format(num)][1:]
				last.append(volume)
				context.variables['V{}'.format(num)] = last
		context.variables[symbol] = price

def normalize(vector):
	'''
	Given an array of similar values, minimax scales the data
	'''
	maxi = max(vector)
	mini = min(vector)
	rng = maxi-mini
	return [(i-mini)/rng for i in vector]

