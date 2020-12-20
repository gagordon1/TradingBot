from DatabaseAPI.IexDB import IexDB as iDB
from datetime import timedelta, datetime as dt
import HelperFunctions as HF
from MagicDB import MagicDB as mDB
import pytz
import pandas as pd

class context:
    def __init__(self, budget, time, timestep, positions, verbose):
        '''
        Initialize simulator with an integer budget and magic database
        cash - float amount of cash
        positions- dictionary mapping string symbols to shares owned as a float
        time - datetime object representing current time of the context
        timestep - (1m,5m,15m,1d)
        '''
        self.cash = budget
        self.positions = positions
        self.time = time
        self.timestep = timestep
        self.buys = {}
        self.sells = {}
        self.database = None
        self.variables = {}
        self.graphs = []
        self.graph_data = []
        self.verbose = verbose

    def __str__(self):
        time = 'Time: ' + self.get_ny_datetime_string() + ' ET'
        cash = 'Cash: ' + str(self.cash)
        port_value = 'Portfolio Value: ' + str(self.get_portfolio_value())
        total_value = 'Total Value: ' + str(self.total_asset_value())
        posits = 'Positions:' + '\n'
        for position in self.positions:
            nex = position + ' ' + str(self.positions[position]) + '\n'
            posits += nex
        
        return time + '\n' + cash + '\n' + total_value + '\n' + port_value +'\n' + posits

    def get_portfolio_value(self):
        total = 0
        for position in self.positions:
            total += self.database.get_most_recent_price(position, self.time)*self.positions[position]
        return total
    def total_asset_value(self):
        return self.cash + self.get_portfolio_value()

    #ORDER FUNCTIONS
    def buy_position(self, symbol, quantity):
        '''
        This adds a security at a given to add to our account.

        **Eventually draw price from our dataset directly rather
        an as an input**
        '''
        
        price = self.database.get_value(symbol, self.time, "Open")
        if isinstance(price, str):
            if self.verbose:
                print(price)
        else:
            self.cash -= quantity * price
            if symbol in self.positions:
                self.positions[symbol] += quantity
                self.buys[symbol].append(self.time)
            else:
                self.positions[symbol] = quantity
                self.buys[symbol] = [self.time]
            
            if self.verbose:   
                    print('bought {} shares of {} for {}$ at {}'.format(quantity, symbol, 
                        price, self.get_ny_datetime_string()))
            

    def sell_position(self, symbol, quantity):
        '''
        This sells a security at a given quantity from our account.
        '''
        
        price = self.database.get_value(symbol, self.time, "Open")
        if isinstance(price, str):
            if self.verbose:  
                print(price)
        else:
            self.cash += quantity * price
            self.positions[symbol] -= quantity
            if symbol in self.sells:
                self.sells[symbol].append(self.time)
            else:
                self.sells[symbol] = [self.time]
            if self.verbose:  
                print('sold {} shares of {} for {}$ at {}'.format(quantity, symbol, price, self.get_ny_datetime_string()))

    def advance_to_valid_price(self, ticker):
        '''
        for a given symbol, advance context to the first valid price
        '''
        price = ''
        step = HF.get_timestep_as_timedelta(self.timestep)
        while isinstance(price, str):
            price = self.get_historical_open_price(ticker, self.time)
            self.time += step
        return price


    def get_historical_open_price(self, ticker, time):
        '''
        for a given ticker and datetime object, gets the value of the ticker's open price
         at that time
        '''
        return self.database.get_value(ticker, time, "Open")

    def get_current_volume(self, ticker):
        '''
        For a given ticker, gets the current volume based on the simulations time
        '''
        return self.database.get_value(ticker, self.time, "Volume")

    def get_historical_volume(self, ticker, time):
        '''
        For a given ticker, gets the volume based on the given datetime object
        '''
        return self.database.get_value(ticker, time, "Volume")

    def step(self, time_step):
        '''
        given timedelta object time_step advances the state's time
        '''
        if time_step == HF.get_timestep_as_timedelta('1m'):
            if HF.valid_US_stock_minute(self.time):
                self.time += time_step
            else:
                while not HF.valid_US_stock_minute(self.time):
                    self.time += time_step
        
        elif time_step == HF.get_timestep_as_timedelta('1d'):
            if HF.valid_US_market_day(self.time):
                self.time += time_step
            else:
                while not HF.valid_US_market_day(self.time):
                    self.time += time_step
    
    def get_ny_datetime_string(self):
        '''
        get current NY time as string of form "%Y-%m-%d %H:%M:%S"
        '''
        eastern = pytz.timezone('US/Eastern')
        ny_dt = self.time.astimezone(eastern)
        fmt = '%Y-%m-%d  %H:%M:%S'
        return ny_dt.strftime(fmt)

    def get_ny_datetime(self):
        '''
        get current NY time as datetime object of form "%Y-%m-%d %H:%M:%S"
        '''
        eastern = pytz.timezone('US/Eastern')
        ny_dt = self.time.astimezone(eastern)
        return ny_dt

    def update_chart_data(self):
        '''
        during a simulation, environmental variables that are specified to be graphed in 
        self.to_graph will be added to a dictionary where vars map to dictionaries with value
        and timestamp timeseries
        '''

        if self.timestep[-1] == "m":
            for graph in self.graph_data:
                for v in graph:
                    graph[v]["Value"].append(self.variables[v])
                    graph[v]["Timestamp"].append(self.get_ny_datetime())
        elif self.timestep[-1] == "d":
            for graph in self.graph_data:
                for v in graph:
                    graph[v]["Value"].append(self.variables[v])
                    graph[v]["Timestamp"].append(self.time)
    def initialize_graph(self):
        '''
        In an init function, each graph will be specified by the variables associated with it in
        self.graphs as a list of tuples. This fuction initializes the graph_data attribute
        '''
        if self.timestep[-1] == "m":
            for i in range(len(self.graphs)):
                graph = {}
                for var in self.graphs[i]:
                    graph[var] = {"Value": [self.variables[var]],
                            "Timestamp": [self.get_ny_datetime()]}
                self.graph_data.append(graph)
        elif self.timestep[-1] == "d":
            for i in range(len(self.graphs)):
                graph = {}
                for var in self.graphs[i]:
                    graph[var] = {"Value": [self.variables[var]],
                            "Timestamp": [self.time]}
                self.graph_data.append(graph)
                

def simulate(initialize, strategy, start_date, end_date, time_step, budget, verbose = False, symbol = None):
    '''
    Advances a strategy between two datetimes start_date and end_date
    strategy - function that given a context, updates it to the next state
    start_date - datetime object
    end_date - datetime object
    context - object that gives represents an envrionment for a strategy to make decisions
    upon
    '''
    positions = {}
    start_date = pytz.utc.localize(start_date)
    end_date = pytz.utc.localize(end_date)
    con = context(budget, start_date, time_step, positions, verbose = verbose)
    initialize(con, end_date, symbol)                                #gets initial variables their values
    con.initialize_graph()                                   #sets up each graph according to the "to_graph" attribute specified in initialize
    timestep = HF.get_timestep_as_timedelta(time_step)
    while con.time <= end_date:
        strategy(con, symbol)                                        #updates the specified variables
        con.update_chart_data()
        con.step(timestep)
    return con


