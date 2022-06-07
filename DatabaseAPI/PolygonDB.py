import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) 
from GuapBot.APIinfo import AlpacaInfo as ALPACA
from GuapBot import HelperFunctions as HF
import requests
import json
import numpy as np
from datetime import date, timedelta, datetime as dt

class PolygonDB:
	def get_historical_timeseries(self, tickers, start, end, interval):
		'''
		given a list of string tickers, start and end dates as strings of the form "yyyy-mm-dd", 
		and an interval as a string of any of (1m,5m,15m,1d), returns timeseries data for the ticker as 
		a dictionary mapping string tickers to a list of interval dictionaries with fields
		't': time (seconds), 'o': open price, 'h': high price,'l': low price,'c': close price, and 
		'v': volume.
		'''
		timeseries = {}
		for symbol in tickers:
			list1 = self.get_single_historical_timeseries(symbol, start, end, interval)
			timeseries[symbol] = list1
		return timeseries

	def get_recent_timeseries(self, tickers, period, interval):
		'''
		given a list of string tickers,period as string of any of (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y), 
		and an interval as a string of any of (1m,5m,15m,1d), returns timeseries data for the ticker as 
		a dictionary mapping string tickers to a list of interval dictionaries with fields
		't': time (seconds), 'o': open price, 'h': high price,'l': low price,'c': close price, and 
		'v': volume.
		'''
		timeseries = {}
		for symbol in tickers:
			timeseries[symbol] = self.get_single_recent_timeseries(symbol, period, interval)
		return timeseries

	def get_single_historical_timeseries(self, ticker, start, end, interval):
		'''
		given a single string ticker, start and end dates as strings of the form "yyyy-mm-dd", 
		and an interval as a string of any of (1m,5m,15m,1d), returns timeseries data for the ticker as 
		a dictionary mapping string tickers to a list of interval dictionaries with fields
		't': time (seconds), 'o': open price, 'h': high price,'l': low price,'c': close price, and 
		'v': volume.
		'''
		span_conversion = {
		'1m': ('1', 'minute'),
		'2m': ('2', 'minute'),
		'5m': ('5', 'minute'),
		'15m': ('15', 'minute'),
		'30m': ('30', 'minute'),
		'60m': ('60', 'minute'),
		'90m': ('90', 'minute'),
		'1h': ('1', 'hour'),
		'1d': ('1', 'day'),
		'1wk': ('1', 'week'),
		'1mo': ('1', 'month'),
		'3mo': ('3', 'month')
		}
		multiplier = span_conversion[interval][0]
		timespan = span_conversion[interval][1]
		start = HF.get_string_day_from_datetime(start)
		end = HF.get_string_day_from_datetime(end)
		url = ALPACA.POLYGON_API_ENDPOINT + 'aggs/ticker/{}/range/{}/{}/{}/{}'.format(ticker, 
			multiplier, timespan, start, end)
		payload = {'apiKey': ALPACA.API_KEY_ID}
		response = requests.get(url, params = payload)
		data = json.loads(response.text)
		final = data['results']
		for point in final:
			point['t'] = point['t']/1000		
		return final

	def get_single_recent_timeseries(self, ticker, period, interval):
		'''
		given a single string ticker,period as string of any of (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y), 
		and an interval as a string of any of (1m,5m,15m,1d), returns timeseries data for the ticker as 
		a dictionary mapping string tickers to a list of interval dictionaries with fields
		't': time (seconds), 'o': open price, 'h': high price,'l': low price,'c': close price, and 
		'v': volume.
		'''
		today = date.today()
		start = HF.subtract_period(today, period)
		return self.get_single_historical_timeseries(ticker, str(start), str(today), interval)

	def snapshot(self):
		'''
		Snapshot allows you to see all tickers current minute aggregate, daily aggregate and last 
		trade as well as previous days aggregate and calculated change for today.
		'''
		url = ALPACA.POLYGON_API_ENDPOINT + 'snapshot/locale/us/markets/stocks/tickers'
		payload = {'apiKey': ALPACA.API_KEY_ID}
		response = requests.get(url, params = payload)
		data = json.loads(response.text)
		return data['tickers']

		




