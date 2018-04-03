import pandas as pd
import numpy as np
import math
import datetime
import time
from WebStockReader import WebReader as web


# List of securities to analyze
_SECURITIES = ['fb', 'aapl', 'amzn', 'nflx', 'googl']

# Change service used to get data (yahoo, google, etc.). TIINGO only currently available
_SERVICE = 'tiingo'

'''
# Options for API call. If your selected service requires an API key for authentication,
# this parameter must be provided here. To set an option to default simply comment it out or delete
# it from the dictionary.
# Options
# 'key' - API authentication key (required for Tiingo, Quandl, etc.)
# 'start' - date to begin analysis. DEFAULT: Jan 1, 2010
# 'end' - date to end analysis. DEFAULT: today
# 'log' - use log returns if true, otherwise simple returns DEFAULT: False
# 'rfr' - define the Risk Free Rate (for calculation of Sharpe ratio). DEFAULT: 0
'''
_OPTIONS = {
	'key': '',
	# 'start': datetime.datetime(2009, 3, 9),
	# 'end': datetime.datetime.now(),
	'log': True,
	'rfr': 0.0215,

}

# Number of iterations if using Monte Carlo. Default 10,000
_SIMS = 100000

# Number of maximized solutions to return (i.e. 10 largest sharpe ratio weights)
_N = 0

# Weights to be used if retrieving sharpe ratio of portfolio with known weights
_WEIGHTS = {
	'fb': .35,
	'aapl': .15,
	'nflx': .30,
	'googl': .2,
}


class Optimizer(object):
	'''
	Class for optimizing portfolio. Monte Carlo function return the weights of securities
	that maximize Sharpe ratio. Get Sharpe function returns the sharpe ratio for
	a portfolio of given weights of individual securities
	'''

	def __init__(self, securities, service, **kwargs):

		self.securities = securities
		self.service = service

		'''
		Call function that iterates through the securities and queries API
		Function returns a pandas multiIndexed dataframe with the top column
		describing the type of data (ope, close, volume, adjusted close, etc.).
		Calling a data type in this definition allows for quick analysis
		'''
		self.data = web().get(securities, service, **kwargs)['adjClose']
		# Determine if using log returns or standard, then define returns
		if 'log' in kwargs and kwargs['log']:
			self.ret = np.log(self.data).diff()
		else:
			self.ret = self.data.pct_change()

		# Define mean daily portfolio return
		self.ret_mean = self.ret.mean()

		# Define covariance matrix based on returns above
		self.cov = self.ret.cov()

		# Define the risk free rate for sharpe ratio
		if 'rfr' in kwargs:
			self.rfr = kwargs['rfr']
		else:
			self.rfr = 0

	def moneCarlo(self, sims, n=0):
		'''
		Function for running monte carlo simulation
		Outputs 2 variables

		Inputs:
		sims: Integer - Number of iterations to run
		n: Integer - Number of maximized values to return

		Outputs:
		max_sharpe: Pandas Series - Weights of assets to maximize the sharpe ratio
		min_vol: Pandas Series - Weights of assets to minimize volatility
		'''

		# Have a local reference copy of the securities property
		securities = self.securities
		# Numpy array to hold results from each iteration of the simulation
		# results = np.zeros((sims, len(securities) + 3))
		results = []
		# Iterate over the number of monte carlo simulations provided
		# each iteration represents a random possible weight
		for i in range(sims):
			# Numpy array of randomly generated weights for the securities
			weights = np.array(np.random.random(len(securities)))
			# Normalize these weights so that they add to 100%
			weights /= np.sum(weights)
			# Round the weights to whole percentages
			weights = np.around(weights, decimals=2)
			# Calculate portfolio overall anualized return given daily returns and weights
			portfolio_return = np.sum(self.ret_mean * weights) * 252
			# Calculate portfolio standard deviaiton given weights and returns
			portfolio_std = math.sqrt(np.dot(weights.T, np.dot(self.cov, weights))) * math.sqrt(252)
			# Create iteration results list appending values of Return, Volatility, and Sharpe Ratio
			iterres = [portfolio_return, portfolio_std, (portfolio_return - self.rfr) / portfolio_std]
			# Add the asset weights to the iteration list
			for j in range(len(weights)):
				iterres.append(weights[j])
			# Append the iteration list (which will be overwritten each iteration) to the master results list
			results.append(iterres)
		# Cast the results list as a numpy array after all iterations
		results = np.array(results)
		# Define colums for resultant pandas dataframe
		cols = ['Returns', 'StdDev', 'Sharpe']
		# Add the security names to the columns
		for security in securities:
			cols.append(security)
		# Define the result pandas Dataframe to be returned
		resultFrame = pd.DataFrame(results, columns=cols)
		# return results
		# If user wants the n maximum returns or the single max sharpe ratio
		# Use the same process for minimized volatility
		if n > 0:
			max_sharpe = resultFrame.nlargest(n, 'Sharpe')
			min_vol = resultFrame.nsmallest(n, 'StdDev')
		else:
			max_sharpe = resultFrame.iloc[resultFrame['Sharpe'].idxmax()]
			min_vol = resultFrame.iloc[resultFrame['StdDev'].idxmin()]

		# Return the Pandas Series for maximized sharpe ratio and minimized volatility
		return max_sharpe, min_vol

	def getSharpe(self, weights):
		'''
		Function for getting the Sharpe ratio of a portfolio with known weights
		Returns 1 variable

		Input:
		weights: Dict - dictionary describing weight associated with each security

		Output:
		Sharpe Ratio: PandasSeries - Array describing the return, standard deviation,
									and sharpe ratio of the portfolio
		'''
		if not isinstance(weights, dict):
			raise TypeError('Weights must be of type dictionary with the asset key matching to the security')
		# Local reference to securities
		securities = self.securities
		# Populate a weights list using the order of securities lsit
		port_weights = []
		for asset in securities:
			if weights[asset] <= 1:
				port_weights.append(weights[asset])
			else:
				port_weights.append(weights[asset] / 100)
		# Cast list as numpy array
		port_weights = np.array(port_weights)
		# Calculate annualized portfolio return and standard deviation given weights
		portfolio_return = np.sum(self.ret_mean * port_weights) * 252
		portfolio_std = math.sqrt(np.dot(port_weights.T, np.dot(self.cov, port_weights))) * math.sqrt(252)
		# Calculate sharpe ratio
		Sharpe = (portfolio_return - self.rfr) / portfolio_std
		# Cast variables as pandas series
		results = pd.Series([portfolio_return, portfolio_std, Sharpe], index=['Return', 'StdDev', 'Sharpe'])
		# Return this series
		return results


if __name__ == "__main__":
	try:
		# Uncomment this for calculation of portfolios with maximum sharpe ratio
		max_sharpe, min_vol = Optimizer(_SECURITIES, _SERVICE, **_OPTIONS).moneCarlo(_SIMS, _N)
		print('Min Vol:\n' + str(min_vol))
		print('Max Sharpe:\n' + str(max_sharpe))

		# Uncomment Below to calculate sharpe ratio of known weighted assets
		# sharpe = Optimizer(_SECURITIES, _SERVICE, **_OPTIONS).getSharpe(_WEIGHTS)
		# print(sharpe)
	except Exception as e:
		print(e)
