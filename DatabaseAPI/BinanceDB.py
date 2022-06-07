from GuapBot.APIinfo import BinanceInfo as BINANCE
from GuapBot import HelperFunctions as HF
import requests
import json
import random


class BinanceDB:
	def get_historical_timeseries(self, tickers, start, end, interval):
		'''
		given a list of string tickers, start and end dates as datetime objects, 
		and an interval as a string of any of (1m,5m,15m,1d), returns timeseries data for the ticker as 
		a dictionary mapping string tickers to a list of interval dictionaries with fields
		't': time (seconds), 'o': open price, 'h': high price,'l': low price,'c': close price, and 
		'v': volume.
		'''
		start = int(start.timestamp()*1000)
		end = int(end.timestamp()*1000)
		final = {}
		for ticker in tickers:
			payload = {"symbol": ticker, "limit": 1000, "interval": interval, "startTime": start, "endTime": end}
			response = requests.get(BINANCE.BINANCE_BASE + BINANCE.OHLC_ENDPOINT, params = payload)
			resp = json.loads(response.text)
			code = response.status_code
			if code == 429:
				print('Broken request rate limit!')
				return None
			elif code == 418:
				print('Rate limited too many times, auto-banned!')
				return None
			f = []
			for i in resp:
				open_time = int(float(i[0])/1000)
				Open = float(i[1])
				High = float(i[2])
				Low = float(i[3])
				Close = float(i[4])
				Volume = float(i[5])
				close_time = int(float(i[6])/1000)
				f.append({'t': open_time, 'o':Open, 'h':High, 'l':Low, 'c':Close, 'v': Volume})
			final[ticker] = f
		return final


	def get_24hr_price_change_stats(self):
		'''
		Returns 24hr price change stats for every ticker on binance
		'''
		response = requests.get(BINANCE.BINANCE_BASE + BINANCE.PRICE_CHANGE_STATS)
		return json.loads(response.text)

	def get_recent_timeseries(self, tickers, period, interval):
		'''
		given a list of string tickers,period as string of any of (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y), 
		and an interval as a string of any of (1m,5m,15m,1d), returns timeseries data for the ticker as 
		a dictionary mapping string tickers to a list of interval dictionaries with fields
		't': time (seconds), 'o': open price, 'h': high price,'l': low price,'c': close price, and 
		'v': volume.
		'''
		pass