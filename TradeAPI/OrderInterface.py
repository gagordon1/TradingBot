
class OrderInterface:
	def place_buy_market_order(self, symbol, quantity, TIF):

		'''
		symbol - string of the symbol or asset ID
		quantity - number of shares to buy as a string of an integer
		TIF - time in force, a code specifying under what circumstances a trade is valid.
			  can be any of {'day', 'gtc', 'opg', 'cls', 'ioc', 'fok'}
		
		A buy market order is a request to buy a security at the currently available market price
		This places a buy order that is valid for a duration specified by the time in force parameter.
		(see https://alpaca.markets/docs/trading-on-alpaca/orders/#time-in-force for details). 
		'''
		pass

	def place_sell_market_order(self, symbol, quantity, TIF):
		'''
		symbol - string of the symbol or asset ID
		quantity - number of shares to buy as a string of an integer
		TIF - time in force, a code specifying under what circumstances a trade is valid.
			  can be any of {'day', 'gtc', 'opg', 'cls', 'ioc', 'fok'}
		
		A sell market order is a request to sell a security at the currently available market price
		This places a sell order that is valid for a duration specified by the time in force parameter.
		(see https://alpaca.markets/docs/trading-on-alpaca/orders/#time-in-force for details). 
		'''
		pass

	def place_buy_limit_order(self, symbol, quantity, TIF, limit_price):
		'''
		symbol - string of the symbol or asset ID
		quantity - string of an integer
		TIF - time in force, a code specifying under what circumstances a trade is valid.
			  can be any of {'day', 'gtc', 'opg', 'cls', 'ioc', 'fok'}
		limit_price - string of a number 

		Places an order to buy a security at a specified price or above with the order being valid 
		for a duration specified by the time in force parameter.
		'''
		pass

	def place_sell_limit_order(self, symbol, quantity, TIF, limit_price):
		'''
		symbol - string of the symbol or asset ID
		quantity - string of an integer
		TIF - time in force, a code specifying under what circumstances a trade is valid.
			  can be any of {'day', 'gtc', 'opg', 'cls', 'ioc', 'fok'}
		limit_price - string of a number 

		Places an order to sell  a security at a specified price or above with the order being valid 
		for a duration specified by the time in force parameter.
		'''
		pass

	def place_buy_stop_order(self, symbol, quantity, TIF, stop_prie):
		'''
		symbol - string of the symbol or asset ID
		quantity - string of an integer
		TIF - time in force, a code specifying under what circumstances a trade is valid.
			  can be any of {'day', 'gtc', 'opg', 'cls', 'ioc', 'fok'}
		stop_price - string of a number 

		A buy stop (market) order is an order to buy a security when its price moves above a 
		particular point, ensuring a higher probability of achieving a predetermined entry or 
		exit price. Once the market price crosses the specified stop price, the stop order becomes 
		a market order.
		'''
		pass
	def place_sell_stop_order(self, symbol, quantity, TIF, stop_price):
		'''
		symbol - string of the symbol or asset ID
		quantity - string of an integer
		TIF - time in force, a code specifying under what circumstances a trade is valid.
			  can be any of {'day', 'gtc', 'opg', 'cls', 'ioc', 'fok'}
		stop_price - string of a number 

		A sell stop (market) order is an order to ell a security when its price moves below a 
		particular point, ensuring a higher probability of achieving a predetermined entry or 
		exit price. Once the market price crosses the specified stop price, the stop order 
		becomes a market order.
		'''
		pass
	def place_buy_stop_limit_order(self, symbol, quantity, TIF, stop_price):
		'''
		symbol - string of the symbol or asset ID
		quantity - string of an integer
		TIF - time in force, a code specifying under what circumstances a trade is valid.
			  can be any of {'day', 'gtc', 'opg', 'cls', 'ioc', 'fok'}
		stop_price - string of a number 
		limit_price - string of a number 

		The buy stop-limit order will be executed at a specified limit price, or better, after a 
		given stop price has been reached. Once the stop price is reached, the stop-limit order 
		becomes a limit order to buy at the limit price or lower.
		'''
		pass
	def place_sell_stop_limit_order(self, symbol, quantity, TIF, stop_price):
		'''
		symbol - string of the symbol or asset ID
		quantity - string of an integer
		TIF - time in force, a code specifying under what circumstances a trade is valid.
			  can be any of {'day', 'gtc', 'opg', 'cls', 'ioc', 'fok'}
		stop_price - string of a number 
		limit_price - string of a number 

		The sell stop-limit order will be executed at a specified limit price, or better, after 
		a given stop price has been reached. Once the stop price is reached, the stop-limit order 
		becomes a limit order to sell at the limit price or higher.
		'''
		pass
	def get_open_orders(self):
		'''
		Returns orders that have been placed but not completed as a list of order objects
		'''
		pass
	def get_positions(self):
		'''
		Returns current positions as a list of position objects
		'''
		pass



