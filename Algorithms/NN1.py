from GuapBot.Algorithms.NeuralNets.Nets import load_NN
from GuapBot.Simulators.CryptoSim import context
from GuapBot.MagicDB import MagicDB
from GuapBot.DatabaseAPI.BinanceDB import BinanceDB as bDB
import GuapBot.HelperFunctions as HF
from datetime import datetime as dt
import numpy as np
import os,sys
import torch

def init(context, end_date, C1, C2):
	'''
	Stores initial values for each relevant variable
	'''
	symbol = C1 + C2
	context.database = MagicDB(context.timestep, context.time, end_date, bDB())
	first_50 = []
	first_50V = []
	timestep = HF.get_timestep_as_timedelta('1m')
	for i in range(50):
		price = context.get_historical_open_rate(symbol, context.time)
		volume = context.get_historical_volume(symbol, context.time)
		first_50.append(price)
		first_50V.append(volume)
		context.step(timestep)
	V10 = first_50V[40:]
	V20 = first_50V[30:]
	V30 = first_50V[20:]
	V40 = first_50V[10:]
	last_10 = first_50[40:]
	last_20 = first_50[30:]
	last_30 = first_50[20:]
	last_40 = first_50[10:]
	context.buys[symbol] = []
	context.sells[symbol] = []
	context.variables['P10'] = last_10
	context.variables['P20'] = last_20
	context.variables['P30'] = last_30
	context.variables['P40'] = last_40
	context.variables['P50'] = first_50
	context.variables['PMA10'] = sum(last_10)/10
	context.variables['PMA20'] = sum(last_20)/20
	context.variables['PMA30'] = sum(last_30)/30
	context.variables['PMA40'] = sum(last_40)/40
	context.variables['PMA50'] = sum(first_50)/50
	context.variables['V10'] = V10
	context.variables['V20'] = V20
	context.variables['V30'] = V30
	context.variables['V40'] = V40
	context.variables['V50'] = first_50V
	context.variables['VMA10'] = sum(V10)/10
	context.variables['VMA20'] = sum(V20)/20
	context.variables['VMA30'] = sum(V30)/30
	context.variables['VMA40'] = sum(V40)/40
	context.variables['VMA50'] = sum(first_50V)/50
	context.variables[symbol] = price
	context.variables["NN"] = load_NN('Algorithms/NeuralNets/NET2.pth')
	context.graphs = [(symbol,'PMA10', 'PMA50')]


def strat(context, C1, C2):
	symbol = C1 + C2
	price = context.get_historical_open_rate(symbol, context.time)
	volume = context.get_historical_volume(symbol, context.time)
	if isinstance(price, float):
		for num in ['10', '20', '30', '40', '50']:
			context.variables['PMA{}'.format(num)] = sum(context.variables['P{}'.format(num)])/int(num)
			context.variables['VMA{}'.format(num)] = sum(context.variables['V{}'.format(num)])/int(num)
		context.variables[symbol] = price
		[V10,V20,V30,V40,V50] = [context.variables['VMA{}'.format(num)] for num in ["10", "20", "30", "40", "50"]]
		[P10,P20,P30,P40,P50] = [context.variables['PMA{}'.format(num)] for num in ["10", "20", "30", "40", "50"]]
		NN = context.variables["NN"]
		vec = []
		pavgs = [price, P10,P20,P30,P40,P50]
		pavgs = normalize(pavgs)
		for p in pavgs: vec.append(p)
		vavgs = [V10,V20,V30,V40,V50]
		vavgs = normalize(vavgs)
		for v in vavgs: vec.append(v)
		xi = torch.from_numpy(np.array(vec)).float()
		pred = NN(xi)
		selection = pred.max(0)[1].item()
		

		if selection == 0 and pred[0].item() > .999999:
			context.sell(C1,C2, .3*context.positions[C1])
		elif selection == 2 and pred[2].item() > .9988:
			context.buy(C1,C2, .3*context.positions[C2])

		for num in ['10', '20', '30', '40', '50']:
			last = context.variables['P{}'.format(num)][1:]
			last.append(price)
			context.variables['P{}'.format(num)] = last
			last = context.variables['V{}'.format(num)][1:]
			last.append(volume)
			context.variables['V{}'.format(num)] = last


def normalize(vector):
	'''
	Given an array of similar values, minimax scales the data
	'''
	maxi = max(vector)
	mini = min(vector)
	rng = maxi-mini
	return [(i-mini)/rng for i in vector]








