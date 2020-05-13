
class DbInterface:
	def get_historical_timeseries(self, tickers, start, end, interval):
		'''
		given a list of string tickers, start and end dates as datetime objects 
		and an interval as a string of any of (1m,5m,15m,1d), returns timeseries data for the ticker as 
		a dictionary mapping string tickers to a list of interval dictionaries with fields
		't': time (seconds), 'o': open price, 'h': high price,'l': low price,'c': close price, and 
		'v': volume.
		'''
		pass
	def get_recent_timeseries(self, tickers, period, interval):
		'''
		given a list of string tickers,period as string of any of (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y), 
		and an interval as a string of any of (1m,5m,15m,1d), returns timeseries data for the ticker as 
		a dictionary mapping string tickers to a list of interval dictionaries with fields
		't': time (seconds), 'o': open price, 'h': high price,'l': low price,'c': close price, and 
		'v': volume.
		'''
		pass

#INTERVAL DATA STRUCTURE
interval_dictionary = {
	't': timestamp, #seconds 
	'o': open_price, 
	'h': high_price,
	'l': low_price,
	'c': close_price,
	'v': volume
}

