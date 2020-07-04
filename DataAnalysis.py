import GuapBot.HelperFunctions as HF
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd

class DataAnalysis:
	def convert_OHLC_to_pandas(self, data_list):
		'''
		given OHLC data as returned by IEXDB, return a pandas dataframe with index
		"Date" and "Open", "High", "Low", and "Close" fields.
		'''
		final = []
		for info in data_list:
			utc_time = HF.get_utc_from_timestamp(info['t'])
			new = {'Timestamp': utc_time, 'Open': info['o'], 'High': info['h'], 
			'Low': info['l'], 'Close': info['c'], 'Volume': info['v']}
			final.append(new)

		df = pd.DataFrame(final)
		df.set_index('Timestamp', inplace = True)
		return df

	def plot_sim_graph_data(self, graph_data, buys = None, sells = None):
		'''
		given a dictionary mapping index names to dictionaries containing value and time fields
		mapped to timeseries data as a list
		buys - dictionary mapping symbols to times of purchase
		sells - dictionary mapping symbols to when they were sold
		'''
		
		for graph in graph_data:
		    time_frame = 0
		    best_i = None
		    for i in graph:
		        if len(graph[i]['Value']) > time_frame:
		            time_frame = len(graph[i]['Value'])
		            best_i = i
		    times = graph[best_i]['Timestamp']
		    style.use('seaborn')
		    plt.xticks(ticks = [i for i in range(0, time_frame, time_frame//15)], 
		            labels = [HF.get_datetime_string(times[i]) 
		            for i in range(0,time_frame,time_frame//15)],
		              rotation = 30)
		    for var in graph:
		        data = graph[var]['Value']
		        var_times = graph[var]['Timestamp']
		        x = [times.index(i) for i in var_times]
		        if buys != None and var in buys:
		            mark = [times.index(elt) for elt in buys[var]]
		            plt.plot(x, data, marker = 6, label = var + ' Buys', markevery =mark)
		          
		        if sells != None and var in sells:
		            mark = [times.index(elt) for elt in sells[var]]
		            plt.plot(x, data, marker = 7, label = var+ ' Sells', markevery =mark)
		        else:
		            plt.plot(x, data, label = var)
		    plt.grid(True)
		    plt.legend(loc="upper right")
		    plt.show()

	def plot(self, symbol, start, end, interval, DB):
		'''
		Given a symbol, start and end date, plots the data over each time in the given window
		Specify a database as a class.
		'''
		style.use('seaborn')
		dB = DB()
		s = HF.get_string_day_from_datetime(start)
		e = HF.get_string_day_from_datetime(end)
		data = dB.get_historical_timeseries([symbol], s, e, interval)[symbol]
		df = self.convert_OHLC_to_pandas(data)
		for time in df['Open']:
			if time < 8000:
				print(time)
		plt.plot(df['High'])
		plt.show()















