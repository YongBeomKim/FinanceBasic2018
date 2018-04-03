import pandas as pd
import datetime


class WebReader(object):

	def __init__(self):

		'''
		Define key/value pairs for different functions given
		provider input from user
		'''
		self.getService = {
			'tiingo': self.getTiingo,
			'google': self.getGoogle,
		}

		'''
		Set list of providers that require key or token
		for authentication
		'''
		self.key_required = ['tiingo', 'quandl']

		'''
		Set start and end date in case not input by user
		Default start: Jan 1, 2010
		Default End: Today
		'''
		self.start = datetime.datetime(2010, 1, 1).strftime("%Y-%m-%d")
		self.end = datetime.datetime.now().strftime("%Y-%m-%d")

	def get(self, stock, service, **kwargs):
		'''
		Certain providers require an API key or token for authentication.
		We ensure that the 'key' parameter is provided in the call for
		these services
		'''
		if service.lower() in self.key_required and 'key' not in kwargs or len(kwargs['key']) == 0:
			raise KeyError('Must include API key for %s' % service.upper())
		elif 'key' in kwargs and len(kwargs['key']) > 0:
			self.key = kwargs['key']

		'''
		QC check to ensure that the input security is of type string, or an array.
		Then cast to an array for use in service
		'''
		if isinstance(stock, str):
			self.stock = [stock]
		elif isinstance(stock, list):
			self.stock = stock
		else:
			raise ValueError('Unknown type for stock. Must be string or list of strings')

		'''
		If 'start' and 'end' arguments entered, will override
		the defaults of Jan 1, 2010 and today
		'''
		# Check to ensure start and end are 'datetime' objects and define accordingly
		if 'start' in kwargs:
			if not isinstance(kwargs['start'], datetime.datetime):
				raise ValueError('Start Time must be of type datetime')
			else:
				self.start = kwargs['start'].strftime("%Y-%m-%d")
		if 'end' in kwargs:
			if not isinstance(kwargs['end'], datetime.datetime):
				raise ValueError('End Time must be of type datetime')
			else:
				self.end = kwargs['end'].strftime("%Y-%m-%d")

		# Call the unique service for each provider supported
		return self.getService[service]()

	def getTiingo(self):
		'''
		Function called for tiingo api
		'''

		'''
		JSON data loaded from the server will be stored in this dictionary for each
		security passed into the function
		'''
		pandas_data_dict = {}

		# Begin iterating through each security
		for index, val in enumerate(self.stock):
			# Ensure that the value passed to the url is of type string
			if not isinstance(val, str):
				raise ValueError("Unknown type for stock at index %d. '%s' Must be string or list of strings" % (index, val))

			# Base URL for tiingo API support
			url = 'https://api.tiingo.com/tiingo/daily/'
			# Pass parameters into url to build proper API request
			url += '%s/prices?token=%s&startDate=%s&endDate=%s' % (val.lower(), self.key, self.start, self.end)
			
			# Use Pandas default 'fron json' function to make the api call. must manually set the index to date
			urlData = pd.read_json(url, orient='records').set_index('date')

			# Append the asset and resulting DataFrame to the dictionary
			pandas_data_dict[val] = urlData
		'''
		Pandas has deprecated the 'Panel' object and therefore for future functionality, the dictionary
		of dataframes must be converted to a multiindexed dataframe. Pandas can easily convert this after defining
		a dictionary where the key is tuples of the columns and the values the actual values to pass. This function
		defines such a dictionary
		'''
		reform = {(outerKey, innerKey): values for outerKey, innerDict in pandas_data_dict.items() for innerKey, values in innerDict.items()}

		# Create the new dataframe using the dictionary above
		return_df = pd.DataFrame(reform)

		'''
		To allow for quick filtering of security information (e.g. Open, Volume, Adjusted Close, etc.)
		instead of the security itself (FB, AAPL, NFLX, etc.), the hierarchy of the indexes must be swapped
		'''
		return_df.columns = return_df.columns.swaplevel(0, 1)

		# Return the adjusted dataframe
		return return_df

	def getGoogle(self):
		return 'No key required for Google!'


if __name__ == "__main__":
	# stocklist = 'googl'
	stocklist = ['dpz', 'vg', 'voe', 'vgk', 'vnq']
	try:
		data = WebReader().get(stocklist, 'tiingo', key='85d33843a4bd0bffe1bab0beb9de8bd4e0eca039')['adjClose']
		# print(data)
	except Exception as e:
		print(e)
