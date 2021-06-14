import numpy as np
import math

class MC_EquityOptionPricer():
    '''
    Initializes a simple European equity option object with an option_price attribute.
    The option price is calculated by using Monte Carlo simulation.
    The price of the underlying equity is simulated as a brownian motion with constant drift and volatility.

    Parameters
    ----------
    option_type : str ("Call" or "Put")
        Indicates wether the option is of type call or put.
    spot : float (>0)
        spot price of the underlying equity.
    strike : float (>0)
        strike price of the option contract.
    r : float
        risk free rate.
    vol : float (>0)
        annualized volatility of the underlying equity.
    maturity : float (>0)
        time, in years, to maturity of the option contract.
    paths : int (default = 10000)
        number of simulations used to calculate the option price.
    '''

    def __init__(self, option_type, spot, strike, r, vol, maturity, paths=10000):

        # Argument Checks
        if not(str(option_type).upper()=='CALL' or str(option_type).upper()=='PUT'):
            raise ValueError('option_type argument must be either "Put" or "Call"')
        if spot < 0:
            raise ValueError('spot argument must be positive')
        if strike < 0:
            raise ValueError('strike argument must be positive')
        if vol < 0:
            raise ValueError('vol argument must be positive')
        if maturity < 0:
            raise ValueError('maturity argument must be positive')
        if paths < 0:
            raise ValueError('paths argument must be a positive integer')

        # Initializing Attributes
        self.option_type = option_type
        self.volatility = vol
        self.spot = spot
        self.strike = strike
        self.rate = r
        self.maturity = maturity
        self.paths = paths

        # Initialiing variables
        f1 = (r-0.5*(vol**2))*maturity
        f2 = math.sqrt(maturity)*vol
        disc = math.exp(-r*maturity)
        St_total = 0
        St_dist = []

        # Simulating n paths
        for i in range(0, paths):
            N = np.random.normal()
            St = spot*math.exp(f1 + f2*N)
            St_dist.append(St)

        St_dist = np.array(St_dist)

        # Calculating option payoff distribution
        if option_type.upper() == 'PUT':
            payoff = strike - St_dist
        else:
            payoff = St_dist - strike
        
        #Calculate option price
        for i in range(0, paths):
            if payoff[i] > 0:
                St_total += payoff[i]
            
            self.option_price = disc*(St_total/paths)



