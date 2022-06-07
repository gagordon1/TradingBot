from datetime import timedelta, datetime as dt
import GuapBot.HelperFunctions as HF
from GuapBot.MagicDB import MagicDB as mDB
import pytz
import pandas as pd

class context:
    def __init__(self, time, timestep, positions, verbose):
        '''
        Initialize simulator with an integer budget and magic database
        cash - float amount of cash
        positions- dictionary mapping string symbols to shares owned as a float
        time - datetime object representing current time of the context
        timestep - (1m,5m,15m,1d)
        '''
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
        stri = 'Time: ' + HF.get_datetime_string(self.time) + ' Positions: ' + str(self.positions) + '\n'
        total = 'Total Value: ' + str(self.get_BTC_value())
        return stri + total

    def get_BTC_value(self):
        total = 0
        for position in self.positions:
            if position != 'BTC':
                BTCval = self.positions[position]*(self.get_historical_open_rate(
                    '{}BTC'.format(position),self.time))
                total += BTCval
            else:
                total += self.positions['BTC']
        return total

    #ORDER FUNCTIONS
    def buy(self, C1, C2, quantity):
        '''
        buys an amount of C1 given quantity amount of base currency C2
        '''

        rate = self.get_historical_open_rate(C1+C2, self.time) #C2/C1
        self.add_value(C2, -quantity)
        self.add_value(C2, -quantity*.00075) #FEE
        self.add_value(C1, quantity/rate)
        self.buys[C1+C2].append(self.time)

    def sell(self,C1,C2,quantity):
        '''
        buys an amount of the base currency C2 with quantity amount of currency C1
        NOW accounts for Bittrex fee
        '''
        rate = self.get_historical_open_rate(C1+C2, self.time) #C1/C2
        self.add_value(C2, quantity*rate)
        self.add_value(C1, -quantity)
        self.add_value(C2, -quantity*rate*.00075) #FEE
        self.sells[C1+C2].append(self.time)


    def add_value(self, currency, amount):
        if currency in self.positions:
            self.positions[currency] += amount
        else:
            self.positions[currency] = amount

    def get_historical_open_rate(self, ticker, time):
        '''
        for a given ticker and datetime object, gets the value of the ticker's open price
         at that time
        '''
        return self.database.get_crypto_value(ticker, time, "Open") #C1/C2
        

    def get_current_volume(self, ticker):
        '''
        For a given ticker, gets the current volume based on the simulations time
        '''
        return self.database.get_crypto_value(ticker, self.time, "Volume")

    def get_historical_volume(self, ticker, time):
        '''
        For a given ticker, gets the volume based on the given datetime object
        '''
        return self.database.get_crypto_value(ticker, time, "Volume")

    def step(self, time_step):
        '''
        given timedelta object time_step and valid market, advances the state's time
        '''
        self.time += time_step

    def update_chart_data(self):
        '''
        during a simulation, environmental variables that are specified to be graphed in 
        self.to_graph will be added to a dictionary where vars map to dictionaries with value
        and timestamp timeseries
        '''
        for graph in self.graph_data:
            for v in graph:
                graph[v]["Value"].append(self.variables[v])
                graph[v]["Timestamp"].append(self.time)

    def initialize_graph(self):
        '''
        In an init function, each graph will be specified by the variables associated with it in
        self.graphs as a list of tuples. This fuction initializes the graph_data attribute
        '''

        for i in range(len(self.graphs)):
            graph = {}
            for var in self.graphs[i]:
                graph[var] = {"Value": [self.variables[var]],
                        "Timestamp": [self.time]}
            self.graph_data.append(graph)
                

def simulate(initialize, strategy, start_date, end_date, time_step, positions, C1, C2, verbose = False):
    '''
    Advances a strategy between two datetimes start_date and end_date
    strategy - function that given a context, updates it to the next state
    start_date - datetime object
    end_date - datetime object
    context - object that gives represents an envrionment for a strategy to make decisions
    upon
    '''
    start_date = pytz.utc.localize(start_date)
    end_date = pytz.utc.localize(end_date)
    con = context(start_date, time_step, positions, verbose = verbose)

    initialize(con, end_date, C1, C2)                                #gets initial variables their values
    con.initialize_graph()                                   #sets up each graph according to the "to_graph" attribute specified in initialize
    timestep = HF.get_timestep_as_timedelta(time_step)
    while con.time < end_date:
        strategy(con, C1, C2)                                        #updates the specified variables
        con.update_chart_data()
        con.step(timestep)
    return con


