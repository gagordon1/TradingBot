from datetime import date, timedelta, datetime as dt
from GuapBot.DataAnalysis import DataAnalysis as DA
import GuapBot.HelperFunctions as HF
import pytz
import pandas as pd

class MagicDB:
	def __init__(self, timestep, start_date, end_date, database):
		'''
		attributes:
		timestep - timestep as one of (1m, 5m, 15m, 1d)
		start_date, end_date - datetime object
 		timeseries - dictionary containing cached timeseries data where keys 
		are ticker strings and values are dictionaries of timestamp keys and 
		open price values as floats
		price_vectors - dictionary containing cached price vector data where 
		keys are ticker strings and values are nx2 numpy arrays of n prices
		and n times NOT IMPLEMENTED
		'''
		self.timestep = timestep
		self.start_date = start_date
		self.end_date = end_date
		self.timeseries = {}
		self.price_vectors = {} #NOT IMPLEMENTED
		self.DB = database

	def track_historical_stock_ticker(self, symbol, start, end):
		'''
		adds a stock to the timseries cache from after a specified start date
		as a string to an end date as a string
		'''
		data = self.DB.get_historical_timeseries([symbol], start, end, self.timestep)
		data_list = data[symbol]
		final = []
		for info in data_list:
			utc_time = self.get_timestamp_as_utc_time(info['t'])
			new = {'Timestamp': utc_time, 'Open': info['o'], 'High': info['h'], 
			'Low': info['l'], 'Close': info['c'], 'Volume': info['v']}
			final.append(new)
		df = pd.DataFrame(final)
		df.set_index('Timestamp', inplace = True)
		self.timeseries[symbol] = df

	def track_historical_crypto_ticker(self, symbol, start, end):
		final = []
		while start < end:
			data = self.DB.get_historical_timeseries([symbol], start, end, self.timestep)
			data_list = data[symbol]
			for info in data_list:
				utc_time = self.get_timestamp_as_utc_time(info['t'])
				new = {'Timestamp': utc_time, 'Open': info['o'], 'High': info['h'], 
				'Low': info['l'], 'Close': info['c'], 'Volume': info['v']}
				final.append(new)
			start = final[-1]['Timestamp'] + HF.get_timestep_as_timedelta(self.timestep)
		df = pd.DataFrame(final)
		df.set_index('Timestamp', inplace = True)
		self.timeseries[symbol] = df
		

	def get_crypto_value(self, symbol, time, type_):
		'''
		returns the value of a ticker given a datetime and string of the ticker
		valid types: 'Open', 'Low', 'High', 'Close', 'Volume'
		'''
		if symbol not in self.timeseries:
			self.track_historical_crypto_ticker(symbol, self.start_date, self.end_date)
		if time in self.timeseries[symbol].index:
			return self.timeseries[symbol].at[time, type_]
		return '{} data for symbol {} at time {} UTC N/A'.format(type_, symbol, time)
	
	def get_value(self, symbol, time, type_):
		'''
		returns the value of a ticker given a datetime and string of the ticker
		valid types: 'Open', 'Low', 'High', 'Close', 'Volume'
		'''
		if symbol not in self.timeseries:
			self.track_historical_stock_ticker(symbol, self.start_date, self.end_date)
		if time in self.timeseries[symbol].index:
			return self.timeseries[symbol].at[time, type_]
		return '{} data for symbol {} at time {} UTC N/A'.format(type_, symbol, time)

			

	def get_most_recent_price(self, symbol, time):
		'''
		given a symbol, finds the most recent open price.
		'''
		price = self.get_value(symbol, time, "Open")
		step = HF.get_timestep_as_timedelta(self.timestep)
		while isinstance(price, str):
			price = self.get_value(symbol, time, "Open")
			time -= step
		return price

	def get_next_price(self, symbol, time):
		'''
		given a symbol, finds the next valid open price.
		'''
		price = self.get_value(symbol, time, "Open")
		step = HF.get_timestep_as_timedelta(self.timestep)
		while isinstance(price, str):
			price = self.get_value(symbol, time, "Open")
			time += step
		return price



	def get_timestamp_as_utc_time(self, timestamp):
		'''
		convert a unix timestamp to utc time 
		'''
		utc_datetime = dt.fromtimestamp(timestamp, tz = pytz.utc)
		if self.timestep[-1] == 'd':
			utc_datetime = dt(utc_datetime.year, utc_datetime.month, utc_datetime.day, tzinfo = pytz.utc)
		return utc_datetime

	def get_ny_datetime(self, time):
		'''
		get NY time as datetime object of form "%Y-%m-%d %H:%M:%S" given UTC datetime
		'''
		eastern = pytz.timezone('US/Eastern')
		ny_dt = time.astimezone(eastern)
		return ny_dt


