from GuapBot.APIinfo import AlpacaInfo as ALPACA
from GuapBot import HelperFunctions as HF
import requests
import json
import numpy as np
from datetime import date, timedelta, datetime as dt

class IexDB:
			
	def get_historical_timeseries(self, tickers, start, end, interval):
		'''
		given a list of string tickers, start and end dates as datetime objects, 
		and an interval as a string of any of (1m,5m,15m,1d), returns timeseries data for the ticker as 
		a dictionary mapping string tickers to a list of interval dictionaries with fields
		't': time (seconds), 'o': open price, 'h': high price,'l': low price,'c': close price, and 
		'v': volume. ONLY RETURNS 1000 :(
		'''
		span_conversion = {
		'1m': '1Min',
		'5m': '5Min',
		'15m': '15Min',
		'1d': '1D'
		}
		url = ALPACA.IEX_API_ENDPOINT + '/bars/{}'.format(span_conversion[interval])
		payload = {'start': HF.get_iso_format_from_datetime(start), 'end': HF.get_iso_format_from_datetime(end), 
		'symbols': HF.get_comma_separated_string(tickers), 'limit': 1000}
		headers = {'APCA-API-KEY-ID': ALPACA.API_KEY_ID, 'APCA-API-SECRET-KEY': ALPACA.API_SECRET_KEY}
		data = json.loads(requests.get(url, params = payload, headers = headers).text)
		return data


	def get_recent_timeseries(self, tickers, period, interval):
		'''
		given a list of string tickers,period as string of any of (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y), 
		and an interval as a string of any of (1m,5m,15m,1d), returns timeseries data for the ticker as 
		a dictionary mapping string tickers to a list of interval dictionaries with fields
		't': time (seconds), 'o': open price, 'h': high price,'l': low price,'c': close price, and 
		'v': volume.
		'''
		today = date.today()
		start = HF.subtract_period(today, period)
		return self.get_historical_timeseries(tickers, str(start), str(today), interval)

